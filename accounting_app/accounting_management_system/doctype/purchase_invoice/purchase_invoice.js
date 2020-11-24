// Copyright (c) 2020, Frappe and contributors
// For license information, please see license.txt

{% include 'accounting_app/public/js/custom_button.js' %}

frappe.ui.form.on('Purchase Invoice', {
	validate: function(frm) {
			if (frm.doc.due_date < get_today()) {
			msgprint('You can not select past date in Due Date');
			validated = false;
			}
	}		 
});

frappe.ui.form.on('Purchase Invoice', {
    refresh: function (frm) {
		custom_button(frm,frm.doc.total_amount);
        frm.set_query("credit_to", function () {
            return {
                filters: {
                    parent_accounts: 'Accounts Payable'
                }
            }
        });
        frm.set_query("asset_account", function () {
            return {
                filters: {
                    parent_accounts: 'Current Assets'
                }
            }
        });
    }
});

frappe.ui.form.on('Purchase Invoice Item', 'quantity', function(frm, cdt, cdn) {
		var child = locals[cdt][cdn];
		child.amount = child.rate * child.quantity;
		total(frm);
		frm.refresh_field("Items"); 
});

function total(frm) {
	var total_amount = 0;
	var total_qty = 0;
    frm.doc.items.forEach(function (d) {
		total_amount += flt(d.amount);
		total_qty += flt(d.quantity);
    });
	frm.set_value('total_amount', total_amount);
	frm.set_value('total_quantity', total_qty);
	frm.refresh_fields();
}

