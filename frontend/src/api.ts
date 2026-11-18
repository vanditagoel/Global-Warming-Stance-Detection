const API = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000";
export async function predict(text:string){
 const r=await fetch(`${API}/predict`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text})});
 if(!r.ok){const e=await r.json().catch(()=>({detail:"Request failed"}));throw new Error(e.detail||"Prediction failed");}
 return r.json();
}
export async function batchPredict(texts:string[]){
 const r=await fetch(`${API}/predict/batch`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({texts})});
 if(!r.ok){const e=await r.json().catch(()=>({detail:"Request failed"}));throw new Error(e.detail||"Batch prediction failed");}
 return r.json();
}
export async function getAnalytics(){const r=await fetch(`${API}/analytics`);if(!r.ok)throw new Error("Could not load analytics");return r.json();}
export async function explain(text:string){const r=await fetch(`${API}/explain`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({text})});if(!r.ok)throw new Error("Explanation unavailable");return r.json();}
export async function sendFeedback(payload:any){const r=await fetch(`${API}/feedback`,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(payload)});if(!r.ok)throw new Error("Could not save feedback");return r.json();}
