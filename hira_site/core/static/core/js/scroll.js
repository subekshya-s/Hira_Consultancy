(function () {
     // Effect 2: staggered groups. Each child gets a slightly longer delay.
  document.querySelectorAll("[data-stagger]").forEach((group) => {
    [...group.children].forEach((child, i) => {
      child.classList.add("reveal");
      child.style.setProperty("--delay", `${i * 0.08}s`);
    });
  });
  // Effect 1: fade up. Add "visible" the first time an element enters the screen.
  const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      entry.target.classList.toggle("visible", entry.isIntersecting);
    });
  }, { threshold: 0.15, rootMargin: "0px 0px -8% 0px" });
  document.querySelectorAll(".reveal").forEach((el) => revealObserver.observe(el));

 
    // Effect 3: count up. Reads "150+" and animates 0 to 150, keeping the "+"
  function countUp(el) {
    const match = el.textContent.trim().match(/^(\D*)(\d[\d,]*)(.*)$/);
    if (!match) return;
    const [, prefix, digits, suffix] = match;
    const target = parseInt(digits.replace(/,/g, ""), 10);
    if (!target || target >= 1000 || /^[.,]\d/.test(suffix)) return;
    const start = performance.now();
    const duration = 1200;
    function tick(now) {
      const progress = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - progress, 3); // fast start, slow finish
      el.textContent = prefix + Math.round(target * eased).toLocaleString() + suffix;
      if (progress < 1) requestAnimationFrame(tick);
    }
    requestAnimationFrame(tick);
  }

  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
    const countObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          countUp(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.6 });
    document.querySelectorAll(".stat-number").forEach((el) => countObserver.observe(el));
  }
  // Effect 4: header shadow after scrolling
  const header = document.querySelector(".site-header");
  const onScroll = () => header.classList.toggle("is-scrolled", window.scrollY > 10);
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();
})();