#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GẮN Ô LỌC CHO TRANG KHU NHIỀU LÔ.

Trang trung tâm Nam Ban có 96 thẻ — cuộn quá dài, khách phải lướt qua cả trăm lô
mới thấy cái hợp túi tiền. Gắn ô lọc giống hub: tìm nhanh + diện tích + mức giá.

Chỉ gắn cho trang có từ NGUONG thẻ trở lên; trang ít lô thì ô lọc là thừa.

Dùng lại đúng cơ chế đã chạy ổn ở /dat-nen-nam-ban/:
  - đọc data-area / data-price / data-ban trên từng thẻ
  - lô ĐÃ BÁN: không lọc thì vẫn hiện (giữ làm tham khảo), có lọc thì ẩn
  - ghi trạng thái vào URL để chia sẻ/lưu/back được
  - có trạng thái rỗng kèm nút gọi, không để khách nhìn màn hình trắng
"""
import glob
import os
import re

os.chdir("/home/user/nambanvillas")
NGUONG = 20

CSS = """<style>
.kl-box{display:flex;gap:12px;flex-wrap:wrap;background:#F7F3EE;padding:16px;border-radius:12px;margin:0 0 18px}
.kl-tim{flex:1 1 100%;display:flex;align-items:center;gap:9px;background:#fff;border:2px solid #E2DBD0;border-radius:10px;padding:0 12px}
.kl-tim input{flex:1;min-width:0;border:0;outline:none;background:transparent;font-family:inherit;font-size:.92rem;padding:11px 0;color:#1A3D2B}
.kl-box select{flex:1;min-width:130px;padding:9px 12px;border:2px solid #E2DBD0;border-radius:8px;font-family:inherit;font-size:.88rem;outline:none;background:#fff;color:#1A3D2B}
.kl-box select:focus-visible,.kl-tim:focus-within{outline:2.5px solid #1A3D2B;outline-offset:2px}
.kl-dem{margin:0 0 14px;font-size:.9rem;color:#5F6F63}
.kl-dem strong{color:#1A3D2B}
.kl-trong{display:none;padding:18px;background:#F0F4F1;border-radius:12px;color:#3D4A40;font-size:.95rem;line-height:1.7}
.kl-trong a{color:#1A3D2B;font-weight:700}
.sp-sang .sp-row.an-di{display:none!important}
@media(max-width:560px){.kl-box select{flex:1 1 100%}}
</style>
"""

HTML = """<form class="kl-box" onsubmit="return false" aria-label="Lọc lô trong khu">
      <label class="kl-tim" for="kl-q">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#1A3D2B" stroke-width="1.7" stroke-linecap="round" aria-hidden="true" style="flex:0 0 18px"><circle cx="11" cy="11" r="7"></circle><path d="M20 20l-3.5-3.5"></path></svg>
        <input id="kl-q" type="search" enterkeyhint="search" placeholder="Tìm nhanh: thổ cư, view, lô góc, mặt tiền…" aria-label="Tìm lô trong khu">
      </label>
      <select id="kl-area" aria-label="Lọc theo diện tích">
        <option value="">Tất cả diện tích</option>
        <option value="u500">Dưới 500m²</option>
        <option value="500-1000">500–1.000m²</option>
        <option value="o1000">Trên 1.000m²</option>
      </select>
      <select id="kl-price" aria-label="Lọc theo mức giá">
        <option value="">Tất cả mức giá</option>
        <option value="u0.7">Dưới 700 triệu</option>
        <option value="0.7-1">700 triệu – 1 tỷ</option>
        <option value="1-2">1 – 2 tỷ</option>
        <option value="o2">Trên 2 tỷ</option>
      </select>
    </form>
    <p class="kl-dem">Đang hiện <strong id="kl-so">%(n)d</strong> lô</p>
    <p class="kl-trong" id="kl-trong">Chưa có lô nào khớp bộ lọc này. <a href="#" id="kl-reset">Bỏ lọc, xem lại tất cả</a> hoặc gọi <a href="tel:0978758788">0978 758 788</a> để Nam Ban Villas tìm giúp.</p>
"""

JS = """<script>
(function(){
  var q=document.getElementById('kl-q'),ar=document.getElementById('kl-area'),
      pr=document.getElementById('kl-price'),so=document.getElementById('kl-so'),
      trong=document.getElementById('kl-trong'),reset=document.getElementById('kl-reset');
  if(!q||!ar||!pr)return;
  var the=[].slice.call(document.querySelectorAll('.prop-grid.sp-sang .prop-card'));
  function bochu(s){return s.normalize('NFD').replace(/[\\u0300-\\u036f]/g,'').replace(/\\u0111/g,'d').replace(/\\u0110/g,'D').toLowerCase();}
  function chay(ghiUrl){
    var av=ar.value,pv=pr.value,qv=bochu(q.value.trim()),qw=qv?qv.split(/\\s+/):[];
    var coLoc=!!(av||pv||qw.length),hien=0;
    the.forEach(function(c){
      if(!c._txt)c._txt=bochu(c.textContent||'');
      var a=parseFloat(c.getAttribute('data-area')),p=parseFloat(c.getAttribute('data-price'));
      var daBan=c.getAttribute('data-ban')==='1',ok=true;
      // Lô đã bán luôn nằm trên trang, nhưng khi khách ĐANG LỌC tìm hàng mua
      // được thì ẩn đi cho khỏi vướng.
      if(daBan&&coLoc)ok=false;
      // 0 = CHƯA BIẾT (nhà chưa nêu diện tích, giá "Liên hệ"). Không biết thì
      // KHÔNG ẩn — ẩn đi là giấu mất hàng thật của khách.
      if(a>0){
        if(av==='u500'&&!(a<500))ok=false;
        if(av==='500-1000'&&!(a>=500&&a<=1000))ok=false;
        if(av==='o1000'&&!(a>1000))ok=false;
      }
      if(p>0){
        if(pv==='u0.7'&&!(p<0.7))ok=false;
        if(pv==='0.7-1'&&!(p>=0.7&&p<1))ok=false;
        if(pv==='1-2'&&!(p>=1&&p<2))ok=false;
        if(pv==='o2'&&!(p>=2))ok=false;
      }
      if(ok&&qw.length)for(var i=0;i<qw.length;i++){if(c._txt.indexOf(qw[i])===-1){ok=false;break;}}
      c.classList.toggle('an-di',!ok);
      if(ok&&!daBan)hien++;
    });
    if(so)so.textContent=hien;
    if(trong)trong.style.display=hien?'none':'block';
    if(ghiUrl!==false)try{var u=new URL(location.href);
      [['q',q.value.trim()],['dt',av],['gia',pv]].forEach(function(x){
        if(x[1])u.searchParams.set(x[0],x[1]);else u.searchParams.delete(x[0]);});
      history.replaceState(null,'',u);}catch(e){}
    if(window.gtag&&coLoc)gtag('event','loc_trang_khu',{dien_tich:av||'-',gia:pv||'-',so_lo:hien});
  }
  var t;q.addEventListener('input',function(){clearTimeout(t);t=setTimeout(chay,180);});
  ar.addEventListener('change',function(){chay();});
  pr.addEventListener('change',function(){chay();});
  if(reset)reset.addEventListener('click',function(e){e.preventDefault();q.value='';ar.value='';pr.value='';chay();});
  var sp=new URLSearchParams(location.search),co=false;
  if(sp.get('q')){q.value=sp.get('q');co=true;}
  if(sp.get('dt')){ar.value=sp.get('dt');co=true;}
  if(sp.get('gia')){pr.value=sp.get('gia');co=true;}
  if(co)chay(false);
})();
</script>
"""


def main():
    for f in sorted(glob.glob("dat-*-nam-ban/index.html")):
        s = open(f, encoding="utf-8").read()
        if '<div class="prop-grid sp-sang">' not in s:
            continue
        if "kl-box" in s:
            print("  đã có ô lọc, bỏ qua:", f)
            continue
        g = s.split('<div class="prop-grid sp-sang">')[1]
        g = g[:g.rindex("</article>")]
        the = re.findall(r'<article class="prop-card[^>]*>', g)
        con = [t for t in the if 'data-ban="1"' not in t]
        if len(the) < NGUONG:
            continue
        # thiếu data-area/data-price thì lọc sẽ ẩn nhầm -> không gắn
        thieu = [t for t in the if "data-area=" not in t or "data-price=" not in t]
        if thieu:
            print("  BỎ QUA %s — %d thẻ thiếu data-area/data-price" % (f, len(thieu)))
            continue

        i = s.index('<div class="prop-grid sp-sang">')
        s = s[:i] + HTML % {"n": len(con)} + "    " + s[i:]
        j = s.index("</head>")
        s = s[:j] + CSS + s[j:]
        k = s.rindex("</body>")
        s = s[:k] + JS + s[k:]
        open(f, "w", encoding="utf-8").write(s)
        print("  + ô lọc: %-42s %d thẻ (%d đang bán)" % (f, len(the), len(con)))


if __name__ == "__main__":
    main()
