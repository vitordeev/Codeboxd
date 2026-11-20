(() => {
  if (window.CodeboxdCatalogRailDrag) return;
  window.CodeboxdCatalogRailDrag = true;

  const railSelector = '.catalog-rail';
  const dragThreshold = 8;
  let activeDrag = null;
  let suppressedClick = null;
  let suppressionTimer = 0;

  function clearSuppressedClick() {
    suppressedClick = null;
    window.clearTimeout(suppressionTimer);
    suppressionTimer = 0;
  }

  function clearActiveDrag(releaseCapture = true) {
    if (!activeDrag) return;
    const drag = activeDrag;
    activeDrag = null;
    drag.rail.classList.remove('catalog-rail--dragging');
    if (
      releaseCapture &&
      drag.rail.hasPointerCapture(drag.pointerId)
    ) {
      drag.rail.releasePointerCapture(drag.pointerId);
    }
  }

  document.addEventListener(
    'pointerdown',
    event => {
      clearSuppressedClick();
      if (
        event.pointerType !== 'mouse' ||
        event.button !== 0 ||
        !event.isPrimary
      ) {
        return;
      }

      const rail = event.target.closest?.(railSelector);
      if (!rail || rail.scrollWidth <= rail.clientWidth + 1) return;

      activeDrag = {
        rail,
        pointerId: event.pointerId,
        startX: event.clientX,
        startY: event.clientY,
        startScrollLeft: rail.scrollLeft,
        dragging: false,
        verticalIntent: false,
      };
    },
    true,
  );

  document.addEventListener(
    'pointermove',
    event => {
      const drag = activeDrag;
      if (!drag || event.pointerId !== drag.pointerId) return;
      if (!drag.rail.isConnected) {
        clearActiveDrag(false);
        return;
      }

      const deltaX = event.clientX - drag.startX;
      const deltaY = event.clientY - drag.startY;
      if (!drag.dragging && !drag.verticalIntent) {
        if (Math.max(Math.abs(deltaX), Math.abs(deltaY)) < dragThreshold) return;
        if (Math.abs(deltaX) <= Math.abs(deltaY)) {
          drag.verticalIntent = true;
          return;
        }

        drag.dragging = true;
        drag.rail.classList.add('catalog-rail--dragging');
        drag.rail.setPointerCapture(drag.pointerId);
      }

      if (drag.verticalIntent) return;
      event.preventDefault();
      drag.rail.scrollLeft = drag.startScrollLeft - deltaX;
    },
    { capture: true, passive: false },
  );

  document.addEventListener(
    'pointerup',
    event => {
      if (!activeDrag || event.pointerId !== activeDrag.pointerId) return;
      if (activeDrag.dragging || activeDrag.verticalIntent) {
        const drag = activeDrag;
        suppressedClick = { pointerId: drag.pointerId, rail: drag.rail };
        window.clearTimeout(suppressionTimer);
        suppressionTimer = window.setTimeout(clearSuppressedClick, 350);
      }
      clearActiveDrag();
    },
    true,
  );

  function cancelPointer(event) {
    if (activeDrag && event.pointerId === activeDrag.pointerId) {
      clearActiveDrag();
    }
  }

  document.addEventListener('pointercancel', cancelPointer, true);
  document.addEventListener('lostpointercapture', cancelPointer, true);
  document.addEventListener(
    'dragstart',
    event => {
      if (activeDrag?.dragging && activeDrag.rail.contains(event.target)) {
        event.preventDefault();
      }
    },
    true,
  );
  document.addEventListener(
    'click',
    event => {
      const suppressed = suppressedClick;
      if (
        !suppressed ||
        event.detail === 0 ||
        event.pointerId !== suppressed.pointerId ||
        !suppressed.rail.contains(event.target)
      ) {
        return;
      }

      event.preventDefault();
      event.stopPropagation();
      event.stopImmediatePropagation();
      clearSuppressedClick();
    },
    true,
  );

  function cancelForLifecycleChange() {
    clearActiveDrag();
    clearSuppressedClick();
  }

  window.addEventListener('blur', cancelForLifecycleChange);
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) cancelForLifecycleChange();
  });

  new MutationObserver(() => {
    if (activeDrag && !activeDrag.rail.isConnected) clearActiveDrag(false);
  }).observe(document.documentElement, { childList: true, subtree: true });
})();
