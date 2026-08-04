(function () {
  'use strict';

  const shareButtonId = 'shareResultsButton';
  const requiredMetrics = [
    'Recommended hourly rate',
    'Minimum hourly rate',
    'Annual billable hours',
    'Required pre-tax revenue'
  ];

  function getShareText() {
    const metrics = new Map(
      Array.from(document.querySelectorAll('#resultsGrid .metric')).map((metric) => [
        metric.querySelector('span')?.textContent?.trim(),
        metric.querySelector('strong')?.textContent?.trim()
      ])
    );

    const resultLines = requiredMetrics.map((label) => {
      const value = metrics.get(label);
      return value ? `${label}: ${value}` : null;
    }).filter(Boolean);

    if (resultLines.length !== requiredMetrics.length) {
      return null;
    }

    return [
      'Freelance hourly rate results',
      ...resultLines,
      `Page: ${window.location.href}`
    ].join('\n');
  }

  async function copyShareText(text) {
    if (navigator.clipboard && typeof navigator.clipboard.writeText === 'function') {
      try {
        await navigator.clipboard.writeText(text);
        return true;
      } catch {
        // Continue to the compatibility copy method.
      }
    }

    const textarea = document.createElement('textarea');
    textarea.value = text;
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

  function showShareStatus(message, success) {
    const messageElement = document.getElementById('shareStatusMessage');
    if (!messageElement) return;
    messageElement.className = `status-message share-status-message ${success ? 'success' : 'error'}`;
    messageElement.textContent = message;
  }

  function shouldUseNativeShare() {
    const mobileUserAgent = Boolean(navigator.userAgentData?.mobile) || /Android|iPhone|iPad|iPod|Mobile/i.test(navigator.userAgent);
    const coarsePointer = typeof window.matchMedia === 'function' && window.matchMedia('(pointer: coarse)').matches;
    const touchDevice = navigator.maxTouchPoints > 0 && coarsePointer;
    const compactViewport = Math.min(window.innerWidth, window.innerHeight) <= 1024;
    return mobileUserAgent || (touchDevice && compactViewport);
  }

  async function shareResults(event) {
    event.preventDefault();
    event.stopPropagation();

    const shareText = getShareText();
    if (!shareText) {
      showShareStatus('Calculate valid results before sharing.', false);
      return;
    }

    const shareData = {
      title: 'Freelance Hourly Rate Results',
      text: shareText,
      url: window.location.href
    };
    let canUseNativeShare = shouldUseNativeShare() && typeof navigator.share === 'function';

    if (canUseNativeShare && typeof navigator.canShare === 'function') {
      try {
        canUseNativeShare = navigator.canShare(shareData);
      } catch {
        canUseNativeShare = false;
      }
    }

    if (canUseNativeShare) {
      try {
        await navigator.share(shareData);
        return;
      } catch (error) {
        if (error && error.name === 'AbortError') {
          return;
        }
      }
    }

    const copied = await copyShareText(shareText);
    if (copied) {
      showShareStatus('Result copied. You can paste it to share.', true);
    } else {
      showShareStatus('Unable to copy automatically. Please copy the current page URL manually.', false);
    }
  }

  function bindShareButton() {
    const shareButton = document.getElementById(shareButtonId);
    if (!shareButton || shareButton.dataset.shareBound === 'true') return;
    shareButton.dataset.shareBound = 'true';
    shareButton.addEventListener('click', shareResults);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bindShareButton, { once: true });
  } else {
    bindShareButton();
  }
})();
