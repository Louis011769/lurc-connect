// Loughborough URC, site JS (no dependencies, no build step)

// 1) Mobile navigation toggle
(function () {
  var toggle = document.querySelector('.nav-toggle');
  var links = document.getElementById('nav-links');
  if (toggle && links) {
    toggle.addEventListener('click', function () {
      var open = links.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
    });
    links.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () {
        links.classList.remove('open');
        toggle.setAttribute('aria-expanded', 'false');
      });
    });
  }
})();

// 2) Subtle header shadow once you scroll past the top
(function () {
  var header = document.querySelector('.site-header');
  if (!header) return;
  var onScroll = function () { header.classList.toggle('scrolled', window.scrollY > 8); };
  onScroll();
  window.addEventListener('scroll', onScroll, { passive: true });
})();

// 3) Gentle reveal-on-scroll (respects reduced-motion)
(function () {
  var items = Array.prototype.slice.call(document.querySelectorAll('.reveal'));
  if (!items.length) return;
  var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (reduce || !('IntersectionObserver' in window)) {
    items.forEach(function (el) { el.classList.add('in'); });
    return;
  }
  var io = new IntersectionObserver(function (entries, obs) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        var el = entry.target;
        // small stagger between siblings revealing together
        var sibs = Array.prototype.slice.call(el.parentNode.querySelectorAll(':scope > .reveal'));
        var idx = sibs.indexOf(el);
        el.style.transitionDelay = (idx > 0 ? Math.min(idx, 4) * 80 : 0) + 'ms';
        el.classList.add('in');
        obs.unobserve(el);
      }
    });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.08 });
  items.forEach(function (el) { io.observe(el); });
})();
