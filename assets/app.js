(function () {
  const root = document.documentElement;
  const toggle = document.querySelector('.theme-toggle');
  if (!toggle) return;
  const labelEl = toggle.querySelector('.theme-toggle__label');
  const prefersDark = typeof window.matchMedia === 'function' && window.matchMedia('(prefers-color-scheme: dark)').matches;
  let storedTheme = null;
  try {
    storedTheme = localStorage.getItem('fst-theme');
  } catch (error) {
    storedTheme = null;
  }

  function applyTheme(theme) {
    if (theme === 'dark') {
      root.dataset.theme = 'dark';
    } else {
      delete root.dataset.theme;
      theme = 'light';
    }
    const readable = theme === 'dark' ? 'Dark theme' : 'Light theme';
    if (labelEl) labelEl.textContent = readable;
    toggle.setAttribute('aria-label', `Toggle colour theme (current: ${readable})`);
    toggle.setAttribute('aria-pressed', theme === 'dark');
  }

  applyTheme(storedTheme || (prefersDark ? 'dark' : 'light'));

  toggle.addEventListener('click', () => {
    const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try {
      localStorage.setItem('fst-theme', next);
    } catch (error) {
      /* ignore */
    }
    applyTheme(next);
  });

  const yearEl = document.getElementById('year');
  if (yearEl) {
    yearEl.textContent = new Date().getFullYear();
  }

  const reduceMotionQuery = typeof window.matchMedia === 'function' ? window.matchMedia('(prefers-reduced-motion: reduce)') : { matches: false };
  if (!reduceMotionQuery.matches && 'scrollBehavior' in document.documentElement.style) {
    document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
      anchor.addEventListener('click', (event) => {
        const targetId = anchor.getAttribute('href').slice(1);
        if (!targetId) return;
        const target = document.getElementById(targetId);
        if (!target) return;
        event.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      });
    });
  }
})();
