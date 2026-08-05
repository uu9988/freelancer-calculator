(function () {
  'use strict';

  if (window.__freelancerProjectCostCalculatorInitialized) return;
  window.__freelancerProjectCostCalculatorInitialized = true;

  const form = document.getElementById('projectCostCalculatorForm');
  const errorSummary = document.getElementById('projectCostErrorSummary');
  const statusMessage = document.getElementById('projectCostStatusMessage');
  const resultsContainer = document.getElementById('projectCostResults');

  if (!form || !errorSummary || !statusMessage || !resultsContainer) return;

  const fields = {
    estimatedInternalProjectHours: document.getElementById('estimatedInternalProjectHours'),
    internalHourlyCost: document.getElementById('internalHourlyCost'),
    subcontractorCosts: document.getElementById('subcontractorCosts'),
    otherDirectProjectExpenses: document.getElementById('otherDirectProjectExpenses'),
    overheadAllocationPercentage: document.getElementById('overheadAllocationPercentage'),
    projectContingencyPercentage: document.getElementById('projectContingencyPercentage')
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
      estimatedInternalProjectHours: readNumber('estimatedInternalProjectHours'),
      internalHourlyCost: readNumber('internalHourlyCost'),
      subcontractorCosts: readNumber('subcontractorCosts'),
      otherDirectProjectExpenses: readNumber('otherDirectProjectExpenses'),
      overheadAllocationPercentage: readNumber('overheadAllocationPercentage'),
      projectContingencyPercentage: readNumber('projectContingencyPercentage')
    };
    const errors = [];

    if (values.estimatedInternalProjectHours === null || !Number.isFinite(values.estimatedInternalProjectHours)) {
      errors.push(['estimatedInternalProjectHours', 'Enter the estimated internal project hours.']);
    } else if (values.estimatedInternalProjectHours <= 0) {
      errors.push(['estimatedInternalProjectHours', 'Estimated internal project hours must be greater than 0.']);
    }

    if (values.internalHourlyCost === null || !Number.isFinite(values.internalHourlyCost)) {
      errors.push(['internalHourlyCost', 'Enter the internal hourly cost.']);
    } else if (values.internalHourlyCost <= 0) {
      errors.push(['internalHourlyCost', 'Internal hourly cost must be greater than 0.']);
    }

    if (values.subcontractorCosts === null || !Number.isFinite(values.subcontractorCosts)) {
      errors.push(['subcontractorCosts', 'Enter subcontractor costs, using 0 if there are none.']);
    } else if (values.subcontractorCosts < 0) {
      errors.push(['subcontractorCosts', 'Subcontractor costs cannot be negative.']);
    }

    if (values.otherDirectProjectExpenses === null || !Number.isFinite(values.otherDirectProjectExpenses)) {
      errors.push(['otherDirectProjectExpenses', 'Enter other direct project expenses, using 0 if there are none.']);
    } else if (values.otherDirectProjectExpenses < 0) {
      errors.push(['otherDirectProjectExpenses', 'Other direct project expenses cannot be negative.']);
    }

    if (values.overheadAllocationPercentage === null || !Number.isFinite(values.overheadAllocationPercentage)) {
      errors.push(['overheadAllocationPercentage', 'Enter an overhead allocation, using 0 if none is needed.']);
    } else if (values.overheadAllocationPercentage < 0 || values.overheadAllocationPercentage > 100) {
      errors.push(['overheadAllocationPercentage', 'Overhead allocation must be between 0% and 100%.']);
    }

    if (values.projectContingencyPercentage === null || !Number.isFinite(values.projectContingencyPercentage)) {
      errors.push(['projectContingencyPercentage', 'Enter a contingency percentage, using 0 if none is needed.']);
    } else if (values.projectContingencyPercentage < 0 || values.projectContingencyPercentage > 100) {
      errors.push(['projectContingencyPercentage', 'Contingency percentage must be between 0% and 100%.']);
    }

    errors.forEach(([fieldName, message]) => showFieldError(fieldName, message));

    if (errors.length > 0) {
      errorSummary.textContent = errors.map(([, message]) => message).join(' ');
      errorSummary.hidden = false;
    }

    return { values, errors };
  }

  function calculateProjectCost(values) {
    const internalLaborCost = values.estimatedInternalProjectHours * values.internalHourlyCost;
    const directProjectExpenses = values.subcontractorCosts + values.otherDirectProjectExpenses;
    const baseDeliveryCost = internalLaborCost + directProjectExpenses;
    const overheadAllocationAmount = baseDeliveryCost * (values.overheadAllocationPercentage / 100);
    const costBeforeContingency = baseDeliveryCost + overheadAllocationAmount;
    const contingencyAmount = costBeforeContingency * (values.projectContingencyPercentage / 100);
    const totalEstimatedDeliveryCost = costBeforeContingency + contingencyAmount;
    const averageDeliveryCostPerInternalHour = totalEstimatedDeliveryCost / values.estimatedInternalProjectHours;

    return {
      internalLaborCost,
      directProjectExpenses,
      baseDeliveryCost,
      overheadAllocationAmount,
      costBeforeContingency,
      contingencyAmount,
      totalEstimatedDeliveryCost,
      averageDeliveryCostPerInternalHour
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
      ['Internal labor cost', formatCurrency(results.internalLaborCost)],
      ['Direct project expenses', formatCurrency(results.directProjectExpenses)],
      ['Base delivery cost', formatCurrency(results.baseDeliveryCost)],
      ['Overhead allocation amount', formatCurrency(results.overheadAllocationAmount)],
      ['Cost before contingency', formatCurrency(results.costBeforeContingency)],
      ['Contingency amount', formatCurrency(results.contingencyAmount)],
      ['Total estimated delivery cost', formatCurrency(results.totalEstimatedDeliveryCost), 'total-cost-metric'],
      ['Average delivery cost per internal hour', formatCurrency(results.averageDeliveryCostPerInternalHour)]
    ];
    const fragment = document.createDocumentFragment();
    metrics.forEach(([label, value, className]) => fragment.appendChild(createMetric(label, value, className)));
    resultsContainer.replaceChildren(fragment);
    resultsContainer.hidden = false;
    statusMessage.className = 'status-message success';
    statusMessage.textContent = 'Project delivery cost calculated.';
  }

  function handleSubmit(event) {
    event.preventDefault();
    const { values, errors } = validateInputs();

    if (errors.length > 0) {
      hideResults('Correct the highlighted inputs before calculating project cost.');
      fields[errors[0][0]]?.focus();
      return;
    }

    const results = calculateProjectCost(values);

    if (!Object.values(results).every(Number.isFinite)) {
      errorSummary.textContent = 'The calculation produced a number too large to display. Reduce one or more inputs.';
      errorSummary.hidden = false;
      hideResults('Reduce one or more inputs before calculating project cost.');
      return;
    }

    renderResults(results);
  }

  function handleInput(event) {
    const fieldName = event.target?.name;
    if (fieldName && fields[fieldName]) clearFieldError(fieldName);
    if (!resultsContainer.hidden) {
      hideResults('Inputs changed. Select Calculate Project Cost to update the estimate.');
    }
  }

  function handleReset() {
    clearErrors();
    hideResults('Enter your project assumptions and select Calculate Project Cost.');
  }

  form.addEventListener('submit', handleSubmit);
  form.addEventListener('input', handleInput);
  form.addEventListener('reset', handleReset);
})();
