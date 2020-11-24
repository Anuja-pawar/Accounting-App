    
function custom_button(frm, amount) {
    if (frm.doc.docstatus == 1)
    {
        frm.add_custom_button(__("General Ledger"), function(){
            frappe.route_options = {
                "transaction_no": frm.doc.name,
                "from_date": frm.doc.posting_date,
                "to_date": frm.doc.posting_date
            };
            frappe.set_route("query-report", "General Ledger");
        });
        if(frm.doc.doctype == 'Purchase Invoice' || frm.doc.doctype == 'Sales Invoice')
        {
            frm.add_custom_button(__('Payment Entry'), function(){
                frappe.model.with_doctype("Payment Entry", function(){
                    let doc = frappe.model.get_new_doc("Payment Entry");
                    if (frm.doc.doctype == 'Purchase Invoice')
                    {
                        doc.payment_type = 'Pay';
                        doc.account_paid_from = 'Cash';
                        doc.account_paid_to = 'Creditors';
                        doc.party_type = 'Supplier';
                        doc.party  = frm.doc.supplier_name;
                        doc.amount = amount.toString();
                        doc.transaction_type = frm.doc.doctype;
                        doc.transaction_no = frm.doc.name;
                    }
                    else
                    {
                        doc.type = 'Receive';
                        doc.account_paid_from = 'Debtors';
                        doc.account_paid_to = 'Cash';
                        doc.party_type = 'Customer';
                        doc.party  = frm.doc.customer_name;
                        doc.amount = amount.toString();
                        doc.transaction_tpe = frm.doc.doctype;
                        doc.transaction_no = frm.doc.name;
                    }
                    frappe.set_route("Form", doc.doctype, doc.name);
                });
            });
        }
    }
}
    