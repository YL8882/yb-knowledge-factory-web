const WORKSPACE_URL = 'http://127.0.0.1:8000/';
const WORKSPACE_URL_PATTERN = 'http://127.0.0.1:8000/*';

// content.js can't reliably open/navigate a tab itself: by the time its
// fetch() to the backend resolves, the click's transient user-activation may
// have expired, so window.open() risks being blocked as a popup. The
// background service worker's chrome.tabs API isn't subject to that
// restriction.
console.log('[YB Learn][background] service worker loaded');

chrome.runtime.onMessage.addListener(function (message, sender, sendResponse) {
  console.log('[YB Learn][background] message received:', message);
  if (message && message.action === 'openWorkspace') {
    // Acknowledge receipt synchronously — content.js's callback only checks
    // chrome.runtime.lastError, it never reads the response value, so there is
    // no need to wait for openOrFocusWorkspace()'s own async tab work to
    // finish before responding. Responding here (instead of never responding)
    // is what content.js's sendMessage callback is actually waiting on; not
    // completing it is what produced "message port closed before a response
    // was received".
    sendResponse({ received: true });
    openOrFocusWorkspace(message.url);
  }
});

// Single Workspace Principle: the whole browser should only ever have one YB
// Knowledge Workspace tab open. Reuses an existing one by navigating it to
// the new ?url= instead of creating a new tab each time — only falls back to
// chrome.tabs.create() when no matching tab is found (first run, or the user
// closed the previous Workspace tab).
//
// Navigating the existing tab triggers a full page reload, which is enough
// to satisfy "update URL / clear previous state / restart Transcript+Study
// Note" on its own: script.js's autoStartFromExtension() already re-reads
// ?url= and re-triggers the pipeline on every page load — no separate
// "clear state" step or content-script messaging needed.
function openOrFocusWorkspace(capturedUrl) {
  const targetUrl = capturedUrl
    ? WORKSPACE_URL + '?url=' + encodeURIComponent(capturedUrl)
    : WORKSPACE_URL;

  chrome.tabs.query({ url: WORKSPACE_URL_PATTERN }, function (tabs) {
    if (tabs && tabs.length > 0) {
      const tab = tabs[0];
      chrome.tabs.update(tab.id, { url: targetUrl, active: true }, function () {
        if (chrome.runtime.lastError) {
          console.error('[YB Learn][background] tabs.update failed:', chrome.runtime.lastError.message);
        } else {
          console.log('[YB Learn][background] reused existing Workspace tab:', tab.id);
        }
      });
      chrome.windows.update(tab.windowId, { focused: true });
      return;
    }

    chrome.tabs.create({ url: targetUrl }, function (tab) {
      if (chrome.runtime.lastError) {
        console.error('[YB Learn][background] tabs.create failed:', chrome.runtime.lastError.message);
      } else {
        console.log('[YB Learn][background] created new Workspace tab:', tab && tab.id);
      }
    });
  });
}
