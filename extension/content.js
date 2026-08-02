(function () {
  const BUTTON_ID = 'yb-learn-button';
  const TOAST_ID = 'yb-learn-toast';
  const API_BASE_URL = 'http://127.0.0.1:8000';

  function isWatchPage() {
    return location.pathname === '/watch';
  }

  async function onButtonClick() {
    const url = location.href;
    console.log('[YB Learn] Captured URL:', url);

    const button = document.getElementById(BUTTON_ID);
    if (button) {
      button.disabled = true;
    }

    try {
      const response = await fetch(API_BASE_URL + '/api/capture', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ url: url }),
      });

      if (!response.ok) {
        throw new Error('HTTP ' + response.status);
      }

      const data = await response.json();
      console.log('[YB Learn] Backend response:', data);
      showToast('✓ 已送出至 YB 知識工廠：' + url);
    } catch (error) {
      console.error('[YB Learn] Failed to reach backend:', error);
      showToast('✗ 無法連線到後端，請確認伺服器已啟動');
    } finally {
      if (button) {
        button.disabled = false;
      }
    }
  }

  function createButton() {
    if (document.getElementById(BUTTON_ID)) {
      return;
    }
    const button = document.createElement('button');
    button.id = BUTTON_ID;
    button.type = 'button';
    button.textContent = '▶ YB Learn';
    button.addEventListener('click', onButtonClick);
    document.body.appendChild(button);
  }

  function removeButton() {
    const button = document.getElementById(BUTTON_ID);
    if (button) {
      button.remove();
    }
  }

  function showToast(message) {
    const existing = document.getElementById(TOAST_ID);
    if (existing) {
      existing.remove();
    }
    const toast = document.createElement('div');
    toast.id = TOAST_ID;
    toast.textContent = message;
    document.body.appendChild(toast);
    setTimeout(function () {
      toast.remove();
    }, 2500);
  }

  // YouTube is a single-page app — moving between a watch page and any other
  // page (home, search, another watch page) doesn't reload the document, so
  // the button has to be shown/hidden on YouTube's own SPA navigation event
  // instead of only once at content-script load time.
  function syncButtonVisibility() {
    if (isWatchPage()) {
      createButton();
    } else {
      removeButton();
    }
  }

  syncButtonVisibility();
  document.addEventListener('yt-navigate-finish', syncButtonVisibility);
})();
