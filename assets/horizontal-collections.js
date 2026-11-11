/* Codeboxd horizontal collections: native touch, local mouse/keyboard behavior. */
(() => {
  if (window.CodeboxdRails) {
    window.CodeboxdRails.refresh();
    return;
  }
  const selector = '[data-codeboxd-rail]';
  const rails = new Set();
  let active = null;
  let suppressed = null;
  let frame = 0;
  const reduced = () => matchMedia('(prefers-reduced-motion: reduce)').matches;

  function update() {
    frame = 0;
    for (const rail of rails) {
      if (!rail.isConnected) {
        if (active?.rail === rail) finish(false);
        rails.delete(rail);
        resize.unobserve(rail);
        continue;
      }
      const maximum = Math.max(0, rail.scrollWidth - rail.clientWidth);
      for (const control of document.querySelectorAll('[data-rail-direction]')) {
        if (control.getAttribute('aria-controls') !== rail.id) continue;
        const previous = control.dataset.railDirection === '-1';
        const disabled = maximum <= 1 || (previous ? rail.scrollLeft <= 1 : rail.scrollLeft >= maximum - 1);
        if (disabled && document.activeElement === control) rail.focus({preventScroll: true});
        control.disabled = disabled;
      }
    }
  }
  function schedule() {
    if (!frame) frame = requestAnimationFrame(update);
  }
  const resize = new ResizeObserver(schedule);
  function refresh() {
    for (const rail of document.querySelectorAll(selector)) {
      if (!rails.has(rail)) {
        rails.add(rail);
        resize.observe(rail);
      }
    }
    schedule();
  }
  function move(rail, left) {
    rail.scrollTo({left, behavior: reduced() ? 'instant' : 'smooth'});
  }
  function finish(suppressClick) {
    const drag = active;
    if (!drag) return;
    active = null;
    delete drag.rail.dataset.dragging;
    suppressed = suppressClick && drag.dragged
      ? {rail: drag.rail, pointerId: drag.pointerId, until: performance.now() + 350} : null;
    if (drag.rail.hasPointerCapture(drag.pointerId)) drag.rail.releasePointerCapture(drag.pointerId);
    schedule();
  }

  document.addEventListener('pointerdown', event => {
    suppressed = null; // A fresh click must never be swallowed by an old drag.
    if (event.pointerType !== 'mouse' || !event.isPrimary || event.button !== 0
        || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    const rail = event.target.closest(selector);
    if (!rail || rail.scrollWidth <= rail.clientWidth + 1) return;
    const control = event.target.closest('button,a,input,select,textarea,[contenteditable]');
    if (control && !control.matches('[data-rail-item]')) return;
    active = {rail, pointerId: event.pointerId, x: event.clientX, y: event.clientY,
              left: rail.scrollLeft, dragged: false};
  }, true);

  document.addEventListener('pointermove', event => {
    const drag = active;
    if (!drag || drag.pointerId !== event.pointerId) return;
    if (!(event.buttons & 1)) return finish(false);
    const dx = event.clientX - drag.x;
    const dy = event.clientY - drag.y;
    if (!drag.dragged) {
      if (Math.abs(dy) >= 8 && Math.abs(dy) >= Math.abs(dx)) return finish(false);
      if (Math.abs(dx) < 8 || Math.abs(dx) <= Math.abs(dy)) return;
      drag.dragged = true;
      drag.rail.dataset.dragging = 'true';
      drag.rail.setPointerCapture(event.pointerId);
      const selection = getSelection();
      if (selection?.anchorNode && drag.rail.contains(selection.anchorNode)) selection.removeAllRanges();
    }
    event.preventDefault();
    drag.rail.scrollLeft = drag.left - dx;
  }, {capture: true, passive: false});

  document.addEventListener('pointerup', event => {
    if (active?.pointerId === event.pointerId) finish(true);
  }, true);
  for (const type of ['pointercancel', 'lostpointercapture']) {
    document.addEventListener(type, event => {
      if (active?.pointerId === event.pointerId) finish(false);
    }, true);
  }
  window.addEventListener('blur', () => finish(false));
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) finish(false);
  });
  document.addEventListener('dragstart', event => {
    if (event.target.closest(selector)) event.preventDefault();
  }, true);
  document.addEventListener('click', event => {
    if (suppressed && event.detail > 0 && performance.now() <= suppressed.until
        && event.target.closest(selector) === suppressed.rail
        && (event.pointerId === undefined || event.pointerId === suppressed.pointerId)) {
      suppressed = null;
      event.preventDefault();
      event.stopImmediatePropagation();
      return;
    }
    const control = event.target.closest('[data-rail-direction]');
    if (!control || control.disabled) return;
    const rail = document.getElementById(control.getAttribute('aria-controls'));
    if (rail?.matches(selector)) move(rail, rail.scrollLeft + rail.clientWidth * .85 * Number(control.dataset.railDirection));
  }, true);
  document.addEventListener('keydown', event => {
    const rail = event.target;
    if (!rail.matches(selector) || event.altKey || event.ctrlKey || event.metaKey || event.shiftKey) return;
    const maximum = Math.max(0, rail.scrollWidth - rail.clientWidth);
    const positions = {ArrowLeft: rail.scrollLeft - rail.clientWidth * .85,
                       ArrowRight: rail.scrollLeft + rail.clientWidth * .85, Home: 0, End: maximum};
    if (Object.hasOwn(positions, event.key)) {
      event.preventDefault();
      move(rail, positions[event.key]);
    }
  });
  document.addEventListener('focusin', event => {
    const item = event.target.closest('[data-rail-item]');
    const rail = item?.closest(selector);
    if (!rail || active?.dragged) return;
    const area = rail.getBoundingClientRect(), box = item.getBoundingClientRect();
    const delta = box.left < area.left ? box.left - area.left : box.right > area.right ? box.right - area.right : 0;
    if (delta) rail.scrollLeft += delta;
  });
  document.addEventListener('scroll', event => {
    if (event.target.matches?.(selector)) schedule();
  }, {capture: true, passive: true});
  new MutationObserver(refresh).observe(document.documentElement, {childList: true, subtree: true});
  window.CodeboxdRails = {refresh};
  refresh();
})();
