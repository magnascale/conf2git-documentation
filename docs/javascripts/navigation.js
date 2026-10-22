/* Accessible progressive enhancement for Material 9.7's compact navigation. */
(() => {
  'use strict';

  const drawer = document.getElementById('__drawer');
  const sidebar = document.querySelector('.md-sidebar--primary');
  const nav = sidebar?.querySelector('.md-nav--primary');
  const label = document.querySelector('.md-header label[for="__drawer"]');
  if (!drawer || !sidebar || !nav || !label) return;

  // Keep these breakpoints aligned with navigation.css and Material.
  const compact = matchMedia('(max-width: 76.234375em)');
  const opener = document.createElement('button');
  opener.type = 'button';
  opener.className = `${label.className} conf2git-drawer-toggle`;
  opener.innerHTML = label.innerHTML;
  opener.setAttribute('aria-label', 'Open navigation');
  sidebar.id = 'conf2git-navigation';
  opener.setAttribute('aria-controls', sidebar.id);
  opener.setAttribute('aria-expanded', 'false');
  label.replaceWith(opener);

  const close = document.createElement('button');
  close.type = 'button';
  close.className = 'conf2git-drawer-close';
  close.textContent = 'Close navigation';
  nav.prepend(close);

  // Replace disclosure labels only at compact widths. Restore the original
  // elements on desktop so Material's section headings keep their semantics.
  const disclosures = [...nav.querySelectorAll('label.md-nav__link[for]')].map((original, index) => {
    const input = document.getElementById(original.htmlFor);
    const panel = input?.parentElement.querySelector(':scope > nav');
    if (!input || !panel) return null;
    const button = document.createElement('button');
    button.type = 'button';
    button.className = `${original.className} conf2git-disclosure`;
    button.innerHTML = original.innerHTML;
    if (original.id) button.id = original.id;
    button.dataset.conf2gitToggle = input.id;
    panel.id ||= `conf2git-nav-panel-${index}`;
    button.setAttribute('aria-controls', panel.id);
    if (input.id === '__toc') {
      button.setAttribute('aria-label', `Table of contents for ${original.textContent.trim()}`);
    }
    const update = () => {
      button.setAttribute('aria-expanded', String(input.checked));
      panel.setAttribute('aria-expanded', String(input.checked));
    };
    button.addEventListener('click', () => input.click());
    input.addEventListener('change', update);
    update();
    return { original, button };
  }).filter(Boolean);

  let open = false;
  let returnFocus = true;
  let lastFocused = document.activeElement;
  document.addEventListener('focusin', event => {
    if (event.target !== document.body && event.target !== document.documentElement) {
      lastFocused = event.target;
    }
  });
  const background = new Map();
  const visible = element => element.getClientRects().length > 0 &&
    getComputedStyle(element).visibility === 'visible';
  const focusable = () => [...sidebar.querySelectorAll('a[href], button, [tabindex="0"]')]
    .filter(element => !element.disabled && !element.closest('[inert]') && visible(element));

  function restoreBackground() {
    background.forEach((wasInert, element) => { element.inert = wasInert; });
    background.clear();
  }

  function isolateDrawer() {
    // Inert sibling branches, not a drawer ancestor. Leave the click-to-close
    // overlay usable, and preserve any pre-existing inert state.
    let branch = sidebar;
    while (branch.parentElement) {
      for (const sibling of branch.parentElement.children) {
        if (sibling !== branch && !sibling.matches('.md-overlay, script, style, input')) {
          background.set(sibling, sibling.inert);
          sibling.inert = true;
        }
      }
      branch = branch.parentElement;
      if (branch === document.body) break;
    }
  }

  function sync() {
    const next = compact.matches && drawer.checked;
    for (const { original, button } of disclosures) {
      if (compact.matches && original.isConnected) original.replaceWith(button);
      if (!compact.matches && button.isConnected) button.replaceWith(original);
    }
    opener.setAttribute('aria-expanded', String(next));
    sidebar.inert = compact.matches && !next;
    if (next) {
      sidebar.setAttribute('role', 'dialog');
      sidebar.setAttribute('aria-modal', 'true');
      sidebar.setAttribute('aria-label', 'Documentation navigation');
    } else {
      sidebar.removeAttribute('role');
      sidebar.removeAttribute('aria-modal');
      sidebar.removeAttribute('aria-label');
    }
    if (next && !open) {
      isolateDrawer();
      close.focus();
    } else if (!next && open) {
      restoreBackground();
      if (compact.matches && returnFocus) opener.focus();
    }
    open = next;
    returnFocus = true;
  }

  opener.addEventListener('click', () => drawer.click());
  close.addEventListener('click', () => drawer.click());
  drawer.addEventListener('change', sync);
  compact.addEventListener('change', () => {
    // CSS may hide the focused link before matchMedia dispatches its event,
    // causing the browser to move activeElement to body without a focus event.
    const previousFocus = document.activeElement === document.body
      ? lastFocused : document.activeElement;
    if (!compact.matches && drawer.checked) drawer.click();
    sync();
    if (!visible(previousFocus) || previousFocus.closest('[inert]')) {
      if (compact.matches) opener.focus();
      else (focusable()[0] || document.querySelector('.md-header .md-logo'))?.focus();
    }
  });

  document.addEventListener('keydown', event => {
    if (!open || event.ctrlKey || event.metaKey || event.altKey) return;
    // Avoid Material's global shortcuts opening another overlay behind this one.
    event.stopPropagation();
    if (event.key === 'Escape') {
      event.preventDefault();
      drawer.click();
    } else if (event.key === 'Tab') {
      const items = focusable();
      const first = items[0];
      const last = items[items.length - 1];
      if (event.shiftKey && (document.activeElement === first || !sidebar.contains(document.activeElement))) {
        event.preventDefault();
        last?.focus();
      } else if (!event.shiftKey && (document.activeElement === last || !sidebar.contains(document.activeElement))) {
        event.preventDefault();
        first?.focus();
      }
    }
  });

  nav.addEventListener('click', event => {
    const link = event.target.closest('a[href]');
    if (!open || !link || event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
    const url = new URL(link.href);
    returnFocus = false;
    drawer.click();
    // A TOC selection should put focus in the article, not back on the menu.
    if (url.pathname === location.pathname && url.hash) {
      const target = document.getElementById(decodeURIComponent(url.hash.slice(1)));
      if (target) {
        const previous = target.getAttribute('tabindex');
        target.setAttribute('tabindex', '-1');
        target.focus();
        target.addEventListener('blur', () => {
          if (previous === null) target.removeAttribute('tabindex');
          else target.setAttribute('tabindex', previous);
        }, { once: true });
      }
    }
  });

  // Only enable the off-canvas UI after every control and listener is ready.
  document.documentElement.classList.add('conf2git-drawer-ready');
  sync();
})();
