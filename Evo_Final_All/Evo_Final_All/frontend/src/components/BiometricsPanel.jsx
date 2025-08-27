import React, { useEffect, useRef, useState } from 'react';
import api from '../services/api.js';

export default function BiometricsPanel({ token }){
  const videoRef = useRef();
  const [status, setStatus] = useState('');
  useEffect(()=>{ (async ()=>{ try{ const s = await navigator.mediaDevices.getUserMedia({ video:true }); videoRef.current.srcObject = s; await videoRef.current.play(); }catch(e){ console.warn('camera blocked'); } })(); },[]);

  const captureData = ()=>{
    const v = videoRef.current;
    if(!v) return null;
    const c = document.createElement('canvas'); c.width=v.videoWidth; c.height=v.videoHeight; c.getContext('2d').drawImage(v,0,0);
    return c.toDataURL('image/jpeg');
  };
  const enroll = async ()=>{
    const data = captureData();
    try{ await api.post('/biometrics/enroll/face', { image_b64: data }, { headers:{ Authorization: 'Bearer '+token } }); setStatus('Enrolled'); }catch(e){ setStatus('enroll failed'); }
  };
  const verify = async ()=>{
    const data = captureData();
    try{ const res = await api.post('/biometrics/verify/face', { image_b64: data }, { headers:{ Authorization: 'Bearer '+token } }); setStatus('Match: '+res.data.match); }catch(e){ setStatus('verify failed'); }
  };

  return (
    <div style={{background:'#fff', padding:12, borderRadius:8}}>
      <h4>Biometrics & Emotion</h4>
      <video ref={videoRef} style={{width:'100%', background:'#000'}} muted playsInline />
      <div style={{display:'flex', gap:8, marginTop:8}}>
        <button onClick={enroll}>Enroll Face</button>
        <button onClick={verify}>Verify Face</button>
      </div>
      <div style={{marginTop:8}}>{status}</div>
      <p style={{fontSize:12, color:'#666'}}>Camera images are sent only when you click enroll/verify.</p>
    </div>
  );
}