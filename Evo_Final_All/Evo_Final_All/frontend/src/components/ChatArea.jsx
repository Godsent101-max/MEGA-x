import React, { useEffect, useRef, useState } from 'react';
import api from '../services/api.js';

export default function ChatArea({ token, onAuth }){
const genImage = async ()=>{
  const p = prompt('Enter image prompt');
  if(!p) return;
  const res = await api.post('/image/gen', { prompt: p }, { headers:{ Authorization: 'Bearer '+token } });
  if(res.data.url){
    // open image in new tab
    window.open(res.data.url, '_blank');
  } else if(res.data.error){
    alert('Image gen error: ' + res.data.error);
  }
};

  const [username, setUsername] = useState('user1');
  const [password, setPassword] = useState('pass');
  const [sessions, setSessions] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const fileRef = useRef();

  useEffect(()=>{ if(token) loadSessions(); },[token]);

  const signup = async ()=>{
    try{ await api.post('/auth/signup', { username, password }); alert('signed up'); }catch(e){ alert('err:'+e?.response?.data?.detail); }
  };
  const login = async ()=>{
    try{ const res = await api.post('/auth/login', { username, password }); const t = res.data.access_token; localStorage.setItem('token', t); if(onAuth) onAuth(t); window.location.reload(); }catch(e){ alert('login failed'); }
  };
  const loadSessions = async ()=>{
    const res = await api.get('/chat/sessions', { headers:{ Authorization: 'Bearer '+token } });
    setSessions(res.data);
    if(res.data.length>0){ setSessionId(res.data[0].session_id); localStorage.setItem('session', res.data[0].session_id); loadHistory(res.data[0].session_id); }
    else { const ns = await api.post('/chat/session', {}, { headers:{ Authorization: 'Bearer '+token } }); loadSessions(); }
  };
  const loadHistory = async (sid)=>{
    const res = await api.get('/chat/history/'+sid, { headers:{ Authorization: 'Bearer '+token } });
    setMessages(res.data);
  };
  const send = async ()=>{
    if(!input.trim()) return;
    const res = await api.post('/chat', { message: input, session_id: sessionId }, { headers:{ Authorization: 'Bearer '+token } });
    setMessages(prev=>[...prev, res.data]);
    setInput('');
  };
  const onFile = async (e)=>{
    const f = e.target.files[0]; if(!f) return;
    const text = await f.text();
    setInput(text.substring(0,500));
  };
  // original placeholder removed
    alert('Voice recording placeholder — integrate STT in full build');
  };

  if(!token) return (
    <div style={{background:'#fff', padding:12, borderRadius:8}}>
      <h3>Login / Signup</h3>
      <input value={username} onChange={e=>setUsername(e.target.value)} placeholder='username' /><br/>
      <input value={password} onChange={e=>setPassword(e.target.value)} placeholder='password' type='password' /><br/>
      <button onClick={signup}>Signup</button>
      <button onClick={login}>Login</button>
    </div>
  );

  return (
    <div style={{background:'#fff', padding:12, borderRadius:8, height:'80vh', display:'flex', flexDirection:'column'}}>
      <div style={{display:'flex', justifyContent:'space-between', marginBottom:8}}>
        <div>
          <button onClick={()=>{ /* prev */ }}>◀</button>
          <button onClick={()=>{ /* next */ }}>▶</button>
          <button onClick={async ()=>{ await api.post('/chat/session', {}, { headers:{ Authorization: 'Bearer '+token } }); loadSessions(); }}>＋ New</button>
        </div>
        <div style={{fontSize:12, color:'#666'}}>Swipe left/right on mobile to switch sessions</div>
      </div>
      <div style={{flex:1, overflowY:'auto', border:'1px solid #eee', padding:8}}>
        {messages.map(m=> (<div key={m.id} style={{marginBottom:12}}>
          <div style={{fontSize:12, color:'#666'}}> {m.timestamp || ''} </div>
          <div><b>You:</b> {m.message}</div>
          <div style={{marginTop:6, padding:8, background:'#f6f8fa'}}><b>Evo:</b> {m.response}</div>
        </div>))}
      </div>
      <div style={{display:'flex', gap:8, marginTop:8}}>
        <input type='file' ref={fileRef} style={{display:'none'}} onChange={onFile} />
        <button onClick={()=>fileRef.current.click()}>📂 Import</button>
        <button onClick={recordVoice}>🎤 Voice</button> <button onClick={genImage}>🖼️ Gen Image</button>
        <input value={input} onChange={e=>setInput(e.target.value)} placeholder='Type a message or import text...' style={{flex:1}} />
        <button onClick={send}>Send</button>
      </div>
    </div>
  );
}