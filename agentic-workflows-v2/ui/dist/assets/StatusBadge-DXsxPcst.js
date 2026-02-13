import{c as e,j as a}from"./index-DqAERJQh.js";/**
 * @license lucide-react v0.468.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const s=e("Ban",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"m4.9 4.9 14.2 14.2",key:"1m5liu"}]]);/**
 * @license lucide-react v0.468.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const t=e("CircleCheck",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"m9 12 2 2 4-4",key:"dzmm74"}]]);/**
 * @license lucide-react v0.468.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const y=e("CircleX",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["path",{d:"m15 9-6 6",key:"1uzhvr"}],["path",{d:"m9 9 6 6",key:"z0biqf"}]]);/**
 * @license lucide-react v0.468.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const g=e("Clock",[["circle",{cx:"12",cy:"12",r:"10",key:"1mglay"}],["polyline",{points:"12 6 12 12 16 14",key:"68esgv"}]]);/**
 * @license lucide-react v0.468.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const d=e("LoaderCircle",[["path",{d:"M21 12a9 9 0 1 1-6.219-8.56",key:"13zald"}]]);/**
 * @license lucide-react v0.468.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const m=e("SkipForward",[["polygon",{points:"5 4 15 12 5 20 5 4",key:"16p6eg"}],["line",{x1:"19",x2:"19",y1:"5",y2:"19",key:"futhcm"}]]);/**
 * @license lucide-react v0.468.0 - ISC
 *
 * This source code is licensed under the ISC license.
 * See the LICENSE file in the root directory of this source tree.
 */const x=e("Timer",[["line",{x1:"10",x2:"14",y1:"2",y2:"2",key:"14vaq8"}],["line",{x1:"12",x2:"15",y1:"14",y2:"11",key:"17fdiu"}],["circle",{cx:"12",cy:"14",r:"8",key:"1e1u0o"}]]),o={pending:{color:"text-gray-400",bg:"bg-gray-400/10",icon:g,label:"Pending"},running:{color:"text-blue-400",bg:"bg-blue-400/10",icon:d,label:"Running"},success:{color:"text-green-400",bg:"bg-green-400/10",icon:t,label:"Success"},failed:{color:"text-red-400",bg:"bg-red-400/10",icon:y,label:"Failed"},skipped:{color:"text-amber-400",bg:"bg-amber-400/10",icon:m,label:"Skipped"},cancelled:{color:"text-gray-500",bg:"bg-gray-500/10",icon:s,label:"Cancelled"}};function b({status:l,size:n="sm"}){const c=o[l]??o.pending,r=c.icon,i=n==="sm"?"text-xs px-2 py-0.5":"text-sm px-3 py-1";return a.jsxs("span",{className:`inline-flex items-center gap-1 rounded-full font-medium ${c.bg} ${c.color} ${i}`,children:[a.jsx(r,{className:`${n==="sm"?"h-3 w-3":"h-4 w-4"} ${l==="running"?"animate-spin":""}`}),c.label]})}export{t as C,d as L,b as S,x as T,y as a,g as b,m as c};
