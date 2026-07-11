// Scroll'da beliren bölümler — hareket azaltma tercihine saygılı
(function () {
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var els = document.querySelectorAll(
    ".problem__card, .feature-card, .device, .app-main .card, .guide-item, .guide-program, .social-proof__line, .cta2 h2"
  );
  els.forEach(function (el, i) {
    el.classList.add("reveal");
    el.style.transitionDelay = (i % 5) * 70 + "ms";
  });
  var io = new IntersectionObserver(
    function (entries) {
      entries.forEach(function (e) {
        if (e.isIntersecting) {
          e.target.classList.add("reveal--in");
          io.unobserve(e.target);
        }
      });
    },
    { threshold: 0.12 }
  );
  els.forEach(function (el) { io.observe(el); });
})();
