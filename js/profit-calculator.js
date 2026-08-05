(function () {
  'use strict';

  if (window.__freelancerProfitCalculatorInitialized) return;
  window.__freelancerProfitCalculatorInitialized = true;

  const form = document.getElementById('profitCalculatorForm');
  const errorSummary = document.getElementById('profitErrorSummary');
  const statusMessage = document.getElementById('profitStatusMessage');
  const resultsContainer = document.getElementById('profitResults');
  const outcomeMessage = document.getElementById('profitOutcomeMessage');

  if (!form || !errorSummary || !statusMessage || !resultsContainer || !outcomeMessage) return;

  const fields = {
    clientRevenue: document.getElementById('clientRevenue'),
    profitInternalProjectHours: document.getElementById('profitInternalProjectHours'),
    profitInternalHourlyCost: document.getElementById('profitInternalHourlyCost'),
    profitSubcontractorCosts: document.getElementById('profitSubcontractorCosts'),
    profitOtherDirectExpenses: document.getElementById('profitOtherDirectExpenses'),
    profitOverheadPercentage: document.getElementById('profitOverheadPercentage'),
    paymentProcessingFeePercentage: document.getElementById('paymentProcessingFeePercentage')
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
    outcomeMessage.textContent = '';
    outcomeMessage.className = 'status-message profit-outcome';
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
      clientRevenue: readNumber('clientRevenue'),
      profitInternalProjectHours: readNumber('profitInternalProjectHours'),
      profitInternalHourlyCost: readNumber('profitInternalHourlyCost'),
      profitSubcontractorCosts: readNumber('profitSubcontractorCosts'),
      profitOtherDirectExpenses: readNumber('profitOtherDirectExpenses'),
      profitOverheadPercentage: readNumber('profitOverheadPercentage'),
      paymentProcessingFeePercentage: readNumber('paymentProcessingFeePercentage')
    };
    const errors = [];

    if (values.clientRevenue === null || !Number.isFinite(values.clientRevenue)) {
      errors.push(['clientRevenue', 'Enter the client revenue.']);
    } else if (values.clientRevenue <= 0) {
      errors.push(['clientRevenue', 'Client revenue must be greater than 0.']);
    }

    if (values.profitInternalProjectHours === null || !Number.isFinite(values.profitInternalProjectHours)) {
      errors.push(['profitInternalProjectHours', 'Enter the internal project hours.']);
    } else if (values.profitInternalProjectHours <= 0) {
      errors.push(['profitInternalProjectHours', 'Internal project hours must be greater than 0.']);
    } else if (values.profitInternalProjectHours > 10000) {
      errors.push(['profitInternalProjectHours', 'Internal project hours cannot exceed 10,000.']);
    }

    if (values.profitInternalHourlyCost === null || !Number.isFinite(values.profitInternalHourlyCost)) {
      errors.push(['profitInternalHourlyCost', 'Enter the internal hourly cost.']);
    } else if (values.profitInternalHourlyCost <= 0) {
      errors.push(['profitInternalHourlyCost', 'Internal hourly cost must be greater than 0.']);
    }

    if (values.profitSubcontractorCosts === null || !Number.isFinite(values.profitSubcontractorCosts)) {
      errors.push(['profitSubcontractorCosts', 'Enter subcontractor costs, using 0 if there are none.']);
    } else if (values.profitSubcontractorCosts < 0) {
      errors.push(['profitSubcontractorCosts', 'Subcontractor costs cannot be negative.']);
    }

    if (values.profitOtherDirectExpenses === null || !Number.isFinite(values.profitOtherDirectExpenses)) {
      errors.push(['profitOtherDirectExpenses', 'Enter other direct project expenses, using 0 if there are none.']);
    } else if (values.profitOtherDirectExpenses < 0) {
      errors.push(['profitOtherDirectExpenses', 'Other direct project expenses cannot be negative.']);
    }

    if (values.profitOverheadPercentage === null || !Number.isFinite(values.profitOverheadPercentage)) {
      errors.push(['profitOverheadPercentage', 'Enter an overhead allocation, using 0 if none is needed.']);
    } else if (values.profitOverheadPercentage < 0 || values.profitOverheadPercentage > 100) {
      errors.push(['profitOverheadPercentage', 'Overhead allocation must be between 0% and 100%.']);
    }

    if (values.paymentProcessingFeePercentage === null || !Number.isFinite(values.paymentProcessingFeePercentage)) {
      errors.push(['paymentProcessingFeePercentage', 'Enter a payment processing fee, using 0 if none applies.']);
    } else if (values.paymentProcessingFeePercentage < 0 || values.paymentProcessingFeePercentage > 100) {
      errors.push(['paymentProcessingFeePercentage', 'Payment processing fee must be between 0% and 100%.']);
    }

    errors.forEach(([fieldName, message]) => showFieldError(fieldName, message));

    if (errors.length > 0) {
      errorSummary.textContent = errors.map(([, message]) => message).join(' ');
      errorSummary.hidden = false;
    }

    return { values, errors };
  }

  function calculateProfit(values) {
    const internalLaborCost = values.profitInternalProjectHours * values.profitInternalHourlyCost;
    const directProjectExpenses = values.profitSubcontractorCosts + values.profitOtherDirectExpenses;
    const baseProjectCost = internalLaborCost + directProjectExpenses;
    const overheadAllocationAmount = baseProjectCost * (values.profitOverheadPercentage / 100);
    const paymentProcessingFeeAmount = values.clientRevenue * (values.paymentProcessingFeePercentage / 100);
    const totalProjectCost = baseProjectCost + overheadAllocationAmount + paymentProcessingFeeAmount;
    const projectProfit = values.clientRevenue - totalProjectCost;
    const profitMargin = (projectProfit / values.clientRevenue) * 100;
    const costPercentage = (totalProjectCost / values.clientRevenue) * 100;
    const revenuePerInternalHour = values.clientRevenue / values.profitInternalProjectHours;
    const profitPerInternalHour = projectProfit / values.profitInternalProjectHours;

    return {
      clientRevenue: values.clientRevenue,
      internalLaborCost,
      subcontractorCosts: values.profitSubcontractorCosts,
      otherDirectProjectExpenses: values.profitOtherDirectExpenses,
      directProjectExpenses,
      baseProjectCost,
      overheadAllocationAmount,
      paymentProcessingFeeAmount,
      totalProjectCost,
      projectProfit,
      profitMargin,
      costPercentage,
      revenuePerInternalHour,
      profitPerInternalHour
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

  function renderOutcome(projectProfit) {
    const epsilon = 0.000001;
    outcomeMessage.hidden = false;

    if (projectProfit > epsilon) {
      outcomeMessage.className = 'status-message profit-outcome positive';
      outcomeMessage.textContent = 'This project is estimated to produce a positive profit.';
    } else if (projectProfit < -epsilon) {
      outcomeMessage.className = 'status-message profit-outcome loss';
      outcomeMessage.textContent = 'This project is estimated to produce a loss.';
    } else {
      outcomeMessage.className = 'status-message profit-outcome break-even';
      outcomeMessage.textContent = 'This project is estimated to break even.';
    }
  }

  function renderResults(results) {
    const metrics = [
      ['Client revenue', formatCurrency(results.clientRevenue)],
      ['Internal labor cost', formatCurrency(results.internalLaborCost)],
      ['Subcontractor costs', formatCurrency(results.subcontractorCosts)],
      ['Other direct project expenses', formatCurrency(results.otherDirectProjectExpenses)],
      ['Direct project expenses', formatCurrency(results.directProjectExpenses)],
      ['Base project cost', formatCurrency(results.baseProjectCost)],
      ['Overhead allocation amount', formatCurrency(results.overheadAllocationAmount)],
      ['Payment processing fee amount', formatCurrency(results.paymentProcessingFeeAmount)],
      ['Total project cost', formatCurrency(results.totalProjectCost)],
      ['Project profit', formatCurrency(results.projectProfit), 'profit-metric'],
      ['Profit margin', formatPercentage(results.profitMargin), 'margin-metric'],
      ['Cost percentage', formatPercentage(results.costPercentage)],
      ['Revenue per internal hour', formatCurrency(results.revenuePerInternalHour)],
      ['Profit per internal hour', formatCurrency(results.profitPerInternalHour)]
    ];
    const fragment = document.createDocumentFragment();
    metrics.forEach(([label, value, className]) => fragment.appendChild(createMetric(label, value, className)));
    resultsContainer.replaceChildren(fragment);
    resultsContainer.hidden = false;
    statusMessage.className = 'status-message success';
    statusMessage.textContent = 'Project profit calculated.';
    renderOutcome(results.projectProfit);
  }

  function handleSubmit(event) {
    event.preventDefault();
    const { values, errors } = validateInputs();

    if (errors.length > 0) {
      hideResults('Correct the highlighted inputs before calculating project profit.');
      fields[errors[0][0]]?.focus();
      return;
    }

    renderResults(calculateProfit(values));
  }

  function handleInput(event) {
    const fieldName = event.target?.name;
    if (fieldName && fields[fieldName]) clearFieldError(fieldName);
    if (!resultsContainer.hidden) {
      hideResults('Inputs changed. Select Calculate Profit to update the estimate.');
    }
  }

  function handleReset() {
    clearErrors();
    hideResults('Enter your project assumptions and select Calculate Profit.');
  }

  form.addEventListener('submit', handleSubmit);
  form.addEventListener('input', handleInput);
  form.addEventListener('reset', handleReset);
})();
