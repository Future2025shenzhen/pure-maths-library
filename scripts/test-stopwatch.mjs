import assert from 'node:assert/strict';
import {Stopwatch} from '../dist/stopwatch.js';
let now=0;const watch=new Stopwatch(()=>now);
assert.equal(watch.format(),'00:00:00');now=10000;assert.equal(watch.format(),'00:00:00');
watch.start();now+=2500;assert.equal(watch.format(),'00:00:02');watch.start();now+=500;assert.equal(watch.format(),'00:00:03');
watch.pause();now+=90000;assert.equal(watch.format(),'00:00:03');watch.start();now+=1000;assert.equal(watch.format(),'00:00:04');
watch.reset();assert(!watch.running);assert.equal(watch.format(),'00:00:00');watch.restore(3661000);assert.equal(watch.format(),'01:01:01');
console.log('PASS manual stopwatch: initial pause, start, pause, resume, reset, elapsed background time and hours');
