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
  const animEls=document.querySelectorAll('.prop-card,.why-card,.news-card');
  animEls.forEach((el,i)=>{
    el.style.opacity='0';
    el.style.animationDelay=`${(i%4)*.07}s`;
    obs.observe(el);
  });
  // Fallback: nếu element không vào viewport sau 2.5s thì show hết
  setTimeout(()=>animEls.forEach(el=>{if(el.style.opacity==='0')el.style.opacity='1';}),2500);
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

/* Ẩn thẻ "Có thể bạn quan tâm" nếu ảnh lỗi/thiếu */
document.querySelectorAll('.related-card img').forEach(function(img){
  function hide(){var c=img.closest('.related-card');if(c)c.style.display='none';}
  if(img.complete&&img.naturalWidth===0)hide();
  img.addEventListener('error',hide);
});

/* ===== SO SÁNH LÔ ===== */
(function(){
  const cards=document.querySelectorAll('.prop-card');
  if(!cards.length)return;
  const MAX=2;
  let selected=[]; // {id,img,title,href,price,area,loc,specs[]}

  function readCard(card){
    const img=card.querySelector('.prop-img-wrap img');
    const tA=card.querySelector('.prop-title a');
    const price=card.querySelector('.prop-price');
    const area=card.querySelector('.prop-area');
    const loc=card.querySelector('.prop-loc');
    const specs=card.querySelectorAll('.prop-specs span');
    const href=tA?tA.getAttribute('href'):'#';
    return {
      id:href+'|'+(price?price.textContent:''),
      img:img?img.getAttribute('src'):'',
      title:tA?tA.textContent.trim():'',
      href:href,
      price:price?price.textContent.trim():'—',
      area:area?area.textContent.trim():'—',
      loc:loc?loc.textContent.replace(/\s+/g,' ').trim():'—',
      specs:Array.prototype.map.call(specs,s=>s.textContent.trim())
    };
  }

  // Nút "+ So sánh" gắn vào mỗi card
  cards.forEach(card=>{
    const body=card.querySelector('.prop-body');
    if(!body)return;
    const btn=document.createElement('button');
    btn.type='button';
    btn.className='cmp-btn';
    btn.innerHTML='<span class="cmp-plus">＋ So sánh lô này</span><span class="cmp-tick">✓ Đang so sánh</span>';
    btn.addEventListener('click',()=>toggle(card,btn));
    body.appendChild(btn);
    card._cmpBtn=btn;
  });

  function toggle(card,btn){
    const data=readCard(card);
    const idx=selected.findIndex(s=>s.id===data.id);
    if(idx>-1){selected.splice(idx,1);btn.classList.remove('active');}
    else{
      if(selected.length>=MAX){
        // thay lô cũ nhất
        const removed=selected.shift();
        cards.forEach(c=>{if(c._cmpData&&c._cmpData.id===removed.id){c._cmpBtn.classList.remove('active');}});
      }
      selected.push(data);card._cmpData=data;btn.classList.add('active');
    }
    renderBar();
  }

  // Thanh dưới màn hình
  const bar=document.createElement('div');
  bar.className='cmp-bar';
  bar.innerHTML='<div class="container cmp-bar-inner"><div class="cmp-slots"></div><button type="button" class="cmp-go" disabled>So sánh</button><button type="button" class="cmp-clear" aria-label="Xoá hết">✕</button></div>';
  document.body.appendChild(bar);
  const slotsEl=bar.querySelector('.cmp-slots');
  const goBtn=bar.querySelector('.cmp-go');
  const clearBtn=bar.querySelector('.cmp-clear');

  function renderBar(){
    if(!selected.length){bar.classList.remove('show');return;}
    bar.classList.add('show');
    let html='';
    for(let i=0;i<MAX;i++){
      const s=selected[i];
      if(s){
        html+='<div class="cmp-slot"><img src="'+s.img+'" alt=""><div class="cmp-slot-info"><div class="cmp-slot-price">'+s.price+'</div><div class="cmp-slot-title">'+s.area+'</div></div><button type="button" class="cmp-slot-x" data-id="'+s.id+'">✕</button></div>';
      }else{
        html+='<div class="cmp-slot cmp-slot-empty">Chọn thêm 1 lô…</div>';
      }
    }
    slotsEl.innerHTML=html;
    goBtn.disabled=selected.length<2;
    goBtn.textContent=selected.length<2?'Chọn 2 lô':'So sánh 2 lô';
    slotsEl.querySelectorAll('.cmp-slot-x').forEach(x=>{
      x.addEventListener('click',()=>{
        const id=x.getAttribute('data-id');
        selected=selected.filter(s=>s.id!==id);
        cards.forEach(c=>{if(c._cmpData&&c._cmpData.id===id)c._cmpBtn.classList.remove('active');});
        renderBar();
      });
    });
  }

  clearBtn.addEventListener('click',()=>{
    selected=[];
    cards.forEach(c=>c._cmpBtn&&c._cmpBtn.classList.remove('active'));
    renderBar();
  });

  // Modal so sánh
  const ov=document.createElement('div');
  ov.className='cmp-modal-ov';
  ov.innerHTML='<div class="cmp-modal" role="dialog" aria-label="So sánh lô đất"><button type="button" class="cmp-modal-close" aria-label="Đóng">✕</button><h3 class="cmp-modal-title">So Sánh 2 Lô</h3><div class="cmp-modal-body"></div></div>';
  document.body.appendChild(ov);
  const modalBody=ov.querySelector('.cmp-modal-body');
  ov.addEventListener('click',e=>{if(e.target===ov)closeModal();});
  ov.querySelector('.cmp-modal-close').addEventListener('click',closeModal);
  function closeModal(){ov.classList.remove('show');}

  goBtn.addEventListener('click',()=>{
    if(selected.length<2)return;
    const a=selected[0],b=selected[1];
    const row=(label,va,vb)=>'<tr><th>'+label+'</th><td>'+va+'</td><td>'+vb+'</td></tr>';
    const specList=s=>s.specs.length?s.specs.map(x=>'• '+x).join('<br>'):'—';
    let html='<table class="cmp-table"><thead><tr><th></th>';
    [a,b].forEach(s=>{html+='<td class="cmp-col-head"><img src="'+s.img+'" alt=""><a href="'+s.href+'" class="cmp-col-title">'+s.title+'</a></td>';});
    html+='</tr></thead><tbody>';
    html+=row('Giá','<strong>'+a.price+'</strong>','<strong>'+b.price+'</strong>');
    html+=row('Diện tích',a.area,b.area);
    html+=row('Vị trí',a.loc,b.loc);
    html+=row('Đặc điểm',specList(a),specList(b));
    html+='</tbody><tfoot><tr><th></th>';
    [a,b].forEach(s=>{html+='<td><a href="'+s.href+'" class="cmp-col-cta">Hỏi về lô này →</a></td>';});
    html+='</tr></tfoot></table>';
    modalBody.innerHTML=html;
    ov.classList.add('show');
  });
})();

})();
