import React, { useState } from 'react';
import ChatArea from './components/ChatArea.jsx';
import BiometricsPanel from './components/BiometricsPanel.jsx';
import api from './services/api.js';

export default function App(){
  const playAudio = (b64)=>{ const audio = new Audio(b64); audio.play(); };

  const [token, setToken] = useState(localStorage.getItem('token')||'');
  const [mode, setMode] = useState(token ? 'chat' : 'login');

  return (
    <div style={{fontFamily:'sans-serif'}}>
      <div style={{background:'#0f172a', color:'#fff', padding:12, display:'flex', justifyContent:'space-between'}}>
        <div><strong>Evo (Prototype)</strong></div>
        {token && <div style={{display:'flex', gap:8}}>
          <button onClick={()=>{ if(window.confirm('Save as text?')){ const sid = localStorage.getItem('session'); if(sid) window.open(api.defaults.baseURL + '/export/txt/' + sid); }}}>💾 Save</button>
          <button onClick={()=>{ navigator.clipboard.writeText(window.location.href); alert('Link copied (prototype)');}}>🔗 Share</button>
          <button onClick={()=>{ localStorage.removeItem('token'); setToken(''); setMode('login'); }}>Logout</button>
        </div>}
      </div>
      <div style={{display:'grid', gridTemplateColumns:'1fr 360px', gap:12, padding:12}}>
        <ChatArea token={token} onAuth={(t)=>{ localStorage.setItem('token', t); setToken(t); setMode('chat'); }} />
        <div>
          <BiometricsPanel token={token} />
        </div>
      </div>
    </div>
  );
}