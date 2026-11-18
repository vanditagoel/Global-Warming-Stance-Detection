import {useState} from 'react';
import {Activity, Leaf, MessageSquareText, BarChart3, Info, Menu, X} from 'lucide-react';
import Classifier from './pages/Classifier';
import Batch from './pages/Batch';
import Analytics from './pages/Analytics';
import About from './pages/About';

type Page='classifier'|'batch'|'analytics'|'about';
export default function App(){
 const [page,setPage]=useState<Page>('classifier'); const [open,setOpen]=useState(false);
 const nav=[['classifier','Classifier',MessageSquareText],['batch','Batch analysis',Activity],['analytics','Analytics',BarChart3],['about','Methodology',Info]] as const;
 return <div className="app-shell">
  <aside className={`sidebar ${open?'show':''}`}>
   <div className="brand"><div className="brand-icon"><Leaf size={22}/></div><div><b>ClimateStance</b><small>INDIC NLP CHALLENGE</small></div></div>
   <div className="nav-label">WORKSPACE</div>
   {nav.map(([id,label,Icon])=><button key={id} className={`nav-item ${page===id?'active':''}`} onClick={()=>{setPage(id);setOpen(false)}}><Icon size={18}/>{label}</button>)}
   <div className="sidebar-note"><span className="live-dot"/> Research workspace <small>Hindi · Bengali · Code-mixed</small></div>
   <div className="sidebar-footer">STANCE DETECTION · v1.0</div>
  </aside>
  {open&&<div className="scrim" onClick={()=>setOpen(false)}/>}
  <main className="main-area">
   <header className="topbar"><button className="mobile-menu" onClick={()=>setOpen(!open)}>{open?<X/>:<Menu/>}</button><div className="crumb">Research workspace <span>/</span> {nav.find(n=>n[0]===page)?.[1]}</div><div className="top-pill"><span className="live-dot"/> API-connected UI</div></header>
   <div className="content">
    {page==='classifier'&&<Classifier/>}{page==='batch'&&<Batch/>}{page==='analytics'&&<Analytics/>}{page==='about'&&<About/>}
   </div>
   <footer className="footer">INDIC CLIMATE STANCE CHALLENGE <span>Research prototype · Predictions are not ground truth</span></footer>
  </main>
 </div>
}
