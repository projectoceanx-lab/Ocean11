(function () {
  const OFFER_NAME = 'Storefront Catalog';
  const STORAGE_KEY = 'ocean_lead_queue_v1';
  const form = document.getElementById('leadCaptureForm');
  const msg = document.getElementById('ctaMessage');
  const success = document.getElementById('leadSuccess');
  const exportJsonBtn = document.getElementById('exportJsonBtn');
  const exportCsvBtn = document.getElementById('exportCsvBtn');
  const mailtoBtn = document.getElementById('mailtoBtn');

  function getQueue(){ try{return JSON.parse(localStorage.getItem(STORAGE_KEY)||'[]')}catch{return []}}
  function setQueue(v){ localStorage.setItem(STORAGE_KEY, JSON.stringify(v)); }
  function note(t){ if(msg) msg.textContent=t; }
  function esc(v){ const t=String(v||''); return /[",\n]/.test(t)?`"${t.replace(/"/g,'""')}"`:t; }
  function dl(name,content,type){ const b=new Blob([content],{type}); const u=URL.createObjectURL(b); const a=document.createElement('a'); a.href=u;a.download=name;a.click(); URL.revokeObjectURL(u);} 
  function mailto(data){
    const subject=encodeURIComponent(`${OFFER_NAME} - Lead Capture`);
    const body=encodeURIComponent(`Name: ${data.name}\nEmail: ${data.email}\nTelegram: ${data.telegram||'Not provided'}\nOffer Interest: ${data.offerInterest}\nPain Point: ${data.painPoint}\nCaptured At: ${data.capturedAt}`);
    return `mailto:project.oceanx@gmail.com?subject=${subject}&body=${body}`;
  }
  if(form) form.addEventListener('submit',function(e){
    e.preventDefault();
    const d={name:form.name.value.trim(),email:form.email.value.trim(),telegram:form.telegram.value.trim(),offerInterest:form.offerInterest.value,painPoint:form.painPoint.value.trim(),sourceOffer:OFFER_NAME,capturedAt:new Date().toISOString()};
    if(d.name.length<2) return note('Name is required (min 2 characters).');
    if(!/^\S+@\S+\.\S+$/.test(d.email)) return note('A valid email is required.');
    if(!d.offerInterest) return note('Please select your offer interest.');
    if(d.painPoint.length<10) return note('Pain point is required (min 10 characters).');
    const q=getQueue(); q.push(d); setQueue(q);
    if(mailtoBtn) mailtoBtn.href=mailto(d);
    if(success) success.hidden=false;
    note('Lead saved locally. Next step: click Open Email Draft or export JSON/CSV.');
    form.reset();
  });
  if(exportJsonBtn) exportJsonBtn.addEventListener('click',()=>{const q=getQueue(); if(!q.length) return note('No saved leads yet.'); dl(`ocean-leads-${new Date().toISOString().slice(0,10)}.json`,JSON.stringify(q,null,2),'application/json');});
  if(exportCsvBtn) exportCsvBtn.addEventListener('click',()=>{const q=getQueue(); if(!q.length) return note('No saved leads yet.'); const h=['name','email','telegram','offerInterest','painPoint','sourceOffer','capturedAt']; const lines=[h.join(',')].concat(q.map(r=>h.map(k=>esc(r[k])).join(','))); dl(`ocean-leads-${new Date().toISOString().slice(0,10)}.csv`,lines.join('\n'),'text/csv');});
})();