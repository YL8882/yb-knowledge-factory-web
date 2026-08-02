const WORKSPACE_URL = 'http://127.0.0.1:8000/';

// content.js can't reliably open a tab itself: by the time its fetch() to the
// backend resolves, the click's transient user-activation may have expired,
// so window.open() risks being blocked as a popup. chrome.tabs.create() from
// the background service worker isn't subject to that restriction.
console.log('[YB Learn][background] service worker loaded');

chrome.runtime.onMessage.addListener(function (message) {
  console.log('[YB Learn][background] message received:', message);
  if (message && message.action === 'openWorkspace') {
    const targetUrl = message.url
      ? WORKSPACE_URL + '?url=' + encodeURIComponent(message.url)
      : WORKSPACE_URL;
    chrome.tabs.create({ url: targetUrl }, function (tab) {
      if (chrome.runtime.lastError) {
        console.error('[YB Learn][background] tabs.create failed:', chrome.runtime.lastError.message);
      } else {
        console.log('[YB Learn][background] tab opened:', tab && tab.id);
      }
    });
  }
});
