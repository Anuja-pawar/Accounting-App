# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals

import frappe
import unittest
from frappe.utils import nowdate
from accounting_app.accounting_management_system.doctype.accounts.test_accounts import create_account, delete_account

class TestJournalEntry(unittest.TestCase):
	def setUp(self):
		create_account("_Test Debtor", "Asset", "Assets")
		create_account("_Test Creditor", "Liability", "Liabilities")
	

	def tearDown(self):
		delete_account("_Test Debtor")
		delete_account("_Test Creditor")


	def test_journal_entry_creation(self):
		je = make_journal_entry(100, True, True)
		gl_entries = get_gl_entries(je.name, "Journal Entry")
		self.assertTrue(gl_entries)
		expected_values = {
			"_Test Debtor": {
				"debit": 100,
				"credit": 0
			},
			"_Test Creditor": {
				"debit": 0,
				"credit": 100
			}
		}
		for field in ("debit", "credit"):
		    for gle in gl_entries:
		        self.assertEqual(expected_values[gle.account][field], gle[field])
		
		je.cancel()
		# To get cancelled GL entries
		gl_entries = get_gl_entries(je.name, "Journal Entry")
		delete_gl_entries(gl_entries)
		je.delete()

	def test_for_reverse_gl_entries(self):
		je = make_journal_entry(500, True, True)
		original_gl_entries = get_gl_entries(je.name, "Journal Entry")
		delete_gl_entries(original_gl_entries)
		je.cancel()
		gl_entries = get_gl_entries(je.name, "Journal Entry")
		expected_values = {
			"_Test Debtor": {
				"debit": 0,
				"credit": 500
			},
			"_Test Creditor": {
				"debit": 500,
				"credit": 0
			}
		}
		for field in ("debit", "credit"):
		    for gle in gl_entries:
		        self.assertEqual(expected_values[gle.account][field], gle[field])
		delete_gl_entries(gl_entries)
		je.delete()        


def make_journal_entry(amount, save, submit):
	je = frappe.new_doc("Journal Entry")
	je.party = ""
	je.posting_date = nowdate()
	je.set("account_entries",[
		{
			"account": "_Test Debtor",
			"debit": amount if amount > 0 else 0,
			"credit": abs(amount) if amount < 0 else 0
		},
		{
			"account": "_Test Creditor",
			"debit": abs(amount) if amount < 0 else 0,
			"credit": amount if amount > 0 else 0
		}
	])
	if save or submit:
		je.insert()
		if submit:
			je.submit()
			
	return je


def get_account(name):
	return frappe.get_doc("Accounts", name)


def get_gl_entries(transaction_no, transaction_type):
	return frappe.db.get_all("General Ledger", fields=["*"], filters= {"transaction_no":transaction_no, "transaction_type":transaction_type})


def delete_gl_entries(gl_entries):
	for gl in gl_entries:
		gle = frappe.get_doc("General Ledger", gl.name)
		gle.delete()