# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe, unittest
from frappe.utils import nowdate
from accounting_app.accounting_management_system.doctype.accounts.test_accounts import create_account, delete_account
from accounting_app.accounting_management_system.doctype.journal_entry.test_journal_entry import get_gl_entries, delete_gl_entries

class TestSalesInvoice(unittest.TestCase):
	def setUp(self):
		create_account("_Test Stock Assets", "Asset", "Assets")
		create_account("_Test Debtor", "Liability", "Liabilities")


	def tearDown(self):
		delete_account("_Test Stock Assets")
		delete_account("_Test Debtor")


	def test_for_negative_qty(self):
		si= make_sales_invoice(-1,False,False)
		self.assertRaises(frappe.exceptions.ValidationError, si.insert)
		si.items[0].update({
			"quantity":1
		})
		si.insert()
		si.submit()
		self.assertTrue(si)
		si.cancel()
		gl_entries= get_gl_entries(si.name, "Sales Invoice")
		delete_gl_entries(gl_entries)
		si.delete()


	def test_for_reverse_gl_entries(self):
		si = make_sales_invoice(1, True, True)
		original_gl_entries = get_gl_entries(si.name, "Sales Invoice")
		delete_gl_entries(original_gl_entries)
		si.cancel()
		amount = si.total_amount
		gl_entries = get_gl_entries(si.name, "Sales Invoice")
		expected_values = {
			"_Test Debtor": {
				"debit": 0,
				"credit": amount
			},
			"_Test Stock Assets": {
				"debit": amount,
				"credit": 0
			}
		}
		for field in ("debit", "credit"):
			for gle in gl_entries:
				self.assertEqual(expected_values[gle.account][field], gle[field])
		delete_gl_entries(gl_entries)
		si.delete() 


def make_sales_invoice(qty, save, submit):
	si = frappe.new_doc("Sales Invoice")
	si.customer = "Neo"
	si.posting_date = nowdate()
	si.due_date= nowdate()
	si.debit_to = "_Test Debtor"
	si.asset_account = "_Test Stock Assets"
	si.set("items",[
		{
			"item": "chair",
			"quantity": qty
		}
	])
	if save or submit:
		si.insert()
		if submit:
			si.submit()

	return si


