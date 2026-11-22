if (document.body.classList.contains('course-home')) {
  const {mountAccountLink} = await import('./account-client.js');
  await mountAccountLink();
  const accountLink = document.querySelector('#cloud-account-link');
  if (accountLink) document.querySelector('#course-account-link').replaceWith(accountLink);
} else {
  const appendScript = source => new Promise((resolve, reject) => {
    const script = document.createElement('script');
    script.src = source;
    script.onload = resolve;
    script.onerror = reject;
    document.head.append(script);
  });

  const style = document.createElement('link');
  style.rel = 'stylesheet';
  style.href = 'assets/katex/katex.min.css';
  document.head.append(style);
  try {
    await appendScript('assets/katex/katex.min.js');
    await appendScript('assets/katex/contrib/auto-render.min.js');
  } catch (error) {
    console.error(error);
  }
  await import('./app.js?v=24');
}
