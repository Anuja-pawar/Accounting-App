# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt
from accounting_app.accounting_management_system.update_balance import balance_account_je

class JournalEntry(Document):
	def validate(self):
		self.set_total_debit_credit()
		if self.difference != 0:
			frappe.throw(_("Total debit must be equal to total credit. The difference is {}".format(self.difference)))


	def set_total_debit_credit(self):
		self.total_debit, self.total_credit, self.difference= 0, 0, 0
		for i in self.get("account_entries"):
			if i.debit > 0 and i.credit > 0:
				frappe.throw(_("Cannot debit and credit from the same account at once"))
			self.total_debit += flt(i.debit)
			self.total_credit +=  flt(i.credit)

		self.difference = flt(self.total_debit) - flt(self.total_credit)
		if len(self.get("account_entries"))	<=1 :
			frappe.throw(_("Need minimum two entries"))


	def on_submit(self):
		for i in self.get("account_entries"):
			balance_account_je(i.account,i.credit,i.debit)
		self.make_gl_entry()	


	def on_cancel(self):
		for i in self.get("account_entries"):
			balance_account_je(i.account,i.debit,i.credit)		
		self.make_gl_entry(reverse=True)


	def make_gl_entry(self, reverse=False):
		gl_entry= []
		for i in self.get("account_entries"):
			gl_entry.append({
				"doctype":"General Ledger",
				'posting_date' : self.posting_date,
				'account': i.account,
				'debit': i.debit if not reverse else i.credit ,
				'credit': i.credit if not reverse else i.debit,
				'account_balance': frappe.db.get_value('Accounts',i.account,'account_balance'),
				'party': i.party,
				'transaction_type': 'Journal Entry',
				'transaction_no':self.name
			})
		for row in gl_entry:
			doc = frappe.get_doc(row)
			doc.insert()

