// Copyright (c) 2020, Frappe and contributors
// For license information, please see license.txt

{% include 'accounting_app/public/js/custom_button.js' %}

frappe.ui.form.on('Journal Entry', {
	refresh: function (frm) {
		custom_button(frm);
	},
	onload: function (frm) {
		console.log("in setup queries!");
		frm.set_query("account", "account_entries", function () {
			return {
				filters: {
					is_group: 0
				}
			}
		});	
	}
});

frappe.ui.form.on('Journal Entry Account', {
	account : function(frm,index,row){
	let child  = locals[index][row];
	if (frm.doc.difference > 0){
		child.credit = flt(frm.doc.difference);
		child.debit = 0.0 ;
	}
	else if (frm.doc.difference < 0) {
		child.debit = flt(frm.doc.difference) * -1;
		child.credit = flt(0.0) ;
	}
	total(frm);
	},
	debit: function (frm) {
		total(frm);
	},
	credit: function (frm) {
		total(frm);
	},
	transaction_remove: function (frm) {
		total(frm);
	},

});

function total(frm) {
	var total_debit = 0; 
	var total_credit = 0;
	var difference = 0;
	frm.doc.account_entries.forEach(function (d) {
		total_debit += flt(d.debit);
		total_credit += flt(d.credit);
	});
	frm.set_value("total_debit", total_debit);
	frm.set_value("total_credit", total_credit);
	
	difference = flt(frm.doc.total_debit) - flt(frm.doc.total_credit);
	frm.set_value("difference", difference);
	frm.refresh_fields();
}
