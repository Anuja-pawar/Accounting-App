// Copyright (c) 2016, Frappe and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["General Ledger"] = {
	"filters": [{
				"fieldname":"from_date",
				"label": __("From Date"),
				"fieldtype": "Date",
				"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
				"reqd": 1,
				},
				{
				"fieldname":"to_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"default": frappe.datetime.get_today(),
				"reqd": 1,
				},
				{
				"fieldname":"account",
				"label": __("Account"),
				"fieldtype": "Link",
				"options": "Accounts",
				},
				{
				"fieldname":"transaction_type",
				"label": __("Transaction Type"),
				"fieldtype": "Select",
				"options": "\nPurchase Invoice\nSales Invoice\nPayment Entry\nJournal Entry"
				},
				{
				"fieldname":"transaction_no",
				"label": __("Transaction No"),
				"fieldtype": "Data"
				}				
	]
};
