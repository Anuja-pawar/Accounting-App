// Copyright (c) 2020, Frappe and contributors
// For license information, please see license.txt

frappe.ui.form.on('Item', 'item_code', function(frm, doctype, name){
    var row = locals[cdt][cdn];
		row.item_name = row.item_code;
		frm.refresh_fields();  
});
