(function () {
  'use strict';

  if (window.__freelancerIncomeCalculatorInitialized) return;
  window.__freelancerIncomeCalculatorInitialized = true;

  const form = document.getElementById('incomeCalculatorForm');
  const errorSummary = document.getElementById('incomeErrorSummary');
  const statusMessage = document.getElementById('incomeStatusMessage');
  const resultsContainer = document.getElementById('incomeResults');
  const lossMessage = document.getElementById('incomeLossMessage');

  if (!form || !errorSummary || !statusMessage || !resultsContainer || !lossMessage) return;

  const fields = {
    averageHourlyRate: document.getElementById('averageHourlyRate'),
    billableHoursPerWeek: document.getElementById('billableHoursPerWeek'),
    workingWeeksPerYear: document.getElementById('workingWeeksPerYear'),
    annualBusinessExpenses: document.getElementById('annualBusinessExpenses'),
    estimatedEffectiveTaxRate: document.getElementById('estimatedEffectiveTaxRate')
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
    lossMessage.textContent = '';
    lossMessage.hidden = true;
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
      averageHourlyRate: readNumber('averageHourlyRate'),
      billableHoursPerWeek: readNumber('billableHoursPerWeek'),
      workingWeeksPerYear: readNumber('workingWeeksPerYear'),
      annualBusinessExpenses: readNumber('annualBusinessExpenses'),
      estimatedEffectiveTaxRate: readNumber('estimatedEffectiveTaxRate')
    };
    const errors = [];

    if (values.averageHourlyRate === null || !Number.isFinite(values.averageHourlyRate)) {
      errors.push(['averageHourlyRate', 'Enter your average hourly rate.']);
    } else if (values.averageHourlyRate <= 0) {
      errors.push(['averageHourlyRate', 'Average hourly rate must be greater than 0.']);
    }

    if (values.billableHoursPerWeek === null || !Number.isFinite(values.billableHoursPerWeek)) {
      errors.push(['billableHoursPerWeek', 'Enter your billable hours per week.']);
    } else if (values.billableHoursPerWeek <= 0) {
      errors.push(['billableHoursPerWeek', 'Billable hours per week must be greater than 0.']);
    } else if (values.billableHoursPerWeek > 168) {
      errors.push(['billableHoursPerWeek', 'Billable hours per week cannot exceed 168.']);
    }

    if (values.workingWeeksPerYear === null || !Number.isFinite(values.workingWeeksPerYear)) {
      errors.push(['workingWeeksPerYear', 'Enter your working weeks per year.']);
    } else if (values.workingWeeksPerYear < 1 || values.workingWeeksPerYear > 52) {
      errors.push(['workingWeeksPerYear', 'Working weeks per year must be between 1 and 52.']);
    }

    if (values.annualBusinessExpenses === null || !Number.isFinite(values.annualBusinessExpenses)) {
      errors.push(['annualBusinessExpenses', 'Enter annual business expenses, using 0 if you have none.']);
    } else if (values.annualBusinessExpenses < 0) {
      errors.push(['annualBusinessExpenses', 'Annual business expenses cannot be negative.']);
    }

    if (values.estimatedEffectiveTaxRate === null || !Number.isFinite(values.estimatedEffectiveTaxRate)) {
      errors.push(['estimatedEffectiveTaxRate', 'Enter an estimated effective tax rate, using 0 if no reserve is needed.']);
    } else if (values.estimatedEffectiveTaxRate < 0 || values.estimatedEffectiveTaxRate > 100) {
      errors.push(['estimatedEffectiveTaxRate', 'Estimated effective tax rate must be between 0% and 100%.']);
    }

    errors.forEach(([fieldName, message]) => showFieldError(fieldName, message));

    if (errors.length > 0) {
      errorSummary.textContent = errors.map(([, message]) => message).join(' ');
      errorSummary.hidden = false;
      return { values, errors };
    }

    return { values, errors };
  }

  function calculateIncome(values) {
    const annualGrossRevenue = values.averageHourlyRate * values.billableHoursPerWeek * values.workingWeeksPerYear;
    const averageMonthlyGrossRevenue = annualGrossRevenue / 12;
    const estimatedTaxablePlanningBase = Math.max(annualGrossRevenue - values.annualBusinessExpenses, 0);
    const estimatedTaxReserve = estimatedTaxablePlanningBase * (values.estimatedEffectiveTaxRate / 100);
    const annualPlanningIncome = annualGrossRevenue - values.annualBusinessExpenses - estimatedTaxReserve;
    const averageMonthlyPlanningIncome = annualPlanningIncome / 12;
    const effectivePlanningIncomePercentage = annualGrossRevenue > 0
      ? (annualPlanningIncome / annualGrossRevenue) * 100
      : null;

    return {
      annualGrossRevenue,
      averageMonthlyGrossRevenue,
      annualBusinessExpenses: values.annualBusinessExpenses,
      estimatedTaxablePlanningBase,
      estimatedTaxReserve,
      annualPlanningIncome,
      averageMonthlyPlanningIncome,
      effectivePlanningIncomePercentage
    };
  }

  function createMetric(label, value) {
    const metric = document.createElement('div');
    metric.className = 'metric';
    const labelElement = document.createElement('span');
    const valueElement = document.createElement('strong');
    labelElement.textContent = label;
    valueElement.textContent = value;
    metric.append(labelElement, valueElement);
    return metric;
  }

  function renderResults(results) {
    const metrics = [
      ['Annual gross revenue', formatCurrency(results.annualGrossRevenue)],
      ['Average monthly gross revenue', formatCurrency(results.averageMonthlyGrossRevenue)],
      ['Annual business expenses', formatCurrency(results.annualBusinessExpenses)],
      ['Estimated taxable planning base', formatCurrency(results.estimatedTaxablePlanningBase)],
      ['Estimated tax reserve', formatCurrency(results.estimatedTaxReserve)],
      ['Annual planning income', formatCurrency(results.annualPlanningIncome)],
      ['Average monthly planning income', formatCurrency(results.averageMonthlyPlanningIncome)],
      ['Effective planning income percentage', results.effectivePlanningIncomePercentage === null
        ? 'Not available'
        : formatPercentage(results.effectivePlanningIncomePercentage)]
    ];
    const fragment = document.createDocumentFragment();
    metrics.forEach(([label, value]) => fragment.appendChild(createMetric(label, value)));
    resultsContainer.replaceChildren(fragment);
    resultsContainer.hidden = false;
    statusMessage.className = 'status-message success';
    statusMessage.textContent = 'Income estimate calculated.';

    if (results.annualPlanningIncome < 0) {
      lossMessage.textContent = 'Estimated loss: annual business expenses exceed gross revenue. Review your rate, billable hours, working weeks, or costs.';
      lossMessage.hidden = false;
    } else {
      lossMessage.textContent = '';
      lossMessage.hidden = true;
    }
  }

  function handleSubmit(event) {
    event.preventDefault();
    const { values, errors } = validateInputs();

    if (errors.length > 0) {
      hideResults('Correct the highlighted inputs before calculating income.');
      fields[errors[0][0]]?.focus();
      return;
    }

    renderResults(calculateIncome(values));
  }

  function handleInput(event) {
    const fieldName = event.target?.name;
    if (fieldName && fields[fieldName]) clearFieldError(fieldName);
    if (!resultsContainer.hidden) {
      hideResults('Inputs changed. Select Calculate Income to update the estimate.');
    }
  }

  function handleReset() {
    clearErrors();
    hideResults('Enter your assumptions and select Calculate Income.');
  }

  form.addEventListener('submit', handleSubmit);
  form.addEventListener('input', handleInput);
  form.addEventListener('reset', handleReset);
})();
