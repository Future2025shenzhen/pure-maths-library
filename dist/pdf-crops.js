// Keep PDF work close to the viewport and reuse previews across list renders.
export function createCropLoader(scale) {
  const documents = new Map();
  const previews = new Map();
  const pending = new Set();
  let pdfModule;

  function copy(target, source) {
    target.width = source.width;
    target.height = source.height;
    target.getContext('2d').drawImage(source, 0, 0);
    target.dataset.ready = 'true';
  }

  async function draw(canvas) {
    const key = canvas.dataset.pdfCrop;
    if (previews.has(key)) {
      const preview = previews.get(key);
      previews.delete(key);
      previews.set(key, preview);
      copy(canvas, preview);
      return;
    }
    const {pdf: url, page: number, crop: [x, y, width, height]} = JSON.parse(decodeURIComponent(key));
    const pdfjs = await (pdfModule ??= import('./assets/pdfjs/pdf.mjs').then(module => {
      module.GlobalWorkerOptions.workerSrc = new URL('./assets/pdfjs/pdf.worker.mjs', import.meta.url).href;
      return module;
    }));
    if (!canvas.isConnected) return;

    let entry = documents.get(url);
    if (!entry) {
      const task = pdfjs.getDocument({url, isEvalSupported: false});
      entry = {task, users: 0};
    }
    documents.delete(url);
    documents.set(url, entry);
    entry.users++;
    try {
      const page = await (await entry.task.promise).getPage(number);
      if (!canvas.isConnected) return;
      const viewport = page.getViewport({scale});
      const preview = document.createElement('canvas');
      preview.width = Math.max(1, Math.round(viewport.width * width));
      preview.height = Math.max(1, Math.round(viewport.height * height));
      const context = preview.getContext('2d');
      context.fillStyle = '#fff';
      context.fillRect(0, 0, preview.width, preview.height);
      await page.render({canvasContext: context, viewport, transform: [1, 0, 0, 1, -viewport.width * x, -viewport.height * y]}).promise;
      previews.set(key, preview);
      if (previews.size > 18) previews.delete(previews.keys().next().value);
      if (canvas.isConnected) copy(canvas, preview);
    } catch (error) {
      if (documents.get(url) === entry) documents.delete(url);
      throw error;
    } finally {
      entry.users--;
      if (!entry.users && documents.get(url) !== entry) entry.task.destroy().catch(() => {});
      for (const [oldUrl, old] of documents) {
        if (documents.size <= 6) break;
        if (old.users) continue;
        documents.delete(oldUrl);
        old.task.destroy().catch(() => {});
      }
    }
  }

  let running = 0;
  function drain() {
    while (running < 2 && pending.size) {
      const canvas = pending.values().next().value;
      pending.delete(canvas);
      if (!canvas.isConnected || canvas.closest('[hidden]')) {
        delete canvas.dataset.ready;
        continue;
      }
      running++;
      draw(canvas).catch(error => {
        canvas.dataset.ready = 'error';
        console.error(error);
      }).finally(() => {
        running--;
        drain();
      });
    }
  }

  const observer = typeof IntersectionObserver === 'function' ? new IntersectionObserver(entries => {
    for (const {target, isIntersecting} of entries) {
      if (!isIntersecting || target.closest('[hidden]')) continue;
      observer.unobserve(target);
      pending.add(target);
    }
    drain();
  }, {rootMargin: '180px 0px'}) : null;

  return {
    observe(canvas) {
      if (canvas.closest('[hidden]')) return;
      canvas.dataset.ready = 'loading';
      if (observer) observer.observe(canvas);
      else {
        pending.add(canvas);
        drain();
      }
    },
    disconnect() {
      observer?.disconnect();
      pending.clear();
    }
  };
}
