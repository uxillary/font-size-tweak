(() => {
  const results = {
    text: {
      title: 'Windows Text size', target: 'Text throughout Windows', setting: 'Windows Text size', location: 'Settings',
      copy: 'If text across Windows is hard to read, try the built-in text-size control first. In Windows 11, open Settings → Accessibility → Text size, adjust the slider and select Apply. Apps and components can respond differently.',
      links: [['/font-size-tweak/guides/text-size-vs-display-scaling/', 'Compare Text size and display scaling']]
    },
    everything: {
      title: 'Windows Display scaling', target: 'Everything on the screen', setting: 'Display → Scale', location: 'Settings → System → Display',
      copy: 'When controls, spacing and text all feel too small, Windows Display scaling is designed to enlarge more of the interface together. Choose the scale that suits your display and check the apps you use.',
      links: [['/font-size-tweak/guides/text-size-vs-display-scaling/', 'Compare Text size and display scaling']]
    },
    files: {
      title: 'Try Windows Text size first', target: 'File and folder names', setting: 'Text size; then Icons metric if needed', location: 'Settings or Font Size Tweak',
      copy: 'Start with Windows 11 Settings → Accessibility → Text size. If supported classic File Explorer labels still need a more targeted adjustment, Font Size Tweak’s Icons metric may affect them. It changes label text, not icon graphics, and results vary by component/build.',
      links: [['/font-size-tweak/guides/file-explorer-text-size/', 'File Explorer text-size guide'], ['/font-size-tweak/guides/font-size-tweak-vs-advanced-system-font-changer/', 'Compare font-size tools'], ['https://github.com/uxillary/font-size-tweak/releases/latest', 'Free download']]
    },
    icons: {
      title: 'Try Windows Text size first', target: 'Desktop icon labels', setting: 'Text size; then Icons metric if needed', location: 'Settings or Font Size Tweak',
      copy: 'Windows Text size is a useful first step. For supported classic desktop icon labels, Font Size Tweak’s Icons metric may offer a targeted adjustment. It changes label text, not the icon pictures themselves.',
      links: [['/font-size-tweak/guides/file-explorer-text-size/', 'How the Icons metric works'], ['/font-size-tweak/guides/font-size-tweak-vs-advanced-system-font-changer/', 'Compare font-size tools'], ['https://github.com/uxillary/font-size-tweak/releases/latest', 'Free download']]
    },
    menus: {
      title: 'Try Windows Text size first', target: 'Menus', setting: 'Text size; then Menus metric if needed', location: 'Settings or Font Size Tweak',
      copy: 'Try Windows Text size for a broad adjustment. Font Size Tweak’s Menus metric is for supported classic menu text; modern or custom-drawn menus may use another rendering system.',
      links: [['/font-size-tweak/guides/text-size-vs-display-scaling/', 'Compare Windows sizing options'], ['/font-size-tweak/guides/font-size-tweak-vs-advanced-system-font-changer/', 'Compare font-size tools'], ['https://github.com/uxillary/font-size-tweak/releases/latest', 'Free download']]
    },
    title: {
      title: 'Try Windows Text size first', target: 'Window title text', setting: 'Text size; then Title Bar metric if needed', location: 'Settings or Font Size Tweak',
      copy: 'Windows Text size is a sensible first try. Font Size Tweak’s Title Bar metric can adjust supported classic window caption text, though newer windows and apps may not use that metric.',
      links: [['/font-size-tweak/guides/text-size-vs-display-scaling/', 'Compare Windows sizing options'], ['/font-size-tweak/guides/font-size-tweak-vs-advanced-system-font-changer/', 'Compare font-size tools'], ['https://github.com/uxillary/font-size-tweak/releases/latest', 'Free download']]
    },
    messages: {
      title: 'Try Windows Text size first', target: 'Dialog or message text', setting: 'Text size; then Message Boxes metric if needed', location: 'Settings or Font Size Tweak',
      copy: 'Try Windows Text size first. Font Size Tweak’s Message Boxes metric applies to some classic dialogs and prompts; application-specific or modern dialogs may not respond.',
      links: [['/font-size-tweak/guides/windows-font-size-changes-not-appearing/', 'Why a change may not appear'], ['/font-size-tweak/guides/font-size-tweak-vs-advanced-system-font-changer/', 'Compare font-size tools'], ['https://github.com/uxillary/font-size-tweak/releases/latest', 'Free download']]
    },
    status: {
      title: 'Font Size Tweak — Status Bar metric', target: 'Status bar text', setting: 'Status Bar metric', location: 'Font Size Tweak',
      copy: 'For a status bar in a compatible legacy interface, Font Size Tweak’s Status Bar metric may help. Many apps either have no status bar or draw it using a different system, so check the interface you care about.',
      links: [['/font-size-tweak/guides/windows-font-size-changes-not-appearing/', 'Compatibility and refresh notes'], ['/font-size-tweak/guides/font-size-tweak-vs-advanced-system-font-changer/', 'Compare font-size tools'], ['https://github.com/uxillary/font-size-tweak/releases/latest', 'Free download']]
    },
    unsure: {
      title: 'Start with Windows Text size', target: 'Not sure yet', setting: 'Windows Text size', location: 'Settings → Accessibility',
      copy: 'Begin with the built-in Text size setting and see what changes. If the whole interface also feels too small, try Display scaling. If a particular classic text category remains uncomfortable, check whether it has a supported metric.',
      links: [['/font-size-tweak/guides/text-size-vs-display-scaling/', 'Compare Text size and display scaling']]
    }
  };
  const fields = ['title', 'copy', 'target', 'setting', 'location'];
  const result = document.getElementById('decision-result');
  document.querySelectorAll('input[name="sizing-goal"]').forEach(input => {
    input.addEventListener('change', () => {
      const choice = results[input.value];
      if (!choice) return;
      fields.forEach(key => {
        const element = document.getElementById(`result-${key}`);
        if (element) element.textContent = choice[key];
      });
      const links = document.getElementById('result-links');
      links.replaceChildren(...choice.links.map(([href, label]) => {
        const anchor = document.createElement('a');
        anchor.href = href;
        anchor.textContent = label;
        return anchor;
      }));
      result.focus({ preventScroll: true });
    });
  });
})();
