/* Nam Ban Villas – Main JS */
(function () {
  'use strict';

  // ===== Header scroll =====
  const header = document.getElementById('header');
  let lastScroll = 0;
  window.addEventListener('scroll', () => {
    const s = window.scrollY;
    header.classList.toggle('scrolled', s > 10);
    lastScroll = s;
  }, { passive: true });

  // ===== Mobile menu =====
  const hamburger = document.getElementById('hamburger');
  const nav = document.getElementById('nav');
  hamburger?.addEventListener('click', () => {
    const open = hamburger.getAttribute('aria-expanded') === 'true';
    hamburger.setAttribute('aria-expanded', String(!open));
    hamburger.classList.toggle('open');
    nav.classList.toggle('open');
  });
  document.addEventListener('click', e => {
    if (nav?.classList.contains('open') && !nav.contains(e.target) && !hamburger.contains(e.target)) {
      nav.classList.remove('open');
      hamburger.classList.remove('open');
      hamburger.setAttribute('aria-expanded', 'false');
    }
  });

  // ===== Hero slideshow =====
  const slides = document.querySelectorAll('.slide');
  if (slides.length > 1) {
    let cur = 0;
    setInterval(() => {
      slides[cur].classList.remove('active');
      cur = (cur + 1) % slides.length;
      slides[cur].classList.add('active');
    }, 5000);
  }

  // ===== Search tabs =====
  document.querySelectorAll('.search-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      document.querySelectorAll('.search-tab').forEach(t => t.classList.remove('active'));
      tab.classList.add('active');
    });
  });

  // ===== Property filter =====
  const filterTabs = document.querySelectorAll('.filter-tab');
  const cards = document.querySelectorAll('.property-card');
  filterTabs.forEach(tab => {
    tab.addEventListener('click', () => {
      filterTabs.forEach(t => { t.classList.remove('active'); t.setAttribute('aria-selected', 'false'); });
      tab.classList.add('active');
      tab.setAttribute('aria-selected', 'true');
      const filter = tab.dataset.filter;
      cards.forEach(card => {
        const cats = card.dataset.category || '';
        card.classList.toggle('hidden', filter !== 'all' && !cats.includes(filter));
      });
    });
  });

  // ===== Testimonials slider =====
  const track = document.querySelector('.testimonial-track');
  const dots = document.querySelectorAll('.dot');
  const prevBtn = document.querySelector('.slider-btn.prev');
  const nextBtn = document.querySelector('.slider-btn.next');
  if (track) {
    let idx = 0;
    const cards = track.querySelectorAll('.testimonial-card');
    const total = cards.length;
    const perView = () => window.innerWidth < 768 ? 1 : window.innerWidth < 1024 ? 2 : 3;
    const maxIdx = () => Math.max(0, total - perView());

    const go = (n) => {
      idx = Math.max(0, Math.min(n, maxIdx()));
      const w = cards[0].offsetWidth + 24;
      track.style.transform = `translateX(-${idx * w}px)`;
      dots.forEach((d, i) => d.classList.toggle('active', i === idx));
    };
    prevBtn?.addEventListener('click', () => go(idx - 1));
    nextBtn?.addEventListener('click', () => go(idx + 1));
    dots.forEach((d, i) => d.addEventListener('click', () => go(i)));
    window.addEventListener('resize', () => go(Math.min(idx, maxIdx())));

    // Auto play
    let autoSlide = setInterval(() => go(idx < maxIdx() ? idx + 1 : 0), 5000);
    track.addEventListener('mouseenter', () => clearInterval(autoSlide));
    track.addEventListener('mouseleave', () => { autoSlide = setInterval(() => go(idx < maxIdx() ? idx + 1 : 0), 5000); });
  }

  // ===== Scroll to top =====
  const scrollBtn = document.getElementById('scrollTop');
  window.addEventListener('scroll', () => {
    scrollBtn && (scrollBtn.style.display = window.scrollY > 400 ? 'flex' : 'none');
  }, { passive: true });
  scrollBtn?.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

  // ===== Lead Modal =====
  const modal = document.getElementById('leadModal');
  const modalClose = document.getElementById('modalClose');
  const openModal = () => { modal.removeAttribute('hidden'); document.body.style.overflow = 'hidden'; };
  const closeModal = () => { modal.setAttribute('hidden', ''); document.body.style.overflow = ''; };

  modalClose?.addEventListener('click', closeModal);
  modal?.addEventListener('click', e => { if (e.target === modal) closeModal(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

  // Open modal after 30s if not interacted
  let hasInteracted = false;
  ['click', 'scroll', 'touchstart'].forEach(ev => {
    window.addEventListener(ev, () => { hasInteracted = true; }, { once: true, passive: true });
  });
  setTimeout(() => { if (!hasInteracted && modal) openModal(); }, 30000);

  // Open modal on CTA buttons tagged with data-modal
  document.querySelectorAll('[data-modal="lead"]').forEach(btn => btn.addEventListener('click', openModal));

  // Lead form submit
  const leadForm = document.getElementById('leadForm');
  leadForm?.addEventListener('submit', e => {
    e.preventDefault();
    const btn = leadForm.querySelector('[type="submit"]');
    btn.textContent = '✓ Đã gửi! Chúng tôi sẽ liên hệ sớm.';
    btn.style.background = '#16a34a';
    setTimeout(closeModal, 2000);
  });

  // ===== Newsletter =====
  document.querySelector('.newsletter-form')?.addEventListener('submit', e => {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    btn.textContent = '✓ Đăng ký thành công!';
    btn.style.background = '#16a34a';
  });

  // ===== Animate on scroll (Intersection Observer) =====
  const animEls = document.querySelectorAll('.property-card, .reason-card, .news-item, .testimonial-card, .market-card');
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.animation = 'fadeInUp .5s ease forwards';
          obs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
    animEls.forEach((el, i) => {
      el.style.opacity = '0';
      el.style.animationDelay = `${(i % 4) * 0.08}s`;
      obs.observe(el);
    });
  }

  // Inject animation keyframe
  const style = document.createElement('style');
  style.textContent = '@keyframes fadeInUp{from{opacity:0;transform:translateY(20px)}to{opacity:1;transform:translateY(0)}}';
  document.head.appendChild(style);

  // ===== Market stat bar animation =====
  const statBars = document.querySelectorAll('.market-stat-fill');
  if ('IntersectionObserver' in window && statBars.length) {
    const barObs = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.style.width = entry.target.style.width; // trigger repaint
          barObs.unobserve(entry.target);
        }
      });
    }, { threshold: 0.5 });
    statBars.forEach(bar => {
      const w = bar.style.width;
      bar.style.width = '0';
      barObs.observe(bar);
      setTimeout(() => { bar.style.width = w; }, 200);
    });
  }

  // ===== Sticky property save =====
  document.querySelectorAll('.property-save').forEach(btn => {
    btn.addEventListener('click', function () {
      const saved = this.classList.toggle('saved');
      this.style.color = saved ? '#ef4444' : '';
      this.querySelector('svg path').setAttribute('fill', saved ? '#ef4444' : 'none');
    });
  });

})();
