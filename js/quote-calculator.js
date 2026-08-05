(function () {
  'use strict';

  if (window.__freelancerQuoteCalculatorInitialized) return;
  window.__freelancerQuoteCalculatorInitialized = true;

  const form = document.getElementById('quoteCalculatorForm');
  const errorSummary = document.getElementById('quoteErrorSummary');
  const statusMessage = document.getElementById('quoteStatusMessage');
  const resultsContainer = document.getElementById('quoteResults');
  const zeroQuoteMessage = document.getElementById('zeroQuoteMessage');

  if (!form || !errorSummary || !statusMessage || !resultsContainer || !zeroQuoteMessage) return;

  const fields = {
    estimatedProjectHours: document.getElementById('estimatedProjectHours'),
    quoteHourlyRate: document.getElementById('quoteHourlyRate'),
    directProjectExpenses: document.getElementById('directProjectExpenses'),
    contingencyBufferPercentage: document.getElementById('contingencyBufferPercentage'),
    clientDiscountPercentage: document.getElementById('clientDiscountPercentage')
  };

  function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  }

  function errorElement(fieldName) {
    return document.getElementById(`${fieldName}Error`);
  }

  function clearFieldError(fieldName) {
    const field = fields[fieldName];
    const message = errorElement(fieldName);
    if (field) field.removeAttribute('aria-invalid');
    if (message) message.textContent = '';
  }

  function showFieldError(fieldName, message) {
    const field = fields[fieldName];
    const messageElement = errorElement(fieldName);
    if (field) field.setAttribute('aria-invalid', 'true');
    if (messageElement) messageElement.textContent = message;
  }

  function clearErrors() {
    Object.keys(fields).forEach(clearFieldError);
    errorSummary.textContent = '';
    errorSummary.hidden = true;
  }

  function hideResults(message) {
    resultsContainer.replaceChildren();
    resultsContainer.hidden = true;
    zeroQuoteMessage.textContent = '';
    zeroQuoteMessage.hidden = true;
    statusMessage.className = 'status-message';
    statusMessage.textContent = message;
  }

  function readNumber(fieldName) {
    const rawValue = fields[fieldName]?.value.trim() || '';
    return rawValue === '' ? null : Number(rawValue);
  }

  function validateInputs() {
    clearErrors();
    const values = {
      estimatedProjectHours: readNumber('estimatedProjectHours'),
      quoteHourlyRate: readNumber('quoteHourlyRate'),
      directProjectExpenses: readNumber('directProjectExpenses'),
      contingencyBufferPercentage: readNumber('contingencyBufferPercentage'),
      clientDiscountPercentage: readNumber('clientDiscountPercentage')
    };
    const errors = [];

    if (values.estimatedProjectHours === null || !Number.isFinite(values.estimatedProjectHours)) {
      errors.push(['estimatedProjectHours', 'Enter the estimated project hours.']);
    } else if (values.estimatedProjectHours <= 0) {
      errors.push(['estimatedProjectHours', 'Estimated project hours must be greater than 0.']);
    } else if (values.estimatedProjectHours > 10000) {
      errors.push(['estimatedProjectHours', 'Estimated project hours cannot exceed 10,000.']);
    }

    if (values.quoteHourlyRate === null || !Number.isFinite(values.quoteHourlyRate)) {
      errors.push(['quoteHourlyRate', 'Enter your hourly rate.']);
    } else if (values.quoteHourlyRate <= 0) {
      errors.push(['quoteHourlyRate', 'Hourly rate must be greater than 0.']);
    }

    if (values.directProjectExpenses === null || !Number.isFinite(values.directProjectExpenses)) {
      errors.push(['directProjectExpenses', 'Enter direct project expenses, using 0 if there are none.']);
    } else if (values.directProjectExpenses < 0) {
      errors.push(['directProjectExpenses', 'Direct project expenses cannot be negative.']);
    }

    if (values.contingencyBufferPercentage === null || !Number.isFinite(values.contingencyBufferPercentage)) {
      errors.push(['contingencyBufferPercentage', 'Enter a contingency buffer, using 0 if none is needed.']);
    } else if (values.contingencyBufferPercentage < 0 || values.contingencyBufferPercentage > 100) {
      errors.push(['contingencyBufferPercentage', 'Contingency buffer must be between 0% and 100%.']);
    }

    if (values.clientDiscountPercentage === null || !Number.isFinite(values.clientDiscountPercentage)) {
      errors.push(['clientDiscountPercentage', 'Enter a client discount, using 0 for no discount.']);
    } else if (values.clientDiscountPercentage < 0 || values.clientDiscountPercentage > 100) {
      errors.push(['clientDiscountPercentage', 'Client discount must be between 0% and 100%.']);
    }

    errors.forEach(([fieldName, message]) => showFieldError(fieldName, message));

    if (errors.length > 0) {
      errorSummary.textContent = errors.map(([, message]) => message).join(' ');
      errorSummary.hidden = false;
    }

    return { values, errors };
  }

  function calculateQuote(values) {
    const laborSubtotal = values.estimatedProjectHours * values.quoteHourlyRate;
    const baseProjectAmount = laborSubtotal + values.directProjectExpenses;
    const contingencyAmount = baseProjectAmount * (values.contingencyBufferPercentage / 100);
    const quoteBeforeDiscount = baseProjectAmount + contingencyAmount;
    const discountAmount = quoteBeforeDiscount * (values.clientDiscountPercentage / 100);
    const finalClientQuote = quoteBeforeDiscount - discountAmount;
    const effectiveQuotedHourlyValue = finalClientQuote / values.estimatedProjectHours;

    return {
      laborSubtotal,
      directProjectExpenses: values.directProjectExpenses,
      baseProjectAmount,
      contingencyAmount,
      quoteBeforeDiscount,
      discountAmount,
      finalClientQuote,
      effectiveQuotedHourlyValue
    };
  }

  function createMetric(label, value, className) {
    const metric = document.createElement('div');
    metric.className = className ? `metric ${className}` : 'metric';
    const labelElement = document.createElement('span');
    const valueElement = document.createElement('strong');
    labelElement.textContent = label;
    valueElement.textContent = value;
    metric.append(labelElement, valueElement);
    return metric;
  }

  function renderResults(results, discountPercentage) {
    const metrics = [
      ['Labor subtotal', formatCurrency(results.laborSubtotal)],
      ['Direct project expenses', formatCurrency(results.directProjectExpenses)],
      ['Base project amount', formatCurrency(results.baseProjectAmount)],
      ['Contingency amount', formatCurrency(results.contingencyAmount)],
      ['Quote before discount', formatCurrency(results.quoteBeforeDiscount)],
      ['Discount amount', formatCurrency(results.discountAmount)],
      ['Final client quote', formatCurrency(results.finalClientQuote), 'final-quote-metric'],
      ['Effective quoted hourly value', formatCurrency(results.effectiveQuotedHourlyValue)]
    ];
    const fragment = document.createDocumentFragment();
    metrics.forEach(([label, value, className]) => fragment.appendChild(createMetric(label, value, className)));
    resultsContainer.replaceChildren(fragment);
    resultsContainer.hidden = false;
    statusMessage.className = 'status-message success';
    statusMessage.textContent = 'Client quote calculated.';

    if (discountPercentage === 100) {
      zeroQuoteMessage.textContent = 'A 100% discount produces a zero client quote.';
      zeroQuoteMessage.hidden = false;
    } else {
      zeroQuoteMessage.textContent = '';
      zeroQuoteMessage.hidden = true;
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    const { values, errors } = validateInputs();

    if (errors.length > 0) {
      hideResults('Correct the highlighted inputs before calculating the quote.');
      fields[errors[0][0]]?.focus();
      return;
    }

    const results = calculateQuote(values);

    if (!Object.values(results).every(Number.isFinite)) {
      errorSummary.textContent = 'The calculation produced a number too large to display. Reduce one or more inputs.';
      errorSummary.hidden = false;
      hideResults('Reduce one or more inputs before calculating the quote.');
      return;
    }

    renderResults(results, values.clientDiscountPercentage);
  }

  function handleInput(event) {
    const fieldName = event.target?.name;
    if (fieldName && fields[fieldName]) clearFieldError(fieldName);
    if (!resultsContainer.hidden) {
      hideResults('Inputs changed. Select Calculate Quote to update the estimate.');
    }
  }

  function handleReset() {
    clearErrors();
    hideResults('Enter your project assumptions and select Calculate Quote.');
  }

  form.addEventListener('submit', handleSubmit);
  form.addEventListener('input', handleInput);
  form.addEventListener('reset', handleReset);
})();
