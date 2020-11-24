# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe, unittest
from frappe.utils import nowdate
from accounting_app.accounting_management_system.doctype.accounts.test_accounts import create_account, delete_account
from accounting_app.accounting_management_system.doctype.journal_entry.test_journal_entry import get_gl_entries, delete_gl_entries

class TestPurchaseInvoice(unittest.TestCase):
	def setUp(self):
		create_account("_Test Stock Assets", "Asset", "Assets")
		create_account("_Test Creditor", "Liability", "Liabilities")
	

	def tearDown(self):
		delete_account("_Test Stock Assets")
		delete_account("_Test Creditor")
	

	def test_for_negative_qty(self):
		pi= make_purchase_invoice(-1,False,False)
		self.assertRaises(frappe.exceptions.ValidationError, pi.insert)
		pi.items[0].update({
			"quantity":1
		})
		pi.insert()
		pi.submit()
		self.assertTrue(pi)
		pi.cancel()
		gl_entries= get_gl_entries(pi.name, "Purchase Invoice")
		delete_gl_entries(gl_entries)
		pi.delete()

	
	def test_for_reverse_gl_entries(self):
		pi = make_purchase_invoice(1, True, True)
		original_gl_entries = get_gl_entries(pi.name, "Purchase Invoice")
		delete_gl_entries(original_gl_entries)
		pi.cancel()
		amount = pi.total_amount
		gl_entries = get_gl_entries(pi.name, "Purchase Invoice")
		expected_values = {
			"_Test Stock Assets": {
				"debit": 0,
				"credit": amount
			},
			"_Test Creditor": {
				"debit": amount,
				"credit": 0
			}
		}
		for field in ("debit", "credit"):
			for gle in gl_entries:
				self.assertEqual(expected_values[gle.account][field], gle[field])
		delete_gl_entries(gl_entries)
		pi.delete() 

		
def make_purchase_invoice(qty, save, submit):
	pi = frappe.new_doc("Purchase Invoice")
	pi.supplier = "Trinity"
	pi.posting_date = nowdate()
	pi.due_date= nowdate()
	pi.credit_to = "_Test Creditor"
	pi.asset_account = "_Test Stock Assets"
	pi.set("items",[
		{
			"item": "chair", 
			"quantity": qty
		}
	])
	if save or submit:
		pi.insert()
		if submit:
			pi.submit()

	return pi


	

