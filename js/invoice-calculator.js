(function () {
  'use strict';

  if (window.__freelancerInvoiceCalculatorInitialized) return;
  window.__freelancerInvoiceCalculatorInitialized = true;

  const form = document.getElementById('invoiceCalculatorForm');
  const errorSummary = document.getElementById('invoiceErrorSummary');
  const statusMessage = document.getElementById('invoiceStatusMessage');
  const resultsContainer = document.getElementById('invoiceResults');
  const outcomeMessage = document.getElementById('invoiceOutcomeMessage');

  if (!form || !errorSummary || !statusMessage || !resultsContainer || !outcomeMessage) return;

  const fields = {
    billableHours: document.getElementById('billableHours'),
    invoiceHourlyRate: document.getElementById('invoiceHourlyRate'),
    fixedFeeServices: document.getElementById('fixedFeeServices'),
    reimbursableExpenses: document.getElementById('reimbursableExpenses'),
    invoiceDiscountPercentage: document.getElementById('invoiceDiscountPercentage'),
    estimatedInvoiceTaxPercentage: document.getElementById('estimatedInvoiceTaxPercentage'),
    amountAlreadyPaid: document.getElementById('amountAlreadyPaid')
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
    outcomeMessage.textContent = '';
    outcomeMessage.className = 'status-message';
    outcomeMessage.hidden = true;
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
      billableHours: readNumber('billableHours'),
      invoiceHourlyRate: readNumber('invoiceHourlyRate'),
      fixedFeeServices: readNumber('fixedFeeServices'),
      reimbursableExpenses: readNumber('reimbursableExpenses'),
      invoiceDiscountPercentage: readNumber('invoiceDiscountPercentage'),
      estimatedInvoiceTaxPercentage: readNumber('estimatedInvoiceTaxPercentage'),
      amountAlreadyPaid: readNumber('amountAlreadyPaid')
    };
    const errors = [];

    if (values.billableHours === null || !Number.isFinite(values.billableHours)) {
      errors.push(['billableHours', 'Enter billable hours, using 0 if no hourly work is included.']);
    } else if (values.billableHours < 0) {
      errors.push(['billableHours', 'Billable hours cannot be negative.']);
    } else if (values.billableHours > 10000) {
      errors.push(['billableHours', 'Billable hours cannot exceed 10,000.']);
    }

    if (values.invoiceHourlyRate === null || !Number.isFinite(values.invoiceHourlyRate)) {
      errors.push(['invoiceHourlyRate', 'Enter the hourly rate, using 0 if no hourly work is included.']);
    } else if (values.invoiceHourlyRate < 0) {
      errors.push(['invoiceHourlyRate', 'Hourly rate cannot be negative.']);
    }

    if (values.fixedFeeServices === null || !Number.isFinite(values.fixedFeeServices)) {
      errors.push(['fixedFeeServices', 'Enter fixed-fee services, using 0 if none are included.']);
    } else if (values.fixedFeeServices < 0) {
      errors.push(['fixedFeeServices', 'Fixed-fee services cannot be negative.']);
    }

    if (values.reimbursableExpenses === null || !Number.isFinite(values.reimbursableExpenses)) {
      errors.push(['reimbursableExpenses', 'Enter reimbursable expenses, using 0 if none are included.']);
    } else if (values.reimbursableExpenses < 0) {
      errors.push(['reimbursableExpenses', 'Reimbursable expenses cannot be negative.']);
    }

    if (values.invoiceDiscountPercentage === null || !Number.isFinite(values.invoiceDiscountPercentage)) {
      errors.push(['invoiceDiscountPercentage', 'Enter a client discount, using 0 for no discount.']);
    } else if (values.invoiceDiscountPercentage < 0 || values.invoiceDiscountPercentage > 100) {
      errors.push(['invoiceDiscountPercentage', 'Client discount must be between 0% and 100%.']);
    }

    if (values.estimatedInvoiceTaxPercentage === null || !Number.isFinite(values.estimatedInvoiceTaxPercentage)) {
      errors.push(['estimatedInvoiceTaxPercentage', 'Enter estimated sales tax or VAT, using 0 if none applies.']);
    } else if (values.estimatedInvoiceTaxPercentage < 0 || values.estimatedInvoiceTaxPercentage > 100) {
      errors.push(['estimatedInvoiceTaxPercentage', 'Estimated sales tax or VAT must be between 0% and 100%.']);
    }

    if (values.amountAlreadyPaid === null || !Number.isFinite(values.amountAlreadyPaid)) {
      errors.push(['amountAlreadyPaid', 'Enter the amount already paid, using 0 if no payment has been received.']);
    } else if (values.amountAlreadyPaid < 0) {
      errors.push(['amountAlreadyPaid', 'Amount already paid cannot be negative.']);
    }

    const basicInputsAreValid = errors.length === 0;

    if (basicInputsAreValid && values.billableHours > 0 && values.invoiceHourlyRate === 0) {
      errors.push(['invoiceHourlyRate', 'Enter an hourly rate greater than 0 when billable hours are included.']);
    }

    if (basicInputsAreValid && values.invoiceHourlyRate > 0 && values.billableHours === 0) {
      errors.push(['billableHours', 'Enter billable hours greater than 0 when an hourly rate is included, or set the hourly rate to 0.']);
    }

    if (
      basicInputsAreValid &&
      values.billableHours * values.invoiceHourlyRate === 0 &&
      values.fixedFeeServices === 0 &&
      values.reimbursableExpenses === 0
    ) {
      errors.push(['fixedFeeServices', 'Enter billable work, a fixed-fee service, or a reimbursable expense greater than 0.']);
    }

    errors.forEach(([fieldName, message]) => showFieldError(fieldName, message));

    if (errors.length > 0) {
      errorSummary.textContent = errors.map(([, message]) => message).join(' ');
      errorSummary.hidden = false;
    }

    return { values, errors };
  }

  function calculateInvoice(values) {
    const hourlyLaborAmount = values.billableHours * values.invoiceHourlyRate;
    const subtotalBeforeDiscount = hourlyLaborAmount + values.fixedFeeServices + values.reimbursableExpenses;
    const discountAmount = subtotalBeforeDiscount * (values.invoiceDiscountPercentage / 100);
    const subtotalAfterDiscount = subtotalBeforeDiscount - discountAmount;
    const estimatedSalesTaxOrVat = subtotalAfterDiscount * (values.estimatedInvoiceTaxPercentage / 100);
    const invoiceTotal = subtotalAfterDiscount + estimatedSalesTaxOrVat;
    const remainingAmount = invoiceTotal - values.amountAlreadyPaid;

    return {
      hourlyLaborAmount,
      fixedFeeServices: values.fixedFeeServices,
      reimbursableExpenses: values.reimbursableExpenses,
      subtotalBeforeDiscount,
      discountAmount,
      subtotalAfterDiscount,
      estimatedSalesTaxOrVat,
      invoiceTotal,
      amountAlreadyPaid: values.amountAlreadyPaid,
      remainingAmount
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

  function paymentState(remainingAmount) {
    if (Math.abs(remainingAmount) < 0.005) {
      return {
        label: 'Paid in full',
        value: formatCurrency(0),
        message: 'This invoice is fully paid.',
        messageClass: 'success'
      };
    }

    if (remainingAmount > 0) {
      return {
        label: 'Balance due',
        value: formatCurrency(remainingAmount),
        message: 'A remaining balance is due from the client.',
        messageClass: 'balance-due-message'
      };
    }

    return {
      label: 'Client credit or overpayment',
      value: formatCurrency(Math.abs(remainingAmount)),
      message: 'The recorded payment exceeds the calculated invoice total.',
      messageClass: 'credit-message'
    };
  }

  function renderResults(results) {
    const state = paymentState(results.remainingAmount);
    const metrics = [
      ['Hourly labor amount', formatCurrency(results.hourlyLaborAmount)],
      ['Fixed-fee services', formatCurrency(results.fixedFeeServices)],
      ['Reimbursable expenses', formatCurrency(results.reimbursableExpenses)],
      ['Subtotal before discount', formatCurrency(results.subtotalBeforeDiscount)],
      ['Discount amount', formatCurrency(results.discountAmount)],
      ['Subtotal after discount', formatCurrency(results.subtotalAfterDiscount)],
      ['Estimated sales tax or VAT', formatCurrency(results.estimatedSalesTaxOrVat)],
      ['Invoice total', formatCurrency(results.invoiceTotal), 'invoice-total-metric'],
      ['Amount already paid', formatCurrency(results.amountAlreadyPaid)],
      [state.label, state.value, 'payment-status-metric']
    ];
    const fragment = document.createDocumentFragment();
    metrics.forEach(([label, value, className]) => fragment.appendChild(createMetric(label, value, className)));
    resultsContainer.replaceChildren(fragment);
    resultsContainer.hidden = false;
    statusMessage.className = 'status-message success';
    statusMessage.textContent = 'Invoice estimate calculated.';
    outcomeMessage.className = `status-message ${state.messageClass}`;
    outcomeMessage.textContent = state.message;
    outcomeMessage.hidden = false;
  }

  function handleSubmit(event) {
    event.preventDefault();
    const { values, errors } = validateInputs();

    if (errors.length > 0) {
      hideResults('Correct the highlighted inputs before calculating the invoice.');
      fields[errors[0][0]]?.focus();
      return;
    }

    const results = calculateInvoice(values);

    if (!Object.values(results).every(Number.isFinite)) {
      errorSummary.textContent = 'The calculation produced a number too large to display. Reduce one or more inputs.';
      errorSummary.hidden = false;
      hideResults('Reduce one or more inputs before calculating the invoice.');
      errorSummary.focus();
      return;
    }

    renderResults(results);
  }

  function handleInput(event) {
    const fieldName = event.target?.name;
    if (fieldName && fields[fieldName]) clearFieldError(fieldName);
    if (!resultsContainer.hidden) {
      hideResults('Inputs changed. Select Calculate Invoice to update the estimate.');
    }
  }

  function handleReset() {
    clearErrors();
    hideResults('Enter the completed work and payment details, then select Calculate Invoice.');
  }

  form.addEventListener('submit', handleSubmit);
  form.addEventListener('input', handleInput);
  form.addEventListener('reset', handleReset);
})();
