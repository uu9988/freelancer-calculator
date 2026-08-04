from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
from pathlib import Path
from urllib.parse import urlsplit


ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://uu9988.github.io/freelancer-calculator/"
PROJECT_PATH = "/freelancer-calculator/"


TOOL_DATA = {
    "freelance-budget-calculator.html": {
        "title": "Freelance Budget Calculator | Plan Income and Expenses",
        "description": "Plan a practical freelance budget by comparing monthly income, business expenses, tax reserves, and personal pay before making spending decisions.",
        "how_heading": "How freelance budget planning works",
        "how": "Start with expected client income, then separate recurring business costs, variable expenses, tax reserves, and the amount available for personal pay. Reviewing the same categories each month makes cash-flow changes easier to spot.",
        "formula_heading": "Freelance budget formula",
        "formula": "Available freelance cash flow = client income - business expenses - tax reserve - personal withdrawals. Use conservative income estimates when client work changes from month to month.",
        "example_heading": "Monthly budget example",
        "example": "If a freelancer expects $6,500 in monthly revenue, $900 in business costs, and a $1,500 tax reserve, $4,100 remains before savings and personal spending.",
        "guide": ("Freelance Budgeting Tips", "blog/freelance-budgeting-tips.html"),
        "group": "business",
    },
    "freelance-business-calculator.html": {
        "title": "Freelance Business Calculator | Plan Revenue and Costs",
        "description": "Compare freelance revenue, operating costs, tax reserves, and target profit to understand whether your independent business plan is sustainable.",
        "how_heading": "How to model a freelance business",
        "how": "List expected revenue by client or service, then account for operating costs, unpaid time, taxes, and the profit you want the business to retain. This separates business performance from gross billings.",
        "formula_heading": "Business planning formula",
        "formula": "Estimated business profit = total freelance revenue - operating expenses - tax reserve. A planning model should also test lower-revenue months instead of relying only on the best-case scenario.",
        "example_heading": "Business planning example",
        "example": "A consultant billing $9,000 in a month with $1,400 in operating costs and a $2,000 tax reserve would plan around $5,600 in remaining business profit before personal withdrawals.",
        "guide": ("Freelance Billing Growth", "blog/freelance-billing-growth.html"),
        "group": "business",
    },
    "freelance-cost-calculator.html": {
        "title": "Freelance Cost Calculator | Estimate Business Costs",
        "description": "Estimate recurring and one-time freelance business costs, convert annual overhead into a monthly amount, and use the result when setting client rates.",
        "how_heading": "How to estimate freelance costs",
        "how": "Separate fixed costs such as software and insurance from variable costs such as subcontracting, travel, and payment fees. Annual expenses can then be converted into monthly or billable-hour amounts.",
        "formula_heading": "Cost allocation formula",
        "formula": "Monthly overhead = annual fixed costs / 12. Cost per billable hour = total annual business costs / realistic annual billable hours.",
        "example_heading": "Overhead example",
        "example": "With $7,200 in annual overhead and 1,200 billable hours, a freelancer needs to recover at least $6 per billable hour before accounting for taxes and personal income.",
        "guide": ("Freelancer Tax Deduction Checklist", "blog/tax-deduction-checklist.html"),
        "group": "business",
    },
    "freelance-expense-calculator.html": {
        "title": "Freelance Expense Calculator | Plan Business Spending",
        "description": "Organize freelance expenses by category, estimate monthly and annual spending, and understand how business costs affect cash flow and pricing decisions.",
        "how_heading": "How expense planning works",
        "how": "Record recurring subscriptions, equipment, professional services, marketing, travel, and transaction fees separately. Categorizing expenses helps distinguish predictable overhead from occasional purchases.",
        "formula_heading": "Expense total formula",
        "formula": "Annual freelance expenses = recurring monthly expenses x 12 + expected one-time expenses. Keep tax deductibility separate because local rules determine which costs qualify.",
        "example_heading": "Expense planning example",
        "example": "Monthly software and insurance of $350 plus $2,400 in planned annual equipment and marketing produces an estimated annual expense total of $6,600.",
        "guide": ("Freelancer Tax Deduction Checklist", "blog/tax-deduction-checklist.html"),
        "group": "business",
    },
    "freelance-hourly-income-calculator.html": {
        "title": "Freelance Hourly Income Calculator | Freelancer Tools",
        "description": "Estimate gross freelance income from an hourly rate, realistic billable hours, and working weeks, then compare the result with expenses and taxes.",
        "how_heading": "How hourly income is estimated",
        "how": "Use the rate clients pay, the hours you can actually invoice, and the number of working weeks in the period. Administrative time should not be counted as billable unless a client pays for it.",
        "formula_heading": "Hourly income formula",
        "formula": "Estimated gross income = hourly rate x billable hours per week x working weeks. Net planning income requires separate deductions for business expenses and taxes.",
        "example_heading": "Hourly earnings example",
        "example": "At $65 per hour, 24 billable hours per week, and 46 working weeks, estimated gross annual freelance income is $71,760 before expenses and taxes.",
        "guide": ("Hourly Rate Calculation Methods", "blog/hourly-rate-calculation-methods.html"),
        "group": "income",
    },
    "freelance-hourly-rate-calculator.html": {
        "title": "Freelance Hourly Rate Calculator | Freelancer Tools",
        "description": "Estimate a sustainable freelance hourly rate from target income, business expenses, taxes, billable capacity, and time away from client work.",
        "how_heading": "How an hourly rate estimate works",
        "how": "Combine the income you want to take home with business costs and taxes, then divide the required revenue by realistic billable hours rather than total working hours.",
        "formula_heading": "Hourly rate planning formula",
        "formula": "Baseline hourly rate = required pre-tax annual revenue / annual billable hours. A contingency margin can then cover scope changes, late payments, and gaps between projects.",
        "example_heading": "Hourly rate example",
        "example": "If required annual revenue is $84,000 and realistic billable capacity is 1,200 hours, the baseline rate is $70 per hour before adding a contingency margin.",
        "guide": ("Hourly Rate Strategy", "blog/hourly-rate-strategy.html"),
        "group": "rates",
    },
    "freelance-hourly-rate-guide.html": {
        "title": "Freelance Hourly Rate Guide | Formula and Examples",
        "description": "Learn how to calculate a sustainable freelance hourly rate using income goals, expenses, taxes, billable hours, and practical pricing examples.",
        "how_heading": "Using the hourly rate guide",
        "how": "Treat an hourly rate as a business calculation rather than a guess. Begin with annual financial needs, estimate billable capacity, and review the result against market context and project risk.",
        "formula_heading": "Rate-setting framework",
        "formula": "Required revenue includes take-home income, business expenses, and taxes. Dividing that amount by realistic billable hours produces a baseline that can be adjusted for risk and experience.",
        "example_heading": "Applying the framework",
        "example": "A freelancer can compare a calculated baseline with project-based pricing, then check whether the chosen method still covers unpaid administration and time between assignments.",
        "guide": ("Hourly Rate Calculation Methods", "blog/hourly-rate-calculation-methods.html"),
        "group": "rates",
    },
    "freelance-income-calculator.html": {
        "title": "Freelance Income Calculator | Estimate Monthly Earnings",
        "description": "Estimate monthly and annual freelance income from client rates and billable capacity, then compare gross earnings with costs, taxes, and income goals.",
        "how_heading": "How freelance income planning works",
        "how": "Estimate income from the work you expect to invoice, not every hour you spend working. Compare gross billings with operating costs, tax reserves, and the amount you want to take home.",
        "formula_heading": "Freelance income formula",
        "formula": "Gross freelance income = average client rate x billable units completed. Planning income = gross income - business expenses - tax reserve.",
        "example_heading": "Income planning example",
        "example": "A freelancer averaging $7,500 in monthly billings with $900 in expenses and a $1,800 tax reserve would plan around $4,800 before savings and other adjustments.",
        "guide": ("Freelance Income Planning", "blog/freelance-income-planning.html"),
        "group": "income",
    },
    "freelance-income-tax-calculator.html": {
        "title": "Freelance Income Tax Calculator | Tax Planning Guide",
        "description": "Plan a freelance income-tax reserve from estimated taxable profit and an assumed tax rate, while keeping local deductions and payment rules in mind.",
        "how_heading": "How income-tax planning works",
        "how": "Estimate taxable freelance profit after eligible business expenses, then apply a planning rate based on the rules that apply where you live. This is a reserve estimate, not a filed tax return.",
        "formula_heading": "Income-tax estimate formula",
        "formula": "Estimated income-tax reserve = estimated taxable freelance profit x assumed effective tax rate. Actual liability can change with deductions, thresholds, and other income.",
        "example_heading": "Tax reserve example",
        "example": "With $60,000 in estimated taxable freelance profit and a 22% planning rate, the preliminary reserve is $13,200 before jurisdiction-specific adjustments.",
        "guide": ("Freelancer Tax Basics", "blog/freelancer-tax-basics.html"),
        "group": "tax",
    },
    "freelance-invoice-calculator.html": {
        "title": "Freelance Invoice Calculator | Estimate Client Billing",
        "description": "Estimate a freelance invoice total from work quantity, rates, expenses, discounts, and applicable taxes before preparing the final client invoice.",
        "how_heading": "How an invoice estimate works",
        "how": "Add each billable service or product, include approved reimbursable expenses, apply any agreed discount, and calculate tax only when it is legally required.",
        "formula_heading": "Invoice total formula",
        "formula": "Invoice subtotal = sum of quantity x unit rate for all line items. Final total = subtotal + approved expenses - discounts + applicable tax.",
        "example_heading": "Invoice calculation example",
        "example": "Ten hours at $80 produces an $800 service subtotal. Adding $50 in approved expenses gives $850 before any discount or applicable tax.",
        "guide": ("Invoice Best Practices", "blog/invoice-best-practices.html"),
        "group": "invoice",
    },
    "freelance-invoice-generator.html": {
        "title": "Freelance Invoice Generator | Plan Professional Invoices",
        "description": "Prepare the information needed for a clear freelance invoice, including client details, line items, payment terms, totals, and a unique invoice number.",
        "how_heading": "How to prepare a freelance invoice",
        "how": "Gather accurate client details, describe each service, record quantities and rates, assign a unique invoice number, and state the due date and accepted payment method.",
        "formula_heading": "Invoice amount check",
        "formula": "Check that line-item quantities multiplied by their rates equal the subtotal, then account for approved expenses, discounts, and any legally required tax.",
        "example_heading": "Invoice preparation example",
        "example": "A design invoice might include a fixed project fee, two approved revision hours, the issue date, a 14-day due date, and clear bank-transfer instructions.",
        "guide": ("Invoice Best Practices", "blog/invoice-best-practices.html"),
        "group": "invoice",
    },
    "freelance-monthly-income-calculator.html": {
        "title": "Freelance Monthly Income Calculator | Earnings Planner",
        "description": "Estimate monthly freelance income from expected client work, then compare gross billings with expenses, tax reserves, and personal income needs.",
        "how_heading": "How monthly income is estimated",
        "how": "List confirmed and likely client work for the month, apply the relevant rate to each assignment, and keep uncertain pipeline revenue separate from contracted revenue.",
        "formula_heading": "Monthly income formula",
        "formula": "Estimated monthly gross income = sum of expected client billings. Planning income = gross billings - monthly expenses - tax reserve.",
        "example_heading": "Monthly earnings example",
        "example": "Three projects expected to bill $2,000, $1,500, and $3,000 produce $6,500 in projected monthly gross income before costs and taxes.",
        "guide": ("Freelance Income Planning", "blog/freelance-income-planning.html"),
        "group": "income",
    },
    "freelance-payment-calculator.html": {
        "title": "Freelance Payment Calculator | Plan Client Payments",
        "description": "Estimate freelance client payments, deposits, milestones, and outstanding balances so invoice timing is easier to plan and explain.",
        "guide": ("Invoice and Payment Workflow", "blog/invoice-payment-workflow.html"),
        "group": "invoice",
    },
    "freelance-pricing-calculator.html": {
        "title": "Freelance Pricing Calculator | Set Sustainable Rates",
        "description": "Compare freelance pricing options using income targets, project scope, costs, billable time, and risk before choosing an hourly or fixed fee.",
        "how_heading": "How freelance pricing is planned",
        "how": "Define the scope and value of the work, calculate the minimum amount needed to cover time and costs, and then account for complexity, revisions, urgency, and delivery risk.",
        "formula_heading": "Pricing baseline formula",
        "formula": "Pricing baseline = estimated delivery hours x sustainable hourly rate + direct project costs. Fixed prices may also include a contingency for uncertainty and revision risk.",
        "example_heading": "Pricing example",
        "example": "A 30-hour project at a sustainable $75 rate has a $2,250 labor baseline. Adding $200 in direct costs produces $2,450 before any contingency.",
        "guide": ("Hourly Rate Strategy", "blog/hourly-rate-strategy.html"),
        "group": "rates",
    },
    "freelance-profit-calculator.html": {
        "title": "Freelance Profit Calculator | Estimate Net Profit",
        "description": "Estimate freelance profit by subtracting business expenses from client revenue, then compare profit margin across services, projects, or time periods.",
        "how_heading": "How freelance profit is measured",
        "how": "Track revenue and the costs required to earn it within the same period. Separate business profit from personal withdrawals so the calculation reflects business performance.",
        "formula_heading": "Freelance profit formula",
        "formula": "Freelance profit = client revenue - business expenses. Profit margin = profit / revenue x 100. Tax is normally planned separately from operating profit.",
        "example_heading": "Profit margin example",
        "example": "A project earning $5,000 with $1,250 in direct and allocated costs produces $3,750 in profit and a 75% pre-tax profit margin.",
        "guide": ("Freelance Billing Growth", "blog/freelance-billing-growth.html"),
        "group": "business",
    },
    "freelance-project-cost-calculator.html": {
        "title": "Freelance Project Cost Calculator | Estimate Job Costs",
        "description": "Estimate freelance project costs from labor, subcontractors, software, travel, and contingency before setting a quote or approving a scope.",
        "how_heading": "How project costs are estimated",
        "how": "Break the project into tasks, estimate labor for each task, add direct purchases and subcontractor fees, and include a contingency for clearly identified uncertainty.",
        "formula_heading": "Project cost formula",
        "formula": "Estimated project cost = labor hours x internal cost rate + direct expenses + subcontractor costs + contingency. Profit is added later when setting the client price.",
        "example_heading": "Project cost example",
        "example": "Forty hours at a $45 internal cost rate plus $300 in software and a $200 contingency produces an estimated project cost of $2,300.",
        "guide": ("Hourly Rate Calculation Methods", "blog/hourly-rate-calculation-methods.html"),
        "group": "rates",
    },
    "freelance-quote-calculator.html": {
        "title": "Freelance Quote Calculator | Estimate Project Prices",
        "description": "Build a freelance quote from estimated work, a sustainable rate, project costs, revisions, and contingency before presenting a price to a client.",
        "how_heading": "How to estimate a freelance quote",
        "how": "Confirm scope and deliverables, estimate the work required, add direct costs, and state assumptions about revisions, deadlines, and items that fall outside the quote.",
        "formula_heading": "Quote estimate formula",
        "formula": "Quote baseline = estimated hours x sustainable rate + direct project costs + contingency. Taxes should be shown separately when local rules require them.",
        "example_heading": "Quote example",
        "example": "A 24-hour assignment at $90 per hour with $150 in direct costs and a $250 contingency produces a quote baseline of $2,560.",
        "guide": ("Hourly Rate Calculation Methods", "blog/hourly-rate-calculation-methods.html"),
        "group": "rates",
    },
    "freelance-rate-calculator.html": {
        "title": "Freelance Rate Calculator | Hourly and Project Pricing",
        "description": "Estimate a freelance rate from annual income needs, costs, taxes, and billable capacity, then compare hourly and project-pricing approaches.",
        "how_heading": "How freelance rates are compared",
        "how": "Calculate a sustainable hourly baseline first, then use project scope and risk to decide whether hourly, daily, or fixed project pricing is the better fit.",
        "formula_heading": "Rate comparison formula",
        "formula": "Hourly baseline = required revenue / billable hours. A project baseline can be estimated by multiplying that rate by delivery hours and adding direct costs and contingency.",
        "example_heading": "Rate comparison example",
        "example": "A $70 hourly baseline applied to a 20-hour project gives $1,400 before direct costs. A fixed quote can then account for revision and schedule risk.",
        "guide": ("Hourly Rate Strategy", "blog/hourly-rate-strategy.html"),
        "group": "rates",
    },
    "freelance-revenue-calculator.html": {
        "title": "Freelance Revenue Calculator | Plan Business Income",
        "description": "Estimate freelance revenue from rates, project volume, and billable capacity, then compare the forecast with costs and annual business targets.",
        "how_heading": "How revenue forecasting works",
        "how": "Estimate billings by client, service, or project and separate contracted revenue from uncertain opportunities. A realistic forecast also accounts for vacation and gaps between assignments.",
        "formula_heading": "Revenue forecast formula",
        "formula": "Projected freelance revenue = sum of expected billable units x their client rates. Revenue is not profit; operating costs and taxes still need separate planning.",
        "example_heading": "Revenue forecast example",
        "example": "Billing 900 hours at an average of $85 per hour produces $76,500 in projected annual revenue before non-hourly projects, costs, and taxes.",
        "guide": ("Freelance Billing Growth", "blog/freelance-billing-growth.html"),
        "group": "business",
    },
    "freelance-salary-calculator.html": {
        "title": "Freelance Salary Calculator | Compare Annual Earnings",
        "description": "Compare freelance revenue with a salary-equivalent target after allowing for business expenses, unpaid time, benefits, and tax planning assumptions.",
        "how_heading": "How salary-equivalent planning works",
        "how": "A salary and freelance revenue are not directly comparable. Add business overhead, unpaid leave, self-funded benefits, and non-billable time to the take-home amount you want to match.",
        "formula_heading": "Salary-equivalent formula",
        "formula": "Required freelance revenue = target personal compensation + business expenses + benefit replacement + tax reserve. The categories should reflect your actual situation.",
        "example_heading": "Salary comparison example",
        "example": "Matching $60,000 in personal compensation may require substantially more than $60,000 in billings once insurance, leave, overhead, and taxes are included.",
        "guide": ("Freelance Income Planning", "blog/freelance-income-planning.html"),
        "group": "income",
    },
    "freelance-tax-calculator.html": {
        "title": "Freelance Tax Calculator | Estimate Tax Set-Asides",
        "description": "Estimate a freelance tax set-aside from projected profit and a planning tax rate, while allowing for local rules, deductions, and payment schedules.",
        "how_heading": "How a freelance tax estimate works",
        "how": "Begin with projected freelance profit rather than gross invoices, then apply a cautious planning rate. Income from other sources and jurisdiction-specific rules can change the final liability.",
        "formula_heading": "Tax set-aside formula",
        "formula": "Estimated tax set-aside = projected taxable freelance profit x assumed effective tax rate. Treat the result as a planning reserve rather than professional tax advice.",
        "example_heading": "Tax planning example",
        "example": "A freelancer projecting $75,000 in taxable profit and using a 25% planning rate would reserve $18,750 over the year, subject to local tax rules.",
        "guide": ("Freelancer Tax Basics", "blog/freelancer-tax-basics.html"),
        "group": "tax",
    },
    "freelance-yearly-income-calculator.html": {
        "title": "Freelance Yearly Income Calculator | Annual Earnings",
        "description": "Estimate annual freelance income from monthly or project billings, then account for seasonal gaps, business costs, taxes, and time away from work.",
        "how_heading": "How annual income is estimated",
        "how": "Combine realistic monthly forecasts or expected projects across the year. Reduce the forecast for planned leave, client gaps, and work that is possible but not yet contracted.",
        "formula_heading": "Yearly income formula",
        "formula": "Estimated annual gross income = sum of projected monthly billings. Planning income = annual gross income - business expenses - tax reserve.",
        "example_heading": "Annual earnings example",
        "example": "Ten months at $7,000 in billings plus two slower months at $4,000 produces $78,000 in projected annual gross freelance income.",
        "guide": ("Freelance Income Planning", "blog/freelance-income-planning.html"),
        "group": "income",
    },
}


POST_DATA = {
    "freelance-calculator-guide.html": {
        "title": "Freelance Calculator Guide for Income, Rates and Taxes",
        "description": "Learn how to choose and use freelance calculators for hourly rates, income, taxes, costs, and invoices without confusing estimates with guaranteed results.",
        "sections": [
            "Freelance calculators turn business assumptions into estimates you can review. The useful starting point is not the tool itself, but the decision you need to make: setting a rate, forecasting income, reserving tax, pricing a project, or checking an invoice.",
            "A calculation becomes misleading when inputs mix gross revenue with take-home income, count every working hour as billable, or ignore business costs. Different decisions also require different formulas, so one result should not be reused for every purpose.",
            "Choose the calculator that matches the decision, enter conservative assumptions, and save the inputs behind the result. Run at least a base case and a lower-income case so the estimate remains useful when work changes.",
            "Suppose a freelancer wants to compare a $70 hourly rate with an annual income target. An hourly-rate tool can test billable capacity, while an income calculator checks the resulting revenue and a tax tool estimates a separate reserve.",
            "Start with the most important decision, document the assumptions, and revisit the estimate when rates, costs, or available hours change. The related tools below cover the main planning steps.",
        ],
    },
    "freelance-income-planning.html": {
        "title": "Freelance Income Planning for More Reliable Earnings",
        "description": "Build a realistic freelance income plan with contracted work, pipeline estimates, expenses, tax reserves, and scenarios for slower client months.",
        "sections": [
            "Reliable freelance income planning separates money already contracted from opportunities that may not close. A monthly view helps independent professionals see when client concentration or seasonal gaps could affect cash flow.",
            "Gross invoices can look healthy while available cash remains tight. Payment delays, business expenses, taxes, and unpaid time all reduce the amount that can safely support personal spending.",
            "Create a base forecast from signed work, add a clearly labeled pipeline scenario, and subtract expected costs and tax reserves. Updating the forecast as invoices are issued and paid keeps it connected to actual cash flow.",
            "Suppose $5,000 is contracted for next month and another $2,500 is only probable. Plan essential spending from the contracted amount, then treat the pipeline revenue as upside until the work is confirmed.",
            "Review monthly and yearly income together. The monthly view protects cash flow, while the annual view shows whether current rates and client volume support the broader income goal.",
        ],
    },
    "hourly-rate-strategy.html": {
        "title": "Freelance Hourly Rate Strategy for Sustainable Pricing",
        "description": "Set a sustainable freelance hourly rate by combining income needs, expenses, taxes, billable capacity, scope risk, and market context.",
        "sections": [
            "A sustainable hourly rate must fund more than the hour spent on a client task. It also supports administration, sales, time away from work, business overhead, and the tax reserve attached to freelance profit.",
            "Rates are often set from a former salary or a competitor's advertised price. Those shortcuts ignore differences in billable hours, benefits, costs, experience, and the uncertainty built into the service being sold.",
            "Calculate a financial baseline first, then compare it with the value and risk of the work. Use clear minimums for small assignments and revisit the rate when expenses, availability, or service positioning changes.",
            "If required annual revenue is $90,000 and realistic billable capacity is 1,200 hours, the baseline is $75 per hour. A difficult scope or tight deadline may justify a higher quote rather than more hidden hours.",
            "Use the baseline as a decision aid, not a promise that every engagement should be billed hourly. Fixed and value-based pricing can still be checked against the same cost and capacity assumptions.",
        ],
    },
    "freelancer-tax-basics.html": {
        "title": "Freelancer Tax Basics for Estimates and Set-Asides",
        "description": "Understand the basics of freelance tax planning, including taxable profit, set-asides, estimated payments, deductions, and the limits of online calculators.",
        "sections": [
            "Freelancers commonly need to plan for taxes without an employer withholding money from each payment. The relevant obligations depend on location and may include income tax, self-employment or social contributions, and other local requirements.",
            "Using gross client revenue as the tax base can overstate the reserve, while ignoring tax entirely creates a cash-flow risk. Eligible expenses, other income, thresholds, and payment schedules can all change the actual amount due.",
            "Track revenue and business expenses, estimate taxable profit, apply a cautious planning rate, and keep the reserve separate from operating cash. Confirm filing and payment obligations with the appropriate local authority or a qualified adviser.",
            "For example, $80,000 of revenue minus $15,000 of eligible business expenses leaves $65,000 of estimated profit before jurisdiction-specific adjustments. A planning percentage can be applied to that estimate, not blindly to invoices.",
            "Update the estimate when profit changes and before scheduled payments. A calculator can organize assumptions, but it cannot determine the correct legal treatment for every person or location.",
        ],
    },
    "invoice-best-practices.html": {
        "title": "Freelance Invoice Best Practices to Get Paid Faster",
        "description": "Create clearer freelance invoices with accurate client details, itemized work, unique numbers, due dates, payment instructions, and consistent follow-up.",
        "sections": [
            "A clear invoice helps a client verify the work, route the document for approval, and pay without requesting missing information. Consistent formatting also makes the freelancer's own records easier to reconcile.",
            "Payments are often delayed by an incorrect billing contact, vague line items, missing purchase-order details, or payment terms that were never agreed before work began.",
            "Confirm billing requirements at project start, use a unique invoice number, itemize services, state the issue and due dates, and include accurate payment instructions. Keep a copy of the approved scope beside the invoice.",
            "A project invoice might list a $2,400 design milestone, an approved $150 expense, the client's purchase-order number, and a 14-day due date. Each amount should match the agreement and subtotal.",
            "Send the invoice to the correct contact, confirm receipt, and follow a consistent reminder schedule. The related tools can help check amounts and plan payment timing.",
        ],
    },
    "freelance-billing-growth.html": {
        "title": "Freelance Billing Growth Without Sacrificing Profit",
        "description": "Grow freelance billings by improving rates, service mix, capacity, and payment discipline while tracking the costs and profit behind higher revenue.",
        "sections": [
            "Higher freelance billings can come from more client work, better rates, larger scopes, or a stronger mix of services. The healthiest growth is the kind that also improves profit and does not depend on unsustainable hours.",
            "Revenue alone can hide extra subcontractor costs, longer delivery time, unpaid revisions, and slow collections. A busy month is not necessarily a profitable one if scope and payment terms are weak.",
            "Measure revenue, delivery cost, effective rate, and payment time by service. Use those numbers to improve pricing, narrow the offer, and decide where additional capacity would create a real return.",
            "If monthly billings rise from $8,000 to $10,000 but delivery costs rise by $2,500, profit has fallen. A smaller increase produced through a rate improvement could create a better result with less workload.",
            "Review growth with revenue and profit calculators together. That keeps attention on cash collected and value retained, not only the amount invoiced.",
        ],
    },
    "freelance-budgeting-tips.html": {
        "title": "Freelance Budgeting Tips for Income, Costs and Taxes",
        "description": "Build a freelance budget that handles uneven income, recurring expenses, tax reserves, emergency savings, and realistic personal withdrawals.",
        "sections": [
            "Freelance budgets need to handle income that changes from month to month. A useful plan separates business obligations from personal spending and creates room for taxes, quieter periods, and necessary equipment.",
            "A budget based on the best recent month can make recurring commitments too large. It also becomes difficult to tell whether cash in the account belongs to the business, a tax reserve, or personal pay.",
            "Use a conservative income baseline, list fixed and variable costs, reserve taxes as revenue arrives, and set a repeatable personal withdrawal. Keep an emergency buffer for late invoices and gaps between projects.",
            "If revenue varies between $5,000 and $9,000, build essential spending around the lower sustainable level. Higher months can replenish tax, equipment, and emergency reserves before increasing personal withdrawals.",
            "Update the budget with actual results each month. The goal is not a perfect forecast; it is a clear decision process when income or costs change.",
        ],
    },
    "hourly-rate-calculation-methods.html": {
        "title": "Hourly Rate Calculation Methods for Freelancers",
        "description": "Compare income-based, cost-based, salary-equivalent, project-conversion, and value-aware methods for calculating freelance hourly rates.",
        "sections": [
            "Freelancers can calculate an hourly rate from income needs, business costs, salary comparisons, or project economics. Each method answers a slightly different question, so the chosen inputs should match the pricing decision.",
            "A cost-only method may cover expenses but miss personal income and taxes. A salary conversion may overlook unpaid time, while a competitor comparison says little about the freelancer's own capacity or service value.",
            "Use an income-and-cost baseline for financial sustainability, then compare it with project scope, market context, and the value delivered. Converting completed project fees back to an effective hourly rate provides a useful reality check.",
            "A $3,000 project that takes 30 delivery hours has a $100 effective delivery rate. If sales, meetings, and revisions add 10 more hours, the true effective rate is $75.",
            "No single method is correct for every service. Compare at least two approaches and update estimates with actual project time to improve future pricing.",
        ],
    },
    "tax-deduction-checklist.html": {
        "title": "Freelancer Tax Deduction Checklist for Expenses",
        "description": "Organize potential freelance tax deductions with records for software, equipment, workspace, professional services, travel, and other business costs.",
        "sections": [
            "A deduction checklist helps freelancers capture business expenses consistently and keep supporting records near the transaction. Eligibility still depends on local rules and the business purpose of each cost.",
            "Waiting until a filing deadline makes receipts harder to find and personal purchases harder to separate. Missing documentation can also make an otherwise legitimate business cost difficult to support.",
            "Create categories that match the business, record the date, supplier, amount, currency, and purpose, and retain the invoice or receipt. Mark uncertain items for professional review instead of assuming they qualify.",
            "A software subscription used only for client work may be straightforward to record. A home internet bill or mixed-use device may require an allocation supported by local rules and actual business use.",
            "Review the checklist monthly and reconcile it with payment records. Use an expense calculator for totals, but rely on official guidance or a qualified adviser for deductibility.",
        ],
    },
    "invoice-payment-workflow.html": {
        "title": "Freelance Invoice and Payment Workflow Guide",
        "description": "Create a repeatable freelance invoice workflow from scope approval and invoice checks through delivery, reminders, payment matching, and recordkeeping.",
        "sections": [
            "A consistent invoice workflow begins before the invoice is created. Scope, price, billing contact, approval requirements, payment method, and due date should be agreed while the project is being set up.",
            "Without a workflow, invoices may contain inconsistent totals, go to the wrong contact, or remain overdue without a clear follow-up date. The freelancer also loses visibility into expected cash flow.",
            "Confirm completed work, calculate the total, issue a uniquely numbered invoice, record the due date, and schedule reminders. When payment arrives, match it to the invoice and store the supporting record.",
            "For a milestone completed on August 3 with 14-day terms, issue the invoice promptly, record an August 17 due date, and schedule a courteous reminder based on the agreed process.",
            "Review outstanding invoices at least weekly. The related payment and invoice tools can help check amounts, deposits, balances, and timing before a document is sent.",
        ],
    },
}


GROUPS = {
    "business": [
        ("Freelance Business Calculator", "freelance-business-calculator.html"),
        ("Freelance Budget Calculator", "freelance-budget-calculator.html"),
        ("Freelance Cost Calculator", "freelance-cost-calculator.html"),
        ("Freelance Expense Calculator", "freelance-expense-calculator.html"),
        ("Freelance Profit Calculator", "freelance-profit-calculator.html"),
        ("Freelance Revenue Calculator", "freelance-revenue-calculator.html"),
    ],
    "income": [
        ("Freelance Income Calculator", "freelance-income-calculator.html"),
        ("Freelance Hourly Income Calculator", "freelance-hourly-income-calculator.html"),
        ("Freelance Monthly Income Calculator", "freelance-monthly-income-calculator.html"),
        ("Freelance Yearly Income Calculator", "freelance-yearly-income-calculator.html"),
        ("Freelance Salary Calculator", "freelance-salary-calculator.html"),
        ("Freelance Revenue Calculator", "freelance-revenue-calculator.html"),
    ],
    "rates": [
        ("Freelance Hourly Rate Calculator", "freelance-hourly-rate-calculator.html"),
        ("Freelance Rate Calculator", "freelance-rate-calculator.html"),
        ("Freelance Pricing Calculator", "freelance-pricing-calculator.html"),
        ("Freelance Quote Calculator", "freelance-quote-calculator.html"),
        ("Freelance Project Cost Calculator", "freelance-project-cost-calculator.html"),
        ("Freelance Hourly Rate Guide", "freelance-hourly-rate-guide.html"),
    ],
    "tax": [
        ("Freelance Tax Calculator", "freelance-tax-calculator.html"),
        ("Freelance Income Tax Calculator", "freelance-income-tax-calculator.html"),
        ("Freelance Expense Calculator", "freelance-expense-calculator.html"),
        ("Freelance Income Calculator", "freelance-income-calculator.html"),
        ("Freelance Profit Calculator", "freelance-profit-calculator.html"),
    ],
    "invoice": [
        ("Freelance Invoice Calculator", "freelance-invoice-calculator.html"),
        ("Freelance Invoice Generator", "freelance-invoice-generator.html"),
        ("Freelance Payment Calculator", "freelance-payment-calculator.html"),
        ("Freelance Quote Calculator", "freelance-quote-calculator.html"),
        ("Freelance Project Cost Calculator", "freelance-project-cost-calculator.html"),
    ],
}


def replace_one(text: str, pattern: str, replacement: str) -> str:
    if not re.search(pattern, text, flags=re.I | re.S):
        raise ValueError(f"Required pattern not found: {pattern[:80]}")
    return re.sub(pattern, lambda _: replacement, text, count=1, flags=re.I | re.S)


def ensure_meta(text: str, name: str, content: str, after_pattern: str) -> str:
    pattern = rf'<meta[^>]+name=["\']{re.escape(name)}["\'][^>]*>'
    tag = f'<meta name="{name}" content="{content}" />'
    if re.search(pattern, text, flags=re.I):
        return re.sub(pattern, tag, text, count=1, flags=re.I)
    match = re.search(after_pattern, text, flags=re.I)
    if not match:
        raise ValueError(f"Could not insert meta {name}")
    return text[: match.end()] + "\n    " + tag + text[match.end() :]


def set_head_metadata(
    text: str,
    *,
    title: str,
    description: str,
    canonical: str | None,
    robots: str,
    favicon: str,
    og_type: str = "website",
) -> str:
    text = replace_one(text, r"<title[^>]*>.*?</title>", f"<title>{title}</title>")
    text = ensure_meta(text, "description", description, r"<title[^>]*>.*?</title>")
    canonical_pattern = r'<link[^>]+rel=["\']canonical["\'][^>]*>'
    if canonical:
        canonical_tag = f'<link rel="canonical" href="{canonical}" />'
        if re.search(canonical_pattern, text, flags=re.I):
            text = re.sub(canonical_pattern, canonical_tag, text, count=1, flags=re.I)
        else:
            meta_match = re.search(r'<meta[^>]+name=["\']description["\'][^>]*>', text, flags=re.I)
            text = text[: meta_match.end()] + "\n    " + canonical_tag + text[meta_match.end() :]
    else:
        text = re.sub(r"\s*" + canonical_pattern, "", text, count=1, flags=re.I)
    text = ensure_meta(text, "robots", robots, canonical_pattern if canonical else r'<meta[^>]+name=["\']description["\'][^>]*>')
    text = re.sub(
        r'<link[^>]+rel=["\'](?:shortcut )?icon["\'][^>]*>',
        f'<link rel="icon" href="{favicon}" type="image/svg+xml" />',
        text,
        count=1,
        flags=re.I,
    )
    social = {
        "og:title": title,
        "og:description": description,
        "og:type": og_type,
        "og:url": canonical or "",
        "og:site_name": "Freelancer Calculator Hub",
    }
    for prop, value in social.items():
        pattern = rf'<meta[^>]+property=["\']{re.escape(prop)}["\'][^>]*>'
        tag = f'<meta property="{prop}" content="{value}" />'
        if re.search(pattern, text, flags=re.I):
            text = re.sub(pattern, tag, text, count=1, flags=re.I)
        else:
            icon_match = re.search(r'<link[^>]+rel=["\'](?:shortcut )?icon["\'][^>]*>', text, flags=re.I)
            text = text[: icon_match.end()] + "\n    " + tag + text[icon_match.end() :]
    text = ensure_meta(text, "twitter:card", "summary", r'<meta[^>]+property=["\']og:site_name["\'][^>]*>')
    text = ensure_meta(text, "twitter:title", title, r'<meta[^>]+name=["\']twitter:card["\'][^>]*>')
    text = ensure_meta(text, "twitter:description", description, r'<meta[^>]+name=["\']twitter:title["\'][^>]*>')
    text = re.sub(r'\s*<meta[^>]+(?:property|name)=["\'](?:og:image|twitter:image|twitter:site)["\'][^>]*>', "", text, flags=re.I)
    return text


def set_jsonld(text: str, schemas: list[dict]) -> str:
    head = re.search(r"<head>(.*?)</head>", text, flags=re.I | re.S)
    if not head:
        raise ValueError("Missing head element")
    body = re.sub(
        r'\s*<script[^>]+type=["\']application/ld\+json["\'][^>]*>.*?</script>',
        "",
        head.group(1),
        flags=re.I | re.S,
    )
    blocks = "".join(
        "\n    <script type=\"application/ld+json\">\n"
        + json.dumps(schema, indent=2, ensure_ascii=False)
        + "\n    </script>"
        for schema in schemas
    )
    new_head = "<head>" + body.rstrip() + blocks + "\n  </head>"
    return text[: head.start()] + new_head + text[head.end() :]


def clean_text(value: str) -> str:
    return " ".join(html.unescape(re.sub(r"<[^>]+>", " ", value)).split())


def visible_faq(text: str) -> list[tuple[str, str]]:
    return [
        (clean_text(match.group(1)), clean_text(match.group(2)))
        for match in re.finditer(
            r"<details[^>]*>\s*<summary>(.*?)</summary>\s*<p[^>]*>(.*?)</p>\s*</details>",
            text,
            flags=re.I | re.S,
        )
    ]


def page_schema(schema_type: str, name: str, description: str, url: str) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": schema_type,
        "name": name,
        "description": description,
        "url": url,
        "inLanguage": "en",
    }


def faq_schema(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
            for question, answer in items
        ],
    }


def normalize_root_navigation(text: str) -> str:
    text = re.sub(
        r'^[ \t]*<a href=["\'](?:blog\.html|blog/)["\']>Blog</a>[ \t]*\r?\n?',
        "",
        text,
        flags=re.I | re.M,
    )
    text = re.sub(
        r'^(?P<indent>[ \t]*)<a href="index\.html">Home</a>[ \t]*$',
        lambda m: f'{m.group("indent")}<a href="{PROJECT_PATH}">Home</a>\n{m.group("indent")}<a href="{PROJECT_PATH}blog/">Blog</a>',
        text,
        flags=re.M,
    )
    text = re.sub(r'(<a href="/freelancer-calculator/blog/">Blog</a>)\r?\n[ \t]*\r?\n', r"\1\n", text)
    footer = re.search(r'<div class="footer-nav">.*?</div>', text, flags=re.I | re.S)
    if footer:
        block = re.sub(
            r'\s*<a href="(?:/freelancer-calculator/)?changelog\.html">Changelog</a>',
            "",
            footer.group(0),
            flags=re.I,
        )
        block = block.replace(
            f'<a href="{PROJECT_PATH}about.html">About</a>',
            f'<a href="{PROJECT_PATH}about.html">About</a>\n          <a href="{PROJECT_PATH}changelog.html">Changelog</a>',
        )
        text = text[: footer.start()] + block + text[footer.end() :]
    return text


def normalize_blog_navigation(text: str) -> str:
    text = re.sub(
        r'^[ \t]*<a href=["\'](?:\.\./blog\.html|index\.html)["\']>Blog</a>[ \t]*\r?\n?',
        "",
        text,
        flags=re.I | re.M,
    )
    text = re.sub(
        r'^(?P<indent>[ \t]*)<a href="\.\./index\.html">Home</a>[ \t]*$',
        lambda m: f'{m.group("indent")}<a href="{PROJECT_PATH}">Home</a>\n{m.group("indent")}<a href="{PROJECT_PATH}blog/">Blog</a>',
        text,
        flags=re.M,
    )
    text = re.sub(r'(<a href="/freelancer-calculator/blog/">Blog</a>)\r?\n[ \t]*\r?\n', r"\1\n", text)
    footer = re.search(r'<div class="footer-nav">.*?</div>', text, flags=re.I | re.S)
    if footer:
        block = re.sub(
            r'\s*<a href="(?:\.\./|/freelancer-calculator/)changelog\.html">Changelog</a>',
            "",
            footer.group(0),
            flags=re.I,
        )
        block = block.replace(
            f'<a href="{PROJECT_PATH}about.html">About</a>',
            f'<a href="{PROJECT_PATH}about.html">About</a>\n          <a href="{PROJECT_PATH}changelog.html">Changelog</a>',
        )
        text = text[: footer.start()] + block + text[footer.end() :]
    return text


def custom_tool_section(data: dict) -> str:
    return f'''      <section class="page-section planning-notes">
        <div class="container content-card">
          <h2>{data["how_heading"]}</h2>
          <p>{data["how"]}</p>
          <h2>{data["formula_heading"]}</h2>
          <p>{data["formula"]}</p>
          <h2>{data["example_heading"]}</h2>
          <p>{data["example"]}</p>
        </div>
      </section>'''


def related_tool_section(filename: str, data: dict) -> str:
    links = [item for item in GROUPS[data["group"]] if item[1] != filename][:5]
    items = "\n".join(f'            <li><a href="{href}">{label}</a></li>' for label, href in links)
    guide_label, guide_href = data["guide"]
    return f'''    <section class="related-tools">
      <div class="container content-card">
        <h2>Related tools</h2>
        <p>Compare this estimate with other planning tools that cover the same freelance decision from a different angle.</p>
        <ul class="related-list">
{items}
        </ul>
        <p>Related reading: <a href="{guide_href}">{guide_label}</a>.</p>
      </div>
    </section>'''


def repair_tool_page(path: Path, data: dict) -> str:
    text = path.read_text(encoding="utf-8")
    url = BASE_URL + path.name
    text = set_head_metadata(
        text,
        title=data["title"],
        description=data["description"],
        canonical=url,
        robots="index,follow",
        favicon="favicon.svg",
    )
    text = normalize_root_navigation(text)
    if "how_heading" in data:
        generic = (
            r'\s*<section class="page-section">\s*<div class="container content-card">\s*'
            r'<h2>How it works</h2>\s*<p>This section explains how the calculator works and how it helps freelancers estimate their results\.</p>.*?'
            r'</div>\s*</section>'
        )
        if re.search(generic, text, flags=re.I | re.S):
            text = re.sub(generic, "\n" + custom_tool_section(data), text, count=1, flags=re.I | re.S)
    if path.name == "freelance-payment-calculator.html" and "For a $4,000 project with a 40% deposit" not in text:
        text = text.replace(
            """          </ul>
          <h2>FAQ</h2>""",
            """          </ul>
          <p>For a $4,000 project with a 40% deposit, the client pays $1,600 before work begins. Two 25% milestones would be $1,000 each, leaving a $400 final balance. Recording each stage against the agreed schedule makes the outstanding amount clear.</p>
          <h2>FAQ</h2>""",
            1,
        )
    text = re.sub(
        r'^[ \t]*<section class="related-tools">.*?</section>',
        lambda _: related_tool_section(path.name, data),
        text,
        count=1,
        flags=re.I | re.M | re.S,
    )
    faqs = visible_faq(text)
    schemas = [page_schema("WebPage", data["title"], data["description"], url)]
    if faqs:
        schemas.append(faq_schema(faqs))
    return set_jsonld(text, schemas)


def wrap_faq_section(text: str, heading: str, items: list[tuple[str, str]]) -> str:
    details = "\n".join(
        f'''          <details>
            <summary>{question}</summary>
            <p>{answer}</p>
          </details>'''
        for question, answer in items
    )
    section = f'''      <section class="page-section">
        <div class="container content-card">
          <h2>{heading}</h2>
{details}
        </div>
      </section>'''
    pattern = r'\s*<h2>Frequently Asked Questions</h2>\s*(?:<details>.*?</details>\s*)+(?=</main>)'
    if re.search(pattern, text, flags=re.I | re.S):
        return re.sub(pattern, "\n" + section + "\n    ", text, count=1, flags=re.I | re.S)
    if f"<h2>{heading}</h2>" in text:
        return text
    raise ValueError("Unwrapped FAQ block not found")


def replace_related_section(text: str, heading: str, paragraph: str, links: list[tuple[str, str]]) -> str:
    items = "\n".join(f'            <li><a href="{href}">{label}</a></li>' for label, href in links)
    section = f'''    <section class="related-tools">
      <div class="container content-card">
        <h2>{heading}</h2>
        <p>{paragraph}</p>
        <ul class="related-list">
{items}
        </ul>
      </div>
    </section>'''
    return re.sub(
        r'^[ \t]*<section class="related-tools">.*?</section>',
        section,
        text,
        count=1,
        flags=re.I | re.M | re.S,
    )


def repair_basic_pages(changes: dict[Path, str]) -> None:
    configs = {
        "about.html": (
            "About Freelancer Calculator Hub",
            "Learn how Freelancer Calculator Hub helps freelancers, consultants, and independent professionals plan rates, income, costs, taxes, and project pricing.",
            "AboutPage",
        ),
        "contact.html": (
            "Contact Freelancer Calculator Hub",
            "Contact Freelancer Calculator Hub with feedback, corrections, or questions about the site's freelance rate, income, cost, tax, and invoice resources.",
            "ContactPage",
        ),
        "privacy.html": (
            "Privacy Policy | Freelancer Calculator Hub",
            "Read how Freelancer Calculator Hub handles calculator inputs, browser storage, third-party resources, and other privacy considerations on this static site.",
            "WebPage",
        ),
        "terms.html": (
            "Terms of Use | Freelancer Calculator Hub",
            "Review the terms, limitations, and informational-use disclaimer for the freelance calculators and planning resources on Freelancer Calculator Hub.",
            "WebPage",
        ),
        "changelog.html": (
            "Changelog | Freelancer Calculator Hub",
            "Review recent Freelancer Calculator Hub updates, including new calculator resources, content improvements, technical SEO fixes, and maintenance changes.",
            "WebPage",
        ),
    }
    for filename, (title, description, schema_type) in configs.items():
        path = ROOT / filename
        text = path.read_text(encoding="utf-8")
        text = set_head_metadata(
            text,
            title=title,
            description=description,
            canonical=BASE_URL + filename,
            robots="index,follow",
            favicon="favicon.svg",
        )
        text = normalize_root_navigation(text)
        if filename == "about.html":
            text = wrap_faq_section(
                text,
                "Frequently asked questions",
                [
                    ("How accurate are these calculators?", "They provide estimates based on your inputs and help you understand planning assumptions, but they are not professional advice."),
                    ("Can I use these tools for my freelance business?", "Yes, they are built to support freelancers with rate planning, income targets, budgeting, and project estimates."),
                ],
            )
        elif filename == "privacy.html":
            text = text.replace(
                "<h2>Introduction</h2>\n          <p>Freelancer Calculator Hub supports independent professionals with practical online tools for planning rates, income, and business expenses.</p>\n          <h2>Why this site exists</h2>\n          <p>These static tools make it easier to explore pricing and profit scenarios quickly without signing up or installing anything.</p>",
                "<h2>About this privacy policy</h2>\n          <p>This policy explains how the current static site handles calculator inputs and the limited technical data associated with external resources.</p>\n          <h2>How calculator data is handled</h2>\n          <p>Calculator inputs are processed in your browser. The hourly rate calculator may save those inputs in your browser's local storage so they remain available on the same device.</p>",
            )
            text = text.replace(
                "If you later add analytics or advertising tools, their privacy terms\n            should be disclosed here.",
                "The site loads a CDN-hosted chart library to display calculator results. That provider may process technical request data under its own privacy terms.",
            )
            text = text.replace(
                "The site may load third-party resources such as advertising scripts and a CDN-hosted chart library. Those providers may process technical data under their own privacy terms.",
                "The site loads a CDN-hosted chart library to display calculator results. That provider may process technical request data under its own privacy terms.",
            )
            text = text.replace(
                "<summary>Does the site load third-party resources?</summary>\n            <p>Yes. The site may load advertising scripts and a CDN-hosted chart library, which are governed by their providers' privacy terms.</p>",
                "<summary>Does the site load a third-party resource?</summary>\n            <p>Yes. The calculator loads a CDN-hosted chart library, which is governed by that provider's privacy terms.</p>",
            )
            text = replace_related_section(
                text,
                "Related site information",
                "Review the site's usage terms or use the contact page if you have a privacy question or correction.",
                [("Terms of Use", "terms.html"), ("Contact", "contact.html"), ("About this site", "about.html")],
            )
            text = wrap_faq_section(
                text,
                "Privacy questions",
                [
                    ("Does the calculator send my inputs to a site database?", "No. The current site has no account system or backend database, and calculator inputs are processed in your browser."),
                    ("Can calculator inputs remain on my device?", "Yes. The hourly rate calculator may use browser local storage so your inputs remain available on the same device until that storage is cleared."),
                    ("Does the site load a third-party resource?", "Yes. The calculator loads a CDN-hosted chart library, which is governed by that provider's privacy terms."),
                ],
            )
        elif filename == "terms.html":
            text = text.replace(
                "<h2>Introduction</h2>\n          <p>Freelancer Calculator Hub supports independent professionals with practical online tools for planning rates, income, and business expenses.</p>\n          <h2>Why this site exists</h2>\n          <p>These static tools make it easier to explore pricing and profit scenarios quickly without signing up or installing anything.</p>",
                "<h2>Using this site</h2>\n          <p>These terms apply to the calculators, guides, and planning resources available on Freelancer Calculator Hub.</p>\n          <h2>Informational estimates</h2>\n          <p>Results depend on the values and assumptions entered by each user and should be checked before they are used for business decisions.</p>",
            )
            text = replace_related_section(
                text,
                "Related site information",
                "Review the privacy policy or contact the site if you have a question about these terms.",
                [("Privacy Policy", "privacy.html"), ("Contact", "contact.html"), ("About this site", "about.html")],
            )
            text = wrap_faq_section(
                text,
                "Questions about these terms",
                [
                    ("Are calculator results professional financial, tax, or legal advice?", "No. The tools provide informational estimates and are not a substitute for advice from a qualified professional."),
                    ("Who is responsible for reviewing calculator assumptions?", "Each user is responsible for checking their inputs, assumptions, and results before making business or financial decisions."),
                ],
            )
        faqs = visible_faq(text)
        schemas = [page_schema(schema_type, title, description, BASE_URL + filename)]
        if faqs:
            schemas.append(faq_schema(faqs))
        changes[path] = set_jsonld(text, schemas)


def repair_home(changes: dict[Path, str]) -> None:
    path = ROOT / "index.html"
    title = "Freelance Hourly Rate Calculator | Freelancer Calculator Hub"
    description = "Use this free freelance hourly rate calculator and related freelancer tools to plan income, costs, taxes, invoices, and sustainable client pricing."
    text = path.read_text(encoding="utf-8")
    text = set_head_metadata(
        text,
        title=title,
        description=description,
        canonical=BASE_URL,
        robots="index,follow",
        favicon="favicon.svg",
    )
    text = normalize_root_navigation(text)
    text = text.replace("<h3>Frequently Asked Questions</h3>", "<h3>Common setup questions</h3>")
    marker = """            <p class="hero-note">
              This free calculator helps freelancers price services with confidence,
              plan for taxes, and compare different income scenarios.
            </p>"""
    addition = marker + """
            <p class="hero-note">
              Built for freelancers, consultants, and independent professionals, the hub also connects rate planning with income, cost, tax, invoice, and project-pricing resources.
            </p>"""
    if "Built for freelancers, consultants" not in text:
        text = text.replace(marker, addition)
    schemas = [
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": "Freelancer Calculator Hub",
            "url": BASE_URL,
            "description": "Free calculator tools and planning resources for freelance rates, income, costs, taxes, invoices, and project pricing.",
            "inLanguage": "en",
        },
        {
            "@context": "https://schema.org",
            "@type": "WebApplication",
            "name": "Freelance Hourly Rate Calculator",
            "description": "Estimate a sustainable freelance hourly rate from income goals, business expenses, taxes, work schedules, and realistic billable time.",
            "url": BASE_URL,
            "applicationCategory": "BusinessApplication",
            "operatingSystem": "Any",
            "offers": {"@type": "Offer", "price": "0", "priceCurrency": "USD"},
        },
        faq_schema(visible_faq(text)),
    ]
    changes[path] = set_jsonld(text, schemas)


def repair_404_and_template(changes: dict[Path, str]) -> None:
    path = ROOT / "404.html"
    text = path.read_text(encoding="utf-8")
    text = set_head_metadata(
        text,
        title="Page Not Found | Freelancer Calculator Hub",
        description="The requested Freelancer Calculator Hub page could not be found. Return to the homepage or use the navigation to explore available freelance tools.",
        canonical=None,
        robots="noindex,follow",
        favicon="favicon.svg",
    )
    text = text.replace(
        '<meta property="og:url" content="" />',
        f'<meta property="og:url" content="{BASE_URL}404.html" />',
    )
    text = normalize_root_navigation(text)
    changes[path] = set_jsonld(text, [])

    path = ROOT / "blog" / "post-template.html"
    text = path.read_text(encoding="utf-8")
    text = set_head_metadata(
        text,
        title="Blog Post Template | Not for Indexing",
        description="Internal template used to prepare future Freelancer Calculator Hub blog posts.",
        canonical=None,
        robots="noindex,nofollow",
        favicon=PROJECT_PATH + "favicon.svg",
        og_type="article",
    )
    text = re.sub(r'\s*<meta[^>]+property=["\']og:[^"\']+["\'][^>]*>', "", text, flags=re.I)
    text = re.sub(r'\s*<meta[^>]+name=["\']twitter:[^"\']+["\'][^>]*>', "", text, flags=re.I)
    text = normalize_blog_navigation(text)
    text = text.replace("[" + "TITLE]", "{{POST_TITLE}}")
    changes[path] = set_jsonld(text, [])


def repair_blog(changes: dict[Path, str]) -> None:
    path = ROOT / "blog" / "index.html"
    title = "Freelance Calculator Blog | Rates, Income and Tax"
    description = "Read practical freelance guides about hourly rates, income planning, business costs, taxes, invoices, payments, and sustainable independent work."
    text = path.read_text(encoding="utf-8")
    text = set_head_metadata(
        text,
        title=title,
        description=description,
        canonical=BASE_URL + "blog/",
        robots="index,follow",
        favicon="../favicon.svg",
    )
    text = normalize_blog_navigation(text)
    changes[path] = set_jsonld(text, [page_schema("CollectionPage", title, description, BASE_URL + "blog/")])

    path = ROOT / "blog.html"
    title = "Freelance Calculator Blog Directory"
    description = "Alternate directory for Freelancer Calculator Hub articles about freelance rates, income, costs, taxes, invoices, payments, and business planning."
    text = path.read_text(encoding="utf-8")
    text = set_head_metadata(
        text,
        title=title,
        description=description,
        canonical=BASE_URL + "blog/",
        robots="noindex,follow",
        favicon=PROJECT_PATH + "favicon.svg",
    )
    text = normalize_root_navigation(text)
    changes[path] = set_jsonld(text, [])

    section_names = ["Introduction", "Problem", "Solution", "Example", "Next Steps"]
    for filename, data in POST_DATA.items():
        path = ROOT / "blog" / filename
        url = BASE_URL + "blog/" + filename
        text = path.read_text(encoding="utf-8")
        text = set_head_metadata(
            text,
            title=data["title"],
            description=data["description"],
            canonical=url,
            robots="index,follow",
            favicon="../favicon.svg",
            og_type="article",
        )
        text = normalize_blog_navigation(text)
        text = replace_one(text, r"<h1>.*?</h1>", f'<h1>{data["title"]}</h1>')
        for heading, paragraph in zip(section_names, data["sections"]):
            pattern = rf"(<h2>{re.escape(heading)}</h2>\s*)<p>.*?</p>"
            if re.search(pattern, text, flags=re.I | re.S):
                text = re.sub(
                    pattern,
                    lambda match: match.group(1) + f"<p>{paragraph}</p>",
                    text,
                    count=1,
                    flags=re.I | re.S,
                )
            elif re.search(r"\\1<p>.*?</p>", text, flags=re.I | re.S):
                # Repairs output from the first development version of this script,
                # which wrote a literal backreference instead of the heading.
                text = re.sub(
                    r"\\1<p>.*?</p>",
                    lambda _: f"<h2>{heading}</h2>\n          <p>{paragraph}</p>",
                    text,
                    count=1,
                    flags=re.I | re.S,
                )
            else:
                raise ValueError(f"Missing article section: {filename} / {heading}")
        schemas = [
            {
                "@context": "https://schema.org",
                "@type": "Article",
                "headline": data["title"],
                "description": data["description"],
                "mainEntityOfPage": {"@type": "WebPage", "@id": url},
                "inLanguage": "en",
            },
            faq_schema(visible_faq(text)),
        ]
        changes[path] = set_jsonld(text, schemas)


def repair_sitemaps_and_robots(changes: dict[Path, str]) -> None:
    changes[ROOT / "sitemap.xml"] = f'''<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>{BASE_URL}pages-sitemap.xml</loc>
  </sitemap>
  <sitemap>
    <loc>{BASE_URL}tools-sitemap.xml</loc>
  </sitemap>
  <sitemap>
    <loc>{BASE_URL}blog/sitemap.xml</loc>
  </sitemap>
</sitemapindex>
'''
    page_entries = [
        (BASE_URL, "weekly", "1.0"),
        (BASE_URL + "about.html", "monthly", "0.6"),
        (BASE_URL + "contact.html", "monthly", "0.6"),
        (BASE_URL + "privacy.html", "monthly", "0.5"),
        (BASE_URL + "terms.html", "monthly", "0.5"),
        (BASE_URL + "changelog.html", "monthly", "0.4"),
    ]
    page_xml = "\n".join(
        f"  <url>\n    <loc>{url}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{priority}</priority>\n  </url>"
        for url, freq, priority in page_entries
    )
    changes[ROOT / "pages-sitemap.xml"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + page_xml
        + "\n</urlset>\n"
    )
    tool_xml = "\n".join(
        f"  <url>\n    <loc>{BASE_URL}{filename}</loc>\n    <changefreq>monthly</changefreq>\n    <priority>0.8</priority>\n  </url>"
        for filename in TOOL_DATA
    )
    changes[ROOT / "tools-sitemap.xml"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + tool_xml
        + "\n</urlset>\n"
    )
    post_urls = [BASE_URL + "blog/" + filename for filename in POST_DATA]
    urls = [(BASE_URL + "blog/", "weekly", "0.9")] + [(url, "monthly", "0.7") for url in post_urls]
    entries = "\n".join(
        f"  <url>\n    <loc>{url}</loc>\n    <changefreq>{freq}</changefreq>\n    <priority>{priority}</priority>\n  </url>"
        for url, freq, priority in urls
    )
    changes[ROOT / "blog" / "sitemap.xml"] = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + entries
        + "\n</urlset>\n"
    )
    robots = (ROOT / "robots.txt").read_text(encoding="utf-8")
    robots = "\n".join(line for line in robots.splitlines() if "rss.xml" not in line).rstrip() + "\n"
    changes[ROOT / "robots.txt"] = robots

    rss_items = "\n".join(
        f'''    <item>
      <title>{data["title"]}</title>
      <link>{BASE_URL}blog/{filename}</link>
      <guid>{BASE_URL}blog/{filename}</guid>
      <description>{data["description"]}</description>
      <pubDate>Sat, 02 Aug 2026 00:00:00 GMT</pubDate>
    </item>'''
        for filename, data in POST_DATA.items()
    )
    changes[ROOT / "rss.xml"] = f'''<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Freelancer Calculator Hub Blog</title>
    <link>{BASE_URL}blog/</link>
    <description>Latest blog content from Freelancer Calculator Hub for freelancers on income planning, rates, taxes, invoices, and business growth.</description>
    <language>en-US</language>
    <lastBuildDate>Sat, 02 Aug 2026 00:00:00 GMT</lastBuildDate>
    <pubDate>Sat, 02 Aug 2026 00:00:00 GMT</pubDate>
{rss_items}
  </channel>
</rss>
'''


def normalize_project_reference(source: Path, value: str) -> str:
    """Return a GitHub Pages project-root URL for a local href/src value."""
    parsed = urlsplit(html.unescape(value.strip()))
    if (
        parsed.scheme
        or parsed.netloc
        or not parsed.path
        or parsed.path.startswith(PROJECT_PATH)
        or parsed.path.startswith("/")
    ):
        return value

    relative_source = source.relative_to(ROOT).as_posix()
    resolved = posixpath.normpath(posixpath.join(posixpath.dirname(relative_source), parsed.path))
    if resolved == ".." or resolved.startswith("../"):
        return value
    if resolved == "index.html":
        target = PROJECT_PATH
    elif resolved == "blog/index.html" or (resolved == "blog" and parsed.path.endswith("/")):
        target = PROJECT_PATH + "blog/"
    else:
        target = PROJECT_PATH + resolved
    if parsed.query:
        target += "?" + parsed.query
    if parsed.fragment:
        target += "#" + parsed.fragment
    return target


def normalize_html_project_paths(changes: dict[Path, str]) -> None:
    """Make local HTML references independent of the current browser directory."""
    attribute_pattern = re.compile(r'\b(?P<attr>href|src)=(?P<quote>["\'])(?P<value>.*?)(?P=quote)', re.I)
    verification = {"google60c46abce2c0ec23.html"}
    for path in sorted(ROOT.rglob("*.html")):
        if path.relative_to(ROOT).as_posix() in verification:
            continue
        text = changes.get(path, path.read_text(encoding="utf-8"))

        def replace(match: re.Match[str]) -> str:
            value = match.group("value")
            normalized = normalize_project_reference(path, value)
            return f'{match.group("attr")}={match.group("quote")}{normalized}{match.group("quote")}'

        changes[path] = attribute_pattern.sub(replace, text)


def collect_changes() -> dict[Path, str]:
    changes: dict[Path, str] = {}
    repair_home(changes)
    repair_basic_pages(changes)
    repair_404_and_template(changes)
    repair_blog(changes)
    for filename, data in TOOL_DATA.items():
        path = ROOT / filename
        changes[path] = repair_tool_page(path, data)
    repair_sitemaps_and_robots(changes)
    normalize_html_project_paths(changes)
    return {path: content for path, content in changes.items() if path.read_text(encoding="utf-8") != content}


def main() -> int:
    parser = argparse.ArgumentParser(description="Apply the verified SEO repair set.")
    parser.add_argument("--apply", action="store_true", help="Write changes. Without this flag, only show the planned files.")
    args = parser.parse_args()
    changes = collect_changes()
    action = "WRITE" if args.apply else "WOULD WRITE"
    for path in sorted(changes):
        print(f"{action} {path.relative_to(ROOT)}")
    print(f"{len(changes)} files")
    if args.apply:
        for path, content in changes.items():
            path.write_text(content, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
