# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
from frappe.utils import nowdate, now
from accounting_app.accounting_management_system.doctype.accounts.test_accounts import create_account, delete_account
from accounting_app.accounting_management_system.doctype.journal_entry.test_journal_entry import get_gl_entries, delete_gl_entries

class TestPaymentEntry(unittest.TestCase):
	def setUp(self):
		create_account("_Test Creditor", "Liability", "Liabilities")
		create_account("_Test Cash Account", "Asset", "Assets")


	def tearDown(self):
		delete_account("_Test Creditor")
		delete_account("_Test Cash Account")


	def test_payment_entry_creation(self):
		pe= make_payment_entry("Pay", True, True)
		gl_entries = get_gl_entries(pe.name, "Payment Entry")
		self.assertTrue(gl_entries)
		expected_values = {
			"_Test Cash Account": {
				"debit" : 0,
				"credit": 100
			},
			"_Test Creditor": {
				"debit": 100,
				"credit" : 0
			}
		}
		for field in ("debit", "credit"):
			for gle in gl_entries:
				self.assertEqual(expected_values[gle.account][field], gle[field])
		
		delete_gl_entries(gl_entries)
		self.assertFalse(get_gl_entries(pe.name, "Payment Entry"))
		pe.cancel()
		# To get cancelled GL entries
		gl_entries = get_gl_entries(pe.name, "Payment Entry")
		delete_gl_entries(gl_entries)
		pe.delete()
		print("hey!!!!!")


def make_payment_entry(payment_type, save= True, submit=False):
	pe = frappe.new_doc("Payment Entry")
	pe.posting_date = nowdate()
	pe.posting_time = now()
	pe.payment_type = payment_type
	pe.party = "Trinity"
	pe.account_paid_from = "_Test Cash Account"
	pe.account_paid_to = "_Test Creditor"
	pe.amount= 100
	if save or submit:
		pe.insert()
		if submit:
			pe.submit()
			
	return pe

	
