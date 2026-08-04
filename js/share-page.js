(function () {
  'use strict';

  if (window.__freelancerSharePageInitialized) return;
  window.__freelancerSharePageInitialized = true;

  const copyLinkButton = document.getElementById('copyLinkButton');
  const shareStatusMessage = document.getElementById('shareStatusMessage');
  const shareLinkText = document.getElementById('shareLinkText');
  const canonicalLink = document.querySelector('link[rel="canonical"]')?.href;
  const currentUrl = new URL(window.location.href);

  currentUrl.search = '';
  currentUrl.hash = '';

  const canonicalUrl = canonicalLink || currentUrl.href;

  function setShareStatus(message, success) {
    if (!shareStatusMessage) return;
    shareStatusMessage.className = `status-message share-status-message ${success ? 'success' : 'error'}`;
    shareStatusMessage.textContent = message;
  }

  function clearShareStatus() {
    if (!shareStatusMessage) return;
    shareStatusMessage.className = 'status-message share-status-message';
    shareStatusMessage.textContent = '';
  }

  function setManualCopyLink(visible) {
    if (!shareLinkText) return;
    shareLinkText.value = canonicalUrl;
    shareLinkText.hidden = !visible;

    if (visible) {
      shareLinkText.focus();
      shareLinkText.select();
    }
  }

  async function copyWithClipboard() {
    if (!navigator.clipboard || typeof navigator.clipboard.writeText !== 'function') return false;

    try {
      await navigator.clipboard.writeText(canonicalUrl);
      return true;
    } catch {
      return false;
    }
  }

  function copyWithTemporaryTextarea() {
    const textarea = document.createElement('textarea');
    textarea.value = canonicalUrl;
    textarea.setAttribute('readonly', '');
    textarea.setAttribute('aria-hidden', 'true');
    textarea.style.position = 'fixed';
    textarea.style.left = '-9999px';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    textarea.focus();
    textarea.select();

    try {
      return document.execCommand('copy');
    } catch {
      return false;
    } finally {
      textarea.remove();
    }
  }

  async function copyLink() {
    clearShareStatus();
    setManualCopyLink(false);

    const copied = await copyWithClipboard() || copyWithTemporaryTextarea();

    if (copied) {
      setShareStatus('Link copied.', true);
      return true;
    }

    setManualCopyLink(true);
    setShareStatus('Copy failed. Please copy the link manually.', false);
    return false;
  }

  async function handleCopyLink(event) {
    event.preventDefault();
    event.stopPropagation();
    await copyLink();
  }

  if (copyLinkButton && copyLinkButton.dataset.shareBound !== 'true') {
    copyLinkButton.dataset.shareBound = 'true';
    copyLinkButton.addEventListener('click', handleCopyLink);
  }
})();
