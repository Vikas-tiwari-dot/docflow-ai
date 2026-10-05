const API=import.meta.env.VITE_API_URL||'http://localhost:8000';
export async function api(path,options={}){const token=localStorage.getItem('docflow_token');const headers={...(options.body instanceof FormData?{}:{'Content-Type':'application/json'}),...(options.headers||{})};if(token)headers.Authorization=`Bearer ${token}`;const r=await fetch(API+path,{...options,headers});const data=await r.json().catch(()=>({}));if(!r.ok)throw new Error(data?.detail?.error?.message||data?.error?.message||'Request failed');return data}
export const apiBase=API;
