(function () {
  'use strict';

  if (window.__freelancerExpenseCalculatorInitialized) return;
  window.__freelancerExpenseCalculatorInitialized = true;

  const form = document.getElementById('expenseCalculatorForm');
  const errorSummary = document.getElementById('expenseErrorSummary');
  const statusMessage = document.getElementById('expenseStatusMessage');
  const resultsContainer = document.getElementById('expenseResults');

  if (!form || !errorSummary || !statusMessage || !resultsContainer) return;

  const expenseFieldNames = [
    'softwareSubscriptions',
    'workspaceUtilities',
    'insuranceAdministration',
    'marketingAdvertising',
    'internetPhone',
    'equipmentHardware',
    'educationTraining',
    'travelTransportation',
    'otherAnnualExpenses'
  ];

  const fields = {
    softwareSubscriptions: document.getElementById('softwareSubscriptions'),
    workspaceUtilities: document.getElementById('workspaceUtilities'),
    insuranceAdministration: document.getElementById('insuranceAdministration'),
    marketingAdvertising: document.getElementById('marketingAdvertising'),
    internetPhone: document.getElementById('internetPhone'),
    equipmentHardware: document.getElementById('equipmentHardware'),
    educationTraining: document.getElementById('educationTraining'),
    travelTransportation: document.getElementById('travelTransportation'),
    otherAnnualExpenses: document.getElementById('otherAnnualExpenses'),
    expectedAnnualRevenue: document.getElementById('expectedAnnualRevenue'),
    expectedAnnualBillableHours: document.getElementById('expectedAnnualBillableHours')
  };

  function formatCurrency(value) {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    }).format(value);
  }

  function formatPercentage(value) {
    return `${value.toFixed(2)}%`;
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
    statusMessage.className = 'status-message';
    statusMessage.textContent = message;
  }

  function readNumber(fieldName) {
    const rawValue = fields[fieldName]?.value.trim() || '';
    return rawValue === '' ? null : Number(rawValue);
  }

  function validateInputs() {
    clearErrors();
    const values = {};
    const errors = [];

    expenseFieldNames.forEach((fieldName) => {
      values[fieldName] = readNumber(fieldName);
      if (values[fieldName] === null || !Number.isFinite(values[fieldName])) {
        const label = fields[fieldName]?.dataset.fieldLabel || 'This expense';
        errors.push([fieldName, `Enter ${label.toLowerCase()}, using 0 if there is no expense.`]);
      } else if (values[fieldName] < 0) {
        const label = fields[fieldName]?.dataset.fieldLabel || 'This expense';
        errors.push([fieldName, `${label} cannot be negative.`]);
      }
    });

    values.expectedAnnualRevenue = readNumber('expectedAnnualRevenue');
    if (values.expectedAnnualRevenue === null || !Number.isFinite(values.expectedAnnualRevenue)) {
      errors.push(['expectedAnnualRevenue', 'Enter expected annual revenue.']);
    } else if (values.expectedAnnualRevenue <= 0) {
      errors.push(['expectedAnnualRevenue', 'Expected annual revenue must be greater than 0.']);
    }

    values.expectedAnnualBillableHours = readNumber('expectedAnnualBillableHours');
    if (values.expectedAnnualBillableHours === null || !Number.isFinite(values.expectedAnnualBillableHours)) {
      errors.push(['expectedAnnualBillableHours', 'Enter expected annual billable hours.']);
    } else if (values.expectedAnnualBillableHours <= 0) {
      errors.push(['expectedAnnualBillableHours', 'Expected annual billable hours must be greater than 0.']);
    } else if (values.expectedAnnualBillableHours > 10000) {
      errors.push(['expectedAnnualBillableHours', 'Expected annual billable hours cannot exceed 10,000.']);
    }

    const hasValidExpenseValues = expenseFieldNames.every((fieldName) => Number.isFinite(values[fieldName]));
    if (hasValidExpenseValues && expenseFieldNames.every((fieldName) => values[fieldName] === 0)) {
      errors.push(['softwareSubscriptions', 'Enter at least one monthly or annual business expense greater than 0.']);
    }

    errors.forEach(([fieldName, message]) => showFieldError(fieldName, message));

    if (errors.length > 0) {
      errorSummary.textContent = errors.map(([, message]) => message).join(' ');
      errorSummary.hidden = false;
    }

    return { values, errors };
  }

  function calculateExpenses(values) {
    const monthlyRecurringExpenses =
      values.softwareSubscriptions +
      values.workspaceUtilities +
      values.insuranceAdministration +
      values.marketingAdvertising +
      values.internetPhone;
    const annualRecurringExpenses = monthlyRecurringExpenses * 12;
    const annualVariableExpenses =
      values.equipmentHardware +
      values.educationTraining +
      values.travelTransportation +
      values.otherAnnualExpenses;
    const totalAnnualBusinessExpenses = annualRecurringExpenses + annualVariableExpenses;
    const averageMonthlyBusinessExpenses = totalAnnualBusinessExpenses / 12;
    const operatingExpenseRatio = (totalAnnualBusinessExpenses / values.expectedAnnualRevenue) * 100;
    const expenseCostPerBillableHour = totalAnnualBusinessExpenses / values.expectedAnnualBillableHours;

    return {
      monthlyRecurringExpenses,
      annualRecurringExpenses,
      equipmentHardware: values.equipmentHardware,
      educationTraining: values.educationTraining,
      travelTransportation: values.travelTransportation,
      otherAnnualExpenses: values.otherAnnualExpenses,
      annualVariableExpenses,
      totalAnnualBusinessExpenses,
      averageMonthlyBusinessExpenses,
      operatingExpenseRatio,
      expenseCostPerBillableHour
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

  function renderResults(results) {
    const metrics = [
      ['Monthly recurring expenses', formatCurrency(results.monthlyRecurringExpenses)],
      ['Annual recurring expenses', formatCurrency(results.annualRecurringExpenses)],
      ['Equipment and hardware', formatCurrency(results.equipmentHardware)],
      ['Education and training', formatCurrency(results.educationTraining)],
      ['Travel and transportation', formatCurrency(results.travelTransportation)],
      ['Other annual expenses', formatCurrency(results.otherAnnualExpenses)],
      ['Annual variable expenses', formatCurrency(results.annualVariableExpenses)],
      ['Total annual business expenses', formatCurrency(results.totalAnnualBusinessExpenses), 'expense-total-metric'],
      ['Average monthly business expenses', formatCurrency(results.averageMonthlyBusinessExpenses), 'expense-highlight-metric'],
      ['Operating expense ratio', formatPercentage(results.operatingExpenseRatio)],
      ['Expense cost per billable hour', formatCurrency(results.expenseCostPerBillableHour), 'expense-highlight-metric']
    ];
    const fragment = document.createDocumentFragment();
    metrics.forEach(([label, value, className]) => fragment.appendChild(createMetric(label, value, className)));
    resultsContainer.replaceChildren(fragment);
    resultsContainer.hidden = false;
    statusMessage.className = 'status-message success';
    statusMessage.textContent = 'Business expenses calculated.';
  }

  function handleSubmit(event) {
    event.preventDefault();
    const { values, errors } = validateInputs();

    if (errors.length > 0) {
      hideResults('Correct the highlighted inputs before calculating expenses.');
      fields[errors[0][0]]?.focus();
      return;
    }

    const results = calculateExpenses(values);

    if (!Object.values(results).every(Number.isFinite)) {
      errorSummary.textContent = 'The calculation produced a number too large to display. Reduce one or more inputs.';
      errorSummary.hidden = false;
      hideResults('Reduce one or more inputs before calculating expenses.');
      errorSummary.focus();
      return;
    }

    renderResults(results);
  }

  function handleInput(event) {
    const fieldName = event.target?.name;
    if (fieldName && fields[fieldName]) clearFieldError(fieldName);
    if (!resultsContainer.hidden) {
      hideResults('Inputs changed. Select Calculate Expenses to update the estimate.');
    }
  }

  function handleReset() {
    clearErrors();
    hideResults('Enter your business expenses and planning assumptions, then select Calculate Expenses.');
  }

  form.addEventListener('submit', handleSubmit);
  form.addEventListener('input', handleInput);
  form.addEventListener('reset', handleReset);
})();
