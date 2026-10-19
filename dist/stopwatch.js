// Count elapsed time from a monotonic clock so background throttling cannot lose seconds.
export class Stopwatch{
 constructor(now=()=>performance.now()){this.now=now;this.elapsed=0;this.startedAt=null;}
 get running(){return this.startedAt!==null;}
 get milliseconds(){return this.elapsed+(this.running?Math.max(0,this.now()-this.startedAt):0);}
 start(){if(!this.running)this.startedAt=this.now();}
 pause(){if(this.running){this.elapsed=this.milliseconds;this.startedAt=null;}}
 reset(){this.elapsed=0;this.startedAt=null;}
 restore(ms){this.elapsed=Number.isFinite(ms)&&ms>=0?ms:0;this.startedAt=null;}
 format(){const s=Math.floor(this.milliseconds/1000);return [Math.floor(s/3600),Math.floor(s/60)%60,s%60].map(x=>String(x).padStart(2,'0')).join(':');}
}
