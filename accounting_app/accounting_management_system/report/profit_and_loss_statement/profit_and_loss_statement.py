# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from accounting_app.accounting_management_system.report.balance_sheet.balance_sheet import get_fiscal_year, get_columns, get_data

def execute(filters=None):
    columns = get_columns(filters.fiscal_year)
    fiscal_year = get_fiscal_year(filters.fiscal_year)
    data = []
    income = get_data("Income", fiscal_year)
    expense = get_data("Expense", fiscal_year)
    data = []
    if income:
        data.extend(income)
        data.extend([{
            "account": "Total Income",
            "account_balance": income[0].account_balance
        }])
    if expense:
        data.extend(expense)
        data.extend([{
            "account": "Total Expense",
            "account_balance": expense[0].account_balance
        }])
    net_profit_loss = income[0]['account_balance'] -  expense[0]['account_balance']
    data.append(["Profit/ Loss (Income - Expense)", net_profit_loss])
    columns = get_columns(filters.fiscal_year)
    chart = get_chart_data(filters, columns, income, expense, net_profit_loss)
    report_summary = get_report_summary(net_profit_loss, income[0].account_balance, expense[0].account_balance)
    return columns, data, None, chart, report_summary


def get_report_summary(net_profit_loss, total_income, total_expense):
    return [
		{
			"value": net_profit_loss,
			"indicator": "Green" if net_profit_loss > 0 else "Red",
			"label": "Net Profit/Loss",
			"datatype": "Currency",
			"currency": frappe.db.get_value("Currency", "INR", "symbol") 
		},
        {
			"value": total_income,
			"indicator": "Green" if total_income > 0 else "Red",
			"label": "Total Income",
			"datatype": "Currency",
			"currency": frappe.db.get_value("Currency", "INR", "symbol") 
		},
        {
			"value": total_expense,
			"indicator": "Green" if total_expense > 0 else "Red",
			"label": "Total Expense",
			"datatype": "Currency",
			"currency": frappe.db.get_value("Currency", "INR", "symbol") 
		}
	]


def get_chart_data(filters, columns, income, expense, net_profit_loss):
	labels = [d.get("label") for d in columns[1:]]

	income_data, expense_data, net_profit_loss_data = [], [], []

	for p in columns[1:]:
		if income:
			income_data.append(income[0].get(p.get("fieldname")))
		if expense:
			expense_data.append(expense[0].get(p.get("fieldname")))
	
	net_profit_loss_data.append(net_profit_loss)

	datasets = []
	if income_data:
		datasets.append({'name': _('Income'), 'values': income_data})
	if expense_data:
		datasets.append({'name': _('Expense'), 'values': expense_data})
	if net_profit_loss_data:
		datasets.append({'name':_('Net Profit/Loss'), 'values': net_profit_loss_data})
		
	chart = {
		"data": {
			'labels': labels,
			'datasets': datasets
		}
	}
	chart["type"] = "bar"
	return chart