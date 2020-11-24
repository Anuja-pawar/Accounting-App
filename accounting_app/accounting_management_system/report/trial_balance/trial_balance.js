// Copyright (c) 2016, Frappe and contributors
// For license information, please see license.txt
/* eslint-disable */
frappe.require("/assets/accounting_app/js/financial_statements.js", function(){
	frappe.query_reports["Trial Balance"] = {
		"filters": [
			{
				"fieldname": "fiscal_year",
				"label": __("Fiscal Year"),
				"fieldtype": "Link",
				"options": "Fiscal Year",
				"reqd": 1
			}
		],
		"formatter": accounting.financial_statements.formatter
	};
})