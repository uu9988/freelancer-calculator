// Main calculator form and result containers.
const form = document.getElementById('rate-form');
const resultsGrid = document.getElementById('resultsGrid');
const statusMessage = document.getElementById('statusMessage');
let incomeChart = null;

// Format values for display.
function formatCurrency(value) {
  return new Intl.NumberFormat('en-US', {
    style: 'currency',
    currency: 'USD',
    maximumFractionDigits: 2
  }).format(value);
}

function formatNumber(value) {
  return new Intl.NumberFormat('en-US', {
    maximumFractionDigits: 2
  }).format(value);
}

function createMetric(title, value) {
  const metric = document.createElement('div');
  metric.className = 'metric';
  metric.innerHTML = `<span>${title}</span><strong>${value}</strong>`;
  return metric;
}

function buildChart(data) {
  const canvas = document.getElementById('incomeChart');

  if (!canvas || typeof Chart === 'undefined') {
    return;
  }

  if (incomeChart) {
    incomeChart.destroy();
  }

  incomeChart = new Chart(canvas, {
    type: 'pie',
    data: {
      labels: ['Take-home income', 'Business expenses', 'Estimated tax'],
      datasets: [
        {
          data: [data.takeHomeIncome, data.businessExpenses, data.estimatedTax],
          backgroundColor: ['#2563eb', '#f59e0b', '#10b981']
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: {
          position: 'bottom'
        }
      }
    }
  });
}

function showError(message) {
  resultsGrid.innerHTML = '';
  statusMessage.className = 'status-message error';
  statusMessage.textContent = message;

  if (incomeChart) {
    incomeChart.destroy();
    incomeChart = null;
  }
}

// Calculate the main freelance pricing metrics from the provided inputs.
function calculateResults(values) {
  const annualWorkingDays = values.workingDaysPerWeek * 52 - values.vacationDaysPerYear - values.publicHolidaysPerYear;
  const annualWorkingHours = annualWorkingDays * values.workingHoursPerDay;
  const annualBillableHours = annualWorkingHours * (values.billableTimePercentage / 100);
  const requiredPreTaxRevenue = (values.targetAnnualTakeHomeIncome + values.annualBusinessExpenses) / (1 - values.estimatedTaxRate / 100);
  const minimumHourlyRate = requiredPreTaxRevenue / annualBillableHours;
  const recommendedHourlyRate = minimumHourlyRate * 1.15;
  const recommendedDailyRate = recommendedHourlyRate * values.workingHoursPerDay;
  const monthlyRevenueTarget = requiredPreTaxRevenue / 12;
  const estimatedTax = requiredPreTaxRevenue * (values.estimatedTaxRate / 100);

  return {
    annualWorkingDays,
    annualWorkingHours,
    annualBillableHours,
    requiredPreTaxRevenue,
    minimumHourlyRate,
    recommendedHourlyRate,
    recommendedDailyRate,
    monthlyRevenueTarget,
    estimatedTax,
    takeHomeIncome: values.targetAnnualTakeHomeIncome,
    businessExpenses: values.annualBusinessExpenses
  };
}

function validateInputs(values) {
  const errors = [];

  if (!values.targetAnnualTakeHomeIncome || values.targetAnnualTakeHomeIncome <= 0) {
    errors.push('Target annual take-home income must be greater than 0.');
  }

  if (!values.workingDaysPerWeek || values.workingDaysPerWeek <= 0) {
    errors.push('Working days per week must be greater than 0.');
  }

  if (!values.workingHoursPerDay || values.workingHoursPerDay <= 0) {
    errors.push('Working hours per day must be greater than 0.');
  }

  if (values.workingDaysPerWeek > 7) {
    errors.push('Working days per week cannot exceed 7.');
  }

  if (values.workingHoursPerDay > 24) {
    errors.push('Working hours per day cannot exceed 24.');
  }

  if (values.vacationDaysPerYear < 0 || values.publicHolidaysPerYear < 0) {
    errors.push('Vacation days and public holidays cannot be negative.');
  }

  if (values.annualBusinessExpenses < 0) {
    errors.push('Annual business expenses cannot be negative.');
  }

  if (values.estimatedTaxRate < 0) {
    errors.push('Estimated tax rate cannot be negative.');
  }

  if (values.billableTimePercentage <= 0) {
    errors.push('Billable time percentage must be greater than 0.');
  }

  if (values.estimatedTaxRate >= 100) {
    errors.push('Estimated tax rate must be less than 100%.');
  }

  const requiredFields = [
    'targetAnnualTakeHomeIncome',
    'workingDaysPerWeek',
    'workingHoursPerDay',
    'vacationDaysPerYear',
    'publicHolidaysPerYear',
    'annualBusinessExpenses',
    'estimatedTaxRate',
    'billableTimePercentage'
  ];

  const hasEmptyFields = requiredFields.some((field) => {
    const inputValue = document.getElementById(field)?.value;
    return inputValue === '';
  });

  if (hasEmptyFields) {
    errors.push('Please fill in all fields.');
  }

  if (values.estimatedTaxRate === 100) {
    errors.push('Tax rate of 100% is not supported.');
  }

  return errors;
}

function renderResults(results) {
  resultsGrid.innerHTML = '';
  const metrics = [
    ['Annual working days', formatNumber(results.annualWorkingDays)],
    ['Annual working hours', formatNumber(results.annualWorkingHours)],
    ['Annual billable hours', formatNumber(results.annualBillableHours)],
    ['Required pre-tax revenue', formatCurrency(results.requiredPreTaxRevenue)],
    ['Minimum hourly rate', formatCurrency(results.minimumHourlyRate)],
    ['Recommended hourly rate', formatCurrency(results.recommendedHourlyRate)],
    ['Recommended daily rate', formatCurrency(results.recommendedDailyRate)],
    ['Monthly revenue target', formatCurrency(results.monthlyRevenueTarget)],
    ['Estimated tax', formatCurrency(results.estimatedTax)],
    ['Target take-home income', formatCurrency(results.takeHomeIncome)]
  ];

  metrics.forEach(([title, value]) => {
    resultsGrid.appendChild(createMetric(title, value));
  });

  statusMessage.className = 'status-message success';
  statusMessage.textContent = 'Calculation completed successfully.';

  buildChart(results);
}

function handleCalculation() {
  const values = {
    targetAnnualTakeHomeIncome: Number(document.getElementById('targetAnnualTakeHomeIncome').value),
    workingDaysPerWeek: Number(document.getElementById('workingDaysPerWeek').value),
    workingHoursPerDay: Number(document.getElementById('workingHoursPerDay').value),
    vacationDaysPerYear: Number(document.getElementById('vacationDaysPerYear').value),
    publicHolidaysPerYear: Number(document.getElementById('publicHolidaysPerYear').value),
    annualBusinessExpenses: Number(document.getElementById('annualBusinessExpenses').value),
    estimatedTaxRate: Number(document.getElementById('estimatedTaxRate').value),
    billableTimePercentage: Number(document.getElementById('billableTimePercentage').value)
  };

  const validationErrors = validateInputs(values);

  if (validationErrors.length > 0) {
    showError(validationErrors[0]);
    return;
  }

  if ([values.targetAnnualTakeHomeIncome, values.workingDaysPerWeek, values.workingHoursPerDay, values.vacationDaysPerYear, values.publicHolidaysPerYear, values.annualBusinessExpenses, values.estimatedTaxRate, values.billableTimePercentage].some((value) => !Number.isFinite(value))) {
    showError('Please enter valid numbers.');
    return;
  }

  const results = calculateResults(values);

  if (!Number.isFinite(results.annualWorkingDays) || !Number.isFinite(results.annualWorkingHours) || !Number.isFinite(results.annualBillableHours) || !Number.isFinite(results.requiredPreTaxRevenue) || !Number.isFinite(results.minimumHourlyRate) || !Number.isFinite(results.recommendedHourlyRate) || !Number.isFinite(results.recommendedDailyRate) || !Number.isFinite(results.monthlyRevenueTarget) || !Number.isFinite(results.estimatedTax)) {
    showError('The calculation resulted in an unsupported value.');
    return;
  }

  if (results.annualWorkingDays <= 0 || results.annualBillableHours <= 0) {
    showError('The working-day and billable-hour assumptions must produce a positive result.');
    return;
  }

  if (results.requiredPreTaxRevenue <= 0 || results.minimumHourlyRate <= 0 || results.recommendedHourlyRate <= 0 || results.recommendedDailyRate <= 0 || results.monthlyRevenueTarget <= 0) {
    showError('The calculation produced an invalid result.');
    return;
  }

  renderResults(results);
}

if (form) {
  form.addEventListener('submit', (event) => {
    event.preventDefault();
    handleCalculation();
  });

  form.addEventListener('input', () => {
    handleCalculation();
  });
}

document.addEventListener('DOMContentLoaded', () => {
  handleCalculation();
});
