# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, _dict

def execute(filters=None):
	if not filters:
		return [], []
	account_details = {}
	for acc in frappe.get_all("Accounts", fields=["name", "is_group"]):
		account_details.setdefault(acc.name, acc)
	validate_filters(filters,account_details)
	columns = get_columns(filters)
	data = get_results(filters,account_details)
	return columns, data


def validate_filters(filters,account_details):
	if filters.from_date > filters.to_date :
		frappe.throw(_("From date must be before To date"))
	if filters.get("transaction_no") and not account_details.get(filters.transaction_no):
		frappe.throw(_("Transaction no. does not exist").format(filters.account))


def get_results(filters, account_details):
	gl_entries = get_gl_entries(filters)
	data = get_data(filters, account_details, gl_entries)
	result = get_balance(data)
	return result


def get_gl_entries(filters):
	filters = get_conditions(filters)
	gl_entries = frappe.get_list("General Ledger", fields=["*"], filters=filters, order_by ="posting_date, creation")
	return gl_entries


def get_conditions(filters):
	conditions = {}
	if filters.get("account"):
		conditions.update({"account":filters.account})
	if not (filters.get("account")):
		conditions.update({"posting_date": ["<", filters.to_date]})
		conditions.update({"posting_date": [">", filters.from_date]})
	if filters.get("transaction_type"):
		conditions.update({"transaction_type":filters.transaction_type})		
	if filters.get("transaction_no"):
		conditions.update({"transaction_no":filters.transaction_no})

	return conditions if conditions else ""


def get_balance(data):
	for d in data:
		if not d.get('posting_date'):
			balance = 0
		balance += d.get('debit') -  d.get('credit')
		d['balance'] = balance

	return data


def get_data(filters, account_details, gl_entries):
	data = []
	ledger = get_formatted_ledger(filters, gl_entries)
	data.append(ledger.opening)
	data += gl_entries
	data.append(ledger.total)
	data.append(ledger.closing)
	return data


def get_opening_closing_dict():
	def _get_debit_credit_dict(label):
		return _dict(
			account=label,
			debit=0.0,
			credit=0.0
		)

	return _dict(
		opening = _get_debit_credit_dict('Opening'),
		total = _get_debit_credit_dict('Total'),
		closing = _get_debit_credit_dict('Closing (Opening + Total)')
	)


def get_formatted_ledger(filters, gl_entries):
	totals = get_opening_closing_dict()
	total_debit, total_credit = 0, 0
	entries=[]
	for gle in gl_entries:
		total_debit += gle.debit
		total_credit += gle.credit
	totals['total']['debit']= total_debit
	totals['total']['credit']= total_credit
	totals['closing']['debit']= totals['total']['debit'] + totals['opening']['debit']
	totals['closing']['credit']= totals['total']['credit'] + totals['opening']['credit']
	return totals


def get_columns(filters):
	columns = [{
		"fieldname": "posting_date",
		"label": _("Posting Date"),
		"fieldtype": "Date",
		"width": 120
		},
		{
		"fieldname": "account",
		"label": _("Account"),
		"fieldtype": "Link",
		"options":"Accounts",
		"width": 200
		},
		{
		"fieldname": "debit",
		"label": _("Debit (INR)"),
		"fieldtype": "Currency",
		"width": 150
		},
		{
		"fieldname": "credit",
		"label": _("Credit (INR)"),
		"fieldtype": "Currency",
		"width": 150
		},
		{
		"fieldname": "balance",
		"label": _("Balance (INR)"),
		"fieldtype": "Currency",
		"width": 150
		},
		{
		"fieldname": "transaction_type",
		"label": _("Transaction Type"),
		"fieldtype": "Data",
		"width": 150
		},
		{
		"fieldname": "transaction_no",
		"label": _("Transaction No"),
		"fieldtype": "Dynamic Link",
		"options":"transaction_type",
		"width": 180
		},
		{
		"fieldname": "party_type",
		"label": _("Party Type"),
		"fieldtype": "Data",
		"width": 100
		},
		{
		"fieldname": "party",
		"label": _("Party"),
		"fieldtype": "Data",
		"width": 150
		},
	]
	return columns
