import {useState} from 'react'; import {ArrowUpRight, Sparkles, Send, RotateCcw, CheckCircle2, AlertCircle} from 'lucide-react';
import {predict,explain,sendFeedback} from '../api';
const examples=[{lang:'HINDI',text:'जलवायु परिवर्तन और ग्लोबल वार्मिंग बहुत गंभीर समस्या है। हमें अभी कदम उठाने होंगे।'},{lang:'BENGALI',text:'জলবায়ু পরিবর্তন আমাদের ভবিষ্যতের জন্য একটি বড় বিপদ।'},{lang:'ROMANISED HINDI',text:'Climate change kuch nahi hai, ye sab natural hai.'},{lang:'ROMANISED BENGALI',text:'Prithibir gorom bere jacche, eta khub chintar bishoy.'}];
export default function Classifier(){
 const [text,setText]=useState('');const [result,setResult]=useState<any>(null);const [busy,setBusy]=useState(false);const [error,setError]=useState('');const [why,setWhy]=useState<any>(null);const [feedback,setFeedback]=useState('');
 async function run(){if(!text.trim())return;setBusy(true);setError('');setResult(null);setWhy(null);try{setResult(await predict(text.trim()))}catch(e:any){setError(e.message)}finally{setBusy(false)}}
 const colors:any={Favour:'green',Against:'red',None:'grey'};
 return <><div className="eyebrow"><span className="eyebrow-line"/> MULTILINGUAL NLP · LIVE CLASSIFIER</div>
 <div className="hero-row"><div><h1>Understand the <em>stance.</em></h1><p className="lead">Explore how Hindi and Bengali social comments respond to the climate concern claim.</p></div><div className="hero-mark"><Sparkles size={25}/><span>3-CLASS<br/>PREDICTION</span></div></div>
 <div className="claim-card"><div className="claim-icon"><AlertCircle size={19}/></div><div><small>THE CLAIM</small><p>“Climate change and global warming is a serious concern.”</p></div></div>
 <div className="section-heading"><div><h2>Comment classifier</h2><p>Enter a comment to identify its expressed stance.</p></div><span className="model-chip">TF-IDF + Linear SVM</span></div>
 <div className="workspace-grid"><section className="panel input-panel"><div className="panel-top"><span>YOUR COMMENT</span><span className="counter">{text.length}/10,000</span></div><textarea value={text} maxLength={10000} onChange={e=>setText(e.target.value)} placeholder="अपना कमेंट यहाँ लिखें… / আপনার মন্তব্য এখানে লিখুন… / Type a comment here…"/>
 <div className="input-bottom"><span>Hindi · Bengali · Romanised · Code-mixed</span><button className="clear-btn" onClick={()=>{setText('');setResult(null);setError('')}}><RotateCcw size={14}/> Clear</button></div>
 <button className="primary-btn" disabled={!text.trim()||busy} onClick={run}>{busy?'Analysing…':'Analyse stance'} <ArrowUpRight size={17}/></button>
 {error&&<div className="error-box">{error}. Make sure the backend is running and the model has been trained.</div>}
 </section>
 <aside className="panel examples-panel"><div className="panel-top">TRY AN EXAMPLE <Sparkles size={15}/></div><p className="muted">Select a sample to populate the classifier.</p>{examples.map((e,i)=><button className="example" key={i} onClick={()=>{setText(e.text);setResult(null)}}><span>{e.lang}</span><p>{e.text}</p><ArrowUpRight size={15}/></button>)}</aside></div>
 {result&&<section className="result-panel"><div className="result-head"><div><div className="eyebrow">MODEL OUTPUT</div><h2>Prediction result</h2></div><span className={`stance-badge ${colors[result.predicted_label]}`}>{result.predicted_label}</span></div>
 <p className="result-text">“{result.text}”</p><div className="score-list">{Object.entries(result.scores||{}).map(([k,v]:any)=><div className="score-row" key={k}><div><span>{k}</span><b>{(v*100).toFixed(1)}%</b></div><div className="score-track"><i className={colors[k]} style={{width:`${v*100}%`}}/></div></div>)}</div>
 <p className="score-note">{result.score_note} Detected script: {result.detected_language}.</p>
 <div className="result-actions"><button className="secondary-btn" onClick={async()=>{try{setWhy(await explain(text))}catch(e:any){setError(e.message)}}}>Why this prediction?</button><div className="feedback-actions"><span>Was this correct?</span>{['Favour','Against','None'].map(l=><button key={l} onClick={async()=>{await sendFeedback({text,predicted_label:result.predicted_label,corrected_label:l,prediction_id:result.id});setFeedback('Feedback saved. Thank you!')}}>{l}</button>)}</div></div>
 {why&&<div className="explain-box"><b>Top model features</b><p>{why.note}</p><div className="feature-tags">{why.top_features.map((f:any)=><span key={f.feature}>{f.feature}</span>)}</div></div>}{feedback&&<p className="success-note"><CheckCircle2 size={15}/>{feedback}</p>}
 </section>}
 <div className="class-legend"><div><i className="dot green"/> <b>Favour</b><span>Supports the claim</span></div><div><i className="dot red"/> <b>Against</b><span>Opposes the claim</span></div><div><i className="dot grey"/> <b>None</b><span>No clear stance</span></div></div>
 </>;
}
