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

    // Hero album: move "is-active" to the next slide every 6 seconds
  const slides = document.querySelectorAll(".hero-slides .slide");
  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  if (slides.length > 1 && !reduceMotion) {
    let current = 0;
    setInterval(() => {
      slides[current].classList.remove("is-active");
      current = (current + 1) % slides.length;
      slides[current].classList.add("is-active");
    }, 6000);
  }
    // About tabs: Vision / Mission / Objectives / Strategy
  document.querySelectorAll("[data-about-tabs]").forEach((box) => {
    const tabs = box.querySelectorAll("[role='tab']");
    const panels = box.querySelectorAll("[role='tabpanel']");
    function show(i) {
      tabs.forEach((t, n) => {
        t.classList.toggle("is-active", n === i);
        t.setAttribute("aria-selected", n === i ? "true" : "false");
      });
      panels.forEach((p, n) => p.classList.toggle("is-active", n === i));
    }
    tabs.forEach((t, i) => t.addEventListener("click", () => show(i)));
    show(0);
  });
   // About slideshow: Vision / Mission / Objectives / Strategy
  document.querySelectorAll("[data-about-slider]").forEach((box) => {
    const track = box.querySelector(".about-track");
    const slides = box.querySelectorAll(".about-slide");
    const dotsBox = box.querySelector(".about-dots");
    const count = box.querySelector(".about-count");
    const prev = box.querySelector(".about-arrow.prev");
    const next = box.querySelector(".about-arrow.next");
    let index = 0;

    slides.forEach((_, i) => {
      const d = document.createElement("button");
      d.type = "button";
      d.className = "about-dot";
      d.setAttribute("aria-label", "Go to slide " + (i + 1));
      d.addEventListener("click", () => goTo(i));
      dotsBox.appendChild(d);
    });
    const dots = dotsBox.querySelectorAll(".about-dot");

    function fitHeight() {
      track.style.height = slides[index].offsetHeight + "px";
    }
    function goTo(i) {
      index = (i + slides.length) % slides.length;
      track.scrollTo({ left: track.clientWidth * index, behavior: "smooth" });
      fitHeight();
    }
    function update() {
      index = Math.round(track.scrollLeft / track.clientWidth);
      dots.forEach((d, n) => d.classList.toggle("is-active", n === index));
      count.textContent = (index + 1) + " / " + slides.length;
      fitHeight();
    }

    prev.addEventListener("click", () => goTo(index - 1));
    next.addEventListener("click", () => goTo(index + 1));
    track.addEventListener("scroll", () => requestAnimationFrame(update), { passive: true });
    window.addEventListener("resize", () => goTo(index));
    window.addEventListener("load", update);
    update();
  });
    // About team photo slideshow: soft fade every 5 seconds
  document.querySelectorAll("[data-photo-slider]").forEach((box) => {
    const slides = box.querySelectorAll(".about-photo__slide");
    if (slides.length < 2) return;
    const dotsBox = box.querySelector(".about-photo__dots");
    let index = 0, timer;

    const dots = [...slides].map((_, i) => {
      const d = document.createElement("button");
      d.type = "button";
      d.className = "about-photo__dot";
      d.setAttribute("aria-label", "Show photo " + (i + 1));
      d.addEventListener("click", () => { show(i); restart(); });
      dotsBox.appendChild(d);
      return d;
    });

    function show(i) {
      slides[index].classList.remove("is-active");
      dots[index].classList.remove("is-active");
      index = (i + slides.length) % slides.length;
      slides[index].classList.add("is-active");
      dots[index].classList.add("is-active");
    }
    function start() {
      if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
      timer = setInterval(() => show(index + 1), 5000);
    }
    function restart() { clearInterval(timer); start(); }

    box.addEventListener("mouseenter", () => clearInterval(timer));
    box.addEventListener("mouseleave", restart);
    dots[0].classList.add("is-active");
    start();
  });
})();