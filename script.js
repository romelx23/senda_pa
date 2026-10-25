(() => {
  const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  // Reveal sections as they enter the viewport.
  const revealItems = document.querySelectorAll("[data-reveal]");
  if ("IntersectionObserver" in window && !reducedMotion) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { rootMargin: "0px 0px -8% 0px", threshold: 0.12 }
    );
    revealItems.forEach((item) => observer.observe(item));
  } else {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }

  // Keep the page readable if a section was never observed (print, snapshots,
  // or a browser that interrupts the observer while images are loading).
  window.setTimeout(() => {
    revealItems.forEach((item) => item.classList.add("is-visible"));
  }, 3200);

  // Gallery: buttons, drag-to-scroll and click-to-enlarge.
  const track = document.querySelector("[data-gallery-track]");
  if (track) {
    const prev = document.querySelector("[data-gallery-prev]");
    const next = document.querySelector("[data-gallery-next]");
    const shots = Array.from(track.querySelectorAll(".shot"));

    const step = () => {
      const first = shots[0];
      if (!first) return 240;
      const gap = parseFloat(getComputedStyle(track).columnGap || "24") || 24;
      return first.getBoundingClientRect().width + gap;
    };

    const updateButtons = () => {
      const max = track.scrollWidth - track.clientWidth - 2;
      if (prev) prev.disabled = track.scrollLeft <= 2;
      if (next) next.disabled = track.scrollLeft >= max;
    };

    const scrollGallery = (direction) => {
      track.scrollBy({
        left: direction * step(),
        behavior: reducedMotion ? "auto" : "smooth",
      });
    };

    prev?.addEventListener("click", () => scrollGallery(-1));
    next?.addEventListener("click", () => scrollGallery(1));
    track.addEventListener("scroll", updateButtons, { passive: true });
    window.addEventListener("resize", updateButtons, { passive: true });
    updateButtons();

    track.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") {
        event.preventDefault();
        scrollGallery(-1);
      }
      if (event.key === "ArrowRight") {
        event.preventDefault();
        scrollGallery(1);
      }
    });

    let down = false;
    let startX = 0;
    let startScroll = 0;
    let moved = false;

    track.addEventListener("pointerdown", (event) => {
      if (event.pointerType === "touch" || event.button !== 0) return;
      down = true;
      moved = false;
      startX = event.clientX;
      startScroll = track.scrollLeft;
    });

    track.addEventListener("pointermove", (event) => {
      if (!down) return;
      const distance = event.clientX - startX;
      if (Math.abs(distance) > 6) {
        if (!moved) {
          moved = true;
          // Capture only after a real drag starts. Capturing on pointerdown
          // retargets the click away from the link and breaks the lightbox.
          track.setPointerCapture(event.pointerId);
        }
        track.scrollLeft = startScroll - distance;
        event.preventDefault();
      }
    });

    const endDrag = (event) => {
      if (!down) return;
      down = false;
      if (track.hasPointerCapture(event.pointerId)) {
        track.releasePointerCapture(event.pointerId);
      }
      if (moved) {
        track.dataset.dragged = "true";
        window.setTimeout(() => {
          delete track.dataset.dragged;
        }, 50);
      }
    };

    track.addEventListener("pointerup", endDrag);
    track.addEventListener("pointercancel", endDrag);

    track.addEventListener(
      "click",
      (event) => {
        if (track.dataset.dragged === "true") {
          event.preventDefault();
          event.stopPropagation();
        }
      },
      true
    );

    const dialog = document.getElementById("lightbox");
    if (dialog instanceof HTMLDialogElement) {
      const dialogImage = dialog.querySelector("img");
      const dialogCaption = document.getElementById("lightbox-caption");
      const closeButton = dialog.querySelector("[data-lightbox-close]");
      let lastTrigger = null;

      const closeDialog = () => {
        if (dialog.open) dialog.close();
      };

      track.querySelectorAll("[data-lightbox]").forEach((link) => {
        link.addEventListener("click", (event) => {
          if (track.dataset.dragged === "true") {
            event.preventDefault();
            return;
          }
          const image = link.querySelector("img");
          if (!image || !dialogImage || !dialogCaption) return;
          event.preventDefault();
          lastTrigger = link;
          dialogImage.src = link.getAttribute("href") || image.currentSrc;
          dialogImage.alt = image.alt;
          dialogCaption.textContent = link.dataset.caption || "";
          if (!dialog.open) {
            dialog.showModal();
            document.body.style.overflow = "hidden";
          }
        });
      });

      closeButton?.addEventListener("click", closeDialog);

      dialog.addEventListener("click", (event) => {
        if (event.target === dialog) closeDialog();
      });

      dialog.addEventListener("close", () => {
        document.body.style.overflow = "";
        if (dialogImage) {
          dialogImage.removeAttribute("src");
          dialogImage.alt = "";
        }
        lastTrigger?.focus();
        lastTrigger = null;
      });
    }
  }
})();
