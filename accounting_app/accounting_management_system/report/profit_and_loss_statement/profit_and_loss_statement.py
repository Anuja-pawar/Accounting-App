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
    data.extend(income or [])
    if income:
        data.extend([{
            "account": "Total Income",
            "account_balance": income[0].account_balance
        }])
    data.extend(expense or [])
    if expense:
        data.extend([{
            "account": "Total Expense",
            "account_balance": expense[0].account_balance
        }])
    profit_loss = income[0]['account_balance'] -  expense[0]['account_balance']
    data.append(["Profit/ Loss (Income - Expense)", profit_loss])
    columns = get_columns(filters.fiscal_year)
    report_summary = get_report_summary(profit_loss)
    return columns, data, None, None, report_summary

def get_report_summary(profit_loss):
    return [
		{
			"value": profit_loss,
			"indicator": "Green" if profit_loss > 0 else "Red",
			"label": "Net Profit/Loss",
			"datatype": "Currency",
			"currency": frappe.db.get_value("Currency", "INR", "symbol") 
		}
	]