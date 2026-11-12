/* Restore focus for programmatic dialogs without overriding native Radix triggers. */
(() => {
  if (window.CodeboxdDialogFocus) return;
  window.CodeboxdDialogFocus = true;
  const selector = '[role="dialog"],[role="alertdialog"]';
  const history = [];
  const open = new Map();
  document.addEventListener('focusin', event => {
    const node = event.target;
    if (!node.matches?.('button,a[href],input,textarea,select,[tabindex]')) return;
    const index = history.indexOf(node);
    if (index >= 0) history.splice(index, 1);
    history.push(node);
    if (history.length > 32) history.shift();
  });
  function refresh() {
    for (const dialog of document.querySelectorAll(selector)) {
      if (!open.has(dialog)) {
        const opener = [...history].reverse().find(node => node.isConnected && !dialog.contains(node));
        open.set(dialog, opener);
      }
    }
    for (const [dialog, opener] of open) {
      if (dialog.isConnected) continue;
      open.delete(dialog);
      requestAnimationFrame(() => {
        if (!opener?.isConnected || opener.disabled) return;
        if (document.activeElement !== document.body && document.activeElement !== document.documentElement) return;
        const remaining = [...document.querySelectorAll(selector)];
        if (remaining.length && !remaining.some(node => node.contains(opener))) return;
        opener.focus({preventScroll: true});
      });
    }
    for (let index = history.length-1; index >= 0; index--) {
      if (!history[index].isConnected) history.splice(index, 1);
    }
  }
  new MutationObserver(refresh).observe(document.documentElement, {childList: true, subtree: true});
  refresh();
})();
