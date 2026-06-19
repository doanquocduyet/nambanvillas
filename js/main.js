/* Nam Ban Villas – Main JS */
(function(){
'use strict';

// Header scroll
const header=document.getElementById('header');
window.addEventListener('scroll',()=>header.classList.toggle('scrolled',window.scrollY>10),{passive:true});

// Mobile menu
const menuBtn=document.getElementById('menuBtn');
const nav=document.getElementById('nav');
menuBtn?.addEventListener('click',()=>{
  const o=menuBtn.classList.toggle('open');
  nav.classList.toggle('open',o);
});
document.addEventListener('click',e=>{
  if(nav?.classList.contains('open')&&!nav.contains(e.target)&&!menuBtn.contains(e.target)){
    nav.classList.remove('open');menuBtn.classList.remove('open');
  }
});

// Search tabs
document.querySelectorAll('.stab').forEach(t=>t.addEventListener('click',()=>{
  document.querySelectorAll('.stab').forEach(x=>x.classList.remove('active'));
  t.classList.add('active');
  const form=document.querySelector('.search-form');
  if(form) form.action='/'+t.dataset.tab+'/';
}));

// Listing filter
const ltabs=document.querySelectorAll('.ltab');
const cards=document.querySelectorAll('.prop-card');
ltabs.forEach(t=>t.addEventListener('click',()=>{
  ltabs.forEach(x=>x.classList.remove('active'));
  t.classList.add('active');
  const f=t.dataset.type;
  cards.forEach(c=>c.classList.toggle('hidden',f!=='all'&&c.dataset.type!==f));
}));

// QR Code – Zalo
function makeQR(id,url,size){
  const el=document.getElementById(id);
  if(!el||typeof QRCode==='undefined') return;
  new QRCode(el,{text:url,width:size||120,height:size||120,colorDark:'#1A3D2B',colorLight:'#ffffff',correctLevel:QRCode.CorrectLevel.H});
}
window.addEventListener('load',()=>{
  makeQR('qrcode','https://zalo.me/0978758788',110);
  makeQR('qrcodeLarge','https://zalo.me/0978758788',180);
});

// Animate on scroll
if('IntersectionObserver' in window){
  const obs=new IntersectionObserver(entries=>{
    entries.forEach(e=>{
      if(e.isIntersecting){e.target.style.animation='fadeUp .5s ease forwards';obs.unobserve(e.target);}
    });
  },{threshold:.1,rootMargin:'0px 0px -30px 0px'});
  document.querySelectorAll('.prop-card,.why-card,.news-card').forEach((el,i)=>{
    el.style.opacity='0';
    el.style.animationDelay=`${(i%4)*.07}s`;
    obs.observe(el);
  });
}
const s=document.createElement('style');
s.textContent='@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}';
document.head.appendChild(s);

// ===== RSS NEWS LOADER =====
// Dùng rss2json API để bypass CORS
const RSS2JSON='https://api.rss2json.com/v1/api.json?rss_url=';

async function loadRSS(containerId,rssUrl,limit=9){
  const el=document.getElementById(containerId);
  if(!el) return;
  try{
    const res=await fetch(RSS2JSON+encodeURIComponent(rssUrl)+'&count='+limit);
    const data=await res.json();
    if(data.status!=='ok'||!data.items?.length) throw new Error('no items');
    el.innerHTML=data.items.map(item=>{
      const date=new Date(item.pubDate).toLocaleDateString('vi-VN');
      const img=item.thumbnail||item.enclosure?.link||'images/news-placeholder.svg';
      const source=data.feed?.title||rssUrl.replace('https://','').split('/')[0];
      return `<article class="news-card">
        <a href="${item.link}" target="_blank" rel="noopener" class="news-card-img">
          <img src="${img}" alt="${item.title}" width="400" height="225" loading="lazy" onerror="this.src='images/news-placeholder.svg'">
        </a>
        <div class="news-card-body">
          <p class="news-source">${source}</p>
          <h3 class="news-card-title"><a href="${item.link}" target="_blank" rel="noopener">${item.title}</a></h3>
          <p class="news-date">${date}</p>
        </div>
      </article>`;
    }).join('');
  }catch(e){
    el.innerHTML='<p class="news-loading">Đang cập nhật tin tức...</p>';
  }
}

// Thi truong – BDS news
const thiTruongEl=document.getElementById('news-thi-truong');
if(thiTruongEl){
  // VnExpress BĐS + CafeF BĐS
  loadRSS('news-thi-truong','https://vnexpress.net/rss/bat-dong-san.rss');
}

// Ve Nam Ban – local news
const veNamBanEl=document.getElementById('news-ve-nam-ban');
if(veNamBanEl){
  loadRSS('news-ve-nam-ban','https://news.google.com/rss/search?q=Nam+Ban+L%C3%A2m+%C4%90%E1%BB%93ng&hl=vi&gl=VN&ceid=VN:vi');
}

// Contact form
document.getElementById('contactForm')?.addEventListener('submit',function(e){
  e.preventDefault();
  const btn=this.querySelector('.form-submit');
  btn.textContent='✓ Đã gửi! Chúng tôi sẽ liên hệ sớm.';
  btn.style.background='#16a34a';
  setTimeout(()=>{this.reset();btn.textContent='Gửi yêu cầu';btn.style.background='';},4000);
});

})();
