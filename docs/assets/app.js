(() => {
  const repo = 'https://api.github.com/repos/uxillary/font-size-tweak';
  const fallbackRelease = 'https://github.com/uxillary/font-size-tweak/releases/latest';
  const setText = (id, value) => { const element = document.getElementById(id); if (element) element.textContent = value; };
  const formatDate = value => new Intl.DateTimeFormat('en', { day: 'numeric', month: 'short', year: 'numeric' }).format(new Date(value));
  const formatNumber = value => value.toLocaleString();

  fetch(repo, { headers: { Accept: 'application/vnd.github+json' } })
    .then(response => { if (!response.ok) throw new Error('Repository request failed'); return response.json(); })
    .then(repository => {
      const stars = formatNumber(repository.stargazers_count);
      setText('stars', stars);
      setText('star-cta-count', `· ${stars}`);
    })
    .catch(() => {});

  fetch(`${repo}/releases`, { headers: { Accept: 'application/vnd.github+json' } })
    .then(response => { if (!response.ok) throw new Error('Releases request failed'); return response.json(); })
    .then(releases => {
      const published = releases.filter(release => !release.draft);
      const downloads = published.reduce((total, release) => total + release.assets.reduce((releaseTotal, asset) => releaseTotal + asset.download_count, 0), 0);
      setText('downloads', formatNumber(downloads));
      if (!published.length) return;
      const latest = published.find(release => !release.prerelease) || published[0];
      setText('latest-version', latest.tag_name);
      setText('release-date', formatDate(latest.published_at));
      setText('release-title', latest.name || latest.tag_name);
      const releaseMeta = document.getElementById('release-meta');
      if (releaseMeta) releaseMeta.innerHTML = `<i class="fa-regular fa-calendar" aria-hidden="true"></i> Released ${formatDate(latest.published_at)}`;
      const asset = latest.assets.find(item => /\.exe$/i.test(item.name)) || latest.assets[0];
      const downloadUrl = asset ? asset.browser_download_url : latest.html_url;
      document.querySelectorAll('.js-latest-download').forEach(link => { link.href = downloadUrl; });
      const download = document.getElementById('release-download');
      const notes = document.getElementById('release-notes');
      if (download) download.href = downloadUrl;
      if (notes) notes.href = latest.html_url;
      const schema = document.getElementById('software-schema');
      if (schema) { const data = JSON.parse(schema.textContent); data.softwareVersion = latest.tag_name.replace(/^v/, ''); data.downloadUrl = downloadUrl; schema.textContent = JSON.stringify(data); }
      const older = published.filter(release => release.id !== latest.id).slice(0, 5);
      if (older.length) document.getElementById('previous-releases').innerHTML = older.map(release => `<article class="release"><div><h4>${escapeHtml(release.tag_name)}</h4><p><i class="fa-regular fa-calendar" aria-hidden="true"></i> ${formatDate(release.published_at)}</p></div><a href="${escapeHtml(release.html_url)}">Release &amp; download <i class="fa-solid fa-arrow-up-right-from-square" aria-hidden="true"></i></a></article>`).join('');
    }).catch(() => { document.querySelectorAll('.js-latest-download').forEach(link => { link.href = fallbackRelease; }); });

  function escapeHtml(value) { const node = document.createElement('span'); node.textContent = value; return node.innerHTML; }
})();
