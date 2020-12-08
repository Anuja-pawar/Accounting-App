# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, getdate, formatdate
from accounting_app.accounting_management_system.report.balance_sheet.balance_sheet import filter_accounts


def execute(filters=None):
	columns, data = [], []
	validate_filters(filters)
	data = get_data(filters)
	columns = get_columns()
	return columns, data


def validate_filters(filters):
	fiscal_year = frappe.db.get_value("Fiscal Year", filters.fiscal_year, ["start_date", "end_date"], as_dict=1)
	filters.from_date = getdate(fiscal_year.start_date)
	filters.to_date = getdate(fiscal_year.end_date)
	print(filters)
	

def get_data(filters):
	accounts = frappe.get_list("Accounts", fields=["account_name", "parent_accounts", "account_type", "lft", "rgt"], order_by= "lft")
	if not accounts:
		return None	
	accounts, accounts_by_name, parent_children_map = filter_accounts(accounts)
	print(accounts)
	data = []
	# data = opening_closing_dr_cr(accounts)
	return data


	# def opening_closing_dr_cr(accounts):
	# 	gle_opening = frappe.get_list("General Ledger", fields=["account", "sum(debit) as opening_debit", "sum(credit) as opening_credit"],
	# 			filters={"posting_date":["<=", filters.from_date]}, group_by='account' )
	# 	gle_dr_cr = frappe.get_list("General Ledger", fields=["account", "sum(debit) as debit", "sum(credit) as credit"],
	# 			filters={"posting_date":[">=", filters.from_date], "posting_date":["<=", filters.to_date]}}, group_by='account' )
	# 	opening = frappe._dict()
	# 	for d in gle_opening:
	# 		opening.setdefault(d.account, d)
	# 	debit_credit = frappe._dict()
	# 	for d in gle_dr_cr:
	# 		debit_credit.setdefault(d.account, d)
	# 	closing = frappe._dict()
	# 	for d in gle_dr_cr:
	# 		if d.debit > d.credit:
	# 			closing_debit = flt(d.debit - d.credit)
	# 			closing_credit = 0.0
	# 		else:
	# 			closing_credit = flt(d.credit - d.debit)
	# 			closing_debit = 0.0	
	# 	for d in accounts:
	# 		key = d.account
	# 		if opening.get(key):
	# 			opening.update(debit_credit.get(key))
	# 			opening.update(closing.get(key))
	# 	data = []
	# 	data.append(opening)
	# 	print(data)
	# 	return data
				

def get_columns():
	return [
		{
			"fieldname": "account",
			"label": _("Account"),
			"fieldtype": "Link",
			"options": "Accounts",
			"width": 200
		},
		{
			"fieldname": "opening_debit",
			"label": _("Opening (Dr)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		},
		{
			"fieldname": "opening_credit",
			"label": _("Opening (Cr)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		},
		{
			"fieldname": "debit",
			"label": _("Debit"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		},
		{
			"fieldname": "credit",
			"label": _("Credit"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		},
		{
			"fieldname": "closing_debit",
			"label": _("Closing (Dr)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		},
		{
			"fieldname": "closing_credit",
			"label": _("Closing (Cr)"),
			"fieldtype": "Currency",
			"options": "currency",
			"width": 120
		}
	]
