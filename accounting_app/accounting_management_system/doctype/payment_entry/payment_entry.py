# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from accounting_app.accounting_management_system.update_balance import balance_account

class PaymentEntry(Document):
	def on_submit(self):
		balance_account(self.account_paid_from, self.account_paid_to, self.amount)
		self.make_gl_entry(self.account_paid_from,self.account_paid_to)

	def on_cancel(self):
		balance_account(self.account_paid_to, self.account_paid_from, self.amount)
		self.make_gl_entry(self.account_paid_to,self.account_paid_from)

	def make_gl_entry(self,pay_from,pay_to):
		gl_entry =[{
			"doctype":"General Ledger",
			'posting_date' : self.posting_date,
			'account': pay_from,
			'debit': 0.0,
			'credit': self.amount,
			'account_balance': frappe.db.get_value('Accounts',pay_from,'account_balance') ,
			'party_type': self.party_type,
			'party':self.party,
			'transaction_type': 'Payment Entry',
			'transaction_no':self.name,
		},
		{
			"doctype":"General Ledger",
			'posting_date' : self.posting_date,
			'account': pay_to,
			'debit': self.amount,
			'credit': 0.0,
			'account_balance': frappe.db.get_value('Accounts',pay_to,'account_balance') ,
			'party_type': self.party_type,
			'party':self.party,
			'transaction_type': 'Payment Entry',
			'transaction_no':self.name,
		}]
		for row in gl_entry:
			doc = frappe.get_doc(row)
			doc.insert()
