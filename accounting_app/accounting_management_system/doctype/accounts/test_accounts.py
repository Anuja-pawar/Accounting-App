# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and Contributors
# See license.txt
from __future__ import unicode_literals
import frappe
import unittest

class TestAccounts(unittest.TestCase):
	def test_account_creation(self):
		if not frappe.db.exists("Accounts", "_Test Asset Account"):
			self.create_account("_Test Asset Account","Asset", "Assets")		
		account_name = frappe.db.get_value("Accounts", "_Test Asset Account", "account_name")
		self.assertEqual(account_name, "_Test Asset Account")
		self.delete_account("_Test Asset Account")

def create_account(account_name, account_type, parent_accounts):
	if not frappe.db.exists("Accounts", account_name):
		acc = frappe.new_doc("Accounts")
		acc.parent_accounts = parent_accounts
		acc.account_name = account_name
		acc.account_type = account_type
		acc.insert()
	
def delete_account(name):
	frappe.delete_doc("Accounts", name)
