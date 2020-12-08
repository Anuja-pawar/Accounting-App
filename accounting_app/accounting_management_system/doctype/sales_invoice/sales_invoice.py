# -*- coding: utf-8 -*-
# Copyright (c) 2020, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _, throw
from frappe.model.document import Document
from accounting_app.accounting_management_system.update_balance import balance_account

class SalesInvoice(Document):
	def validate(self):
		self.set_item_rate_and_amount()
		self.set_total_quantity_and_amount()
		self.validate_quantity_and_rate()


	def set_item_rate_and_amount(self):
		for i in self.get("items"):
			i.rate = frappe.db.get_value("Item", i.item, "price")
			i.amount = i.rate * i.quantity
	

	def set_total_quantity_and_amount(self):
		self.total_amount = 0
		self.total_quantity = 0
		for i in self.get("items"):
			self.total_amount += i.amount
			self.total_quantity += i.quantity


	def validate_quantity_and_rate(self):
		for i in self.get("items"):
			if i.quantity <= 0:
				frappe.throw(_("Quantity cannot be zero or negative. Please enter a valid quantity"))
			if i.rate <= 0 :
				frappe.throw(_("Rate cannot be zero or negative. Please enter a valid rate "))
	
	
	def on_submit(self):
		balance_account(self.asset_account, self.debit_to, self.total_amount)
		self.make_gl_entry(self.asset_account, self.debit_to)


	def on_cancel(self):
		balance_account(self.debit_to, self.asset_account, self.total_amount)
		self.make_gl_entry(self.debit_to, self.asset_account)


	def make_gl_entry(self, from_account, to_account): 
		gl_entry =[{
			"doctype":"General Ledger",
			'posting_date' : self.posting_date,
			'account': to_account,
			'debit': self.total_amount,
			'credit': 0.0,
			'account_balance': frappe.db.get_value('Accounts',to_account,'account_balance') ,
			'party_type': 'Customer',
			'party':self.customer_name,
			'transaction_type': 'Sales Invoice',
			'transaction_no':self.name,
		},
		{
			"doctype":"General Ledger",
			'posting_date' : self.posting_date,
			'account': from_account,
			'debit': 0.0,
			'credit': self.total_amount,
			'account_balance':frappe.db.get_value('Accounts',from_account,'account_balance'),
			'party_type': 'Customer',
			'party':self.customer_name,
			'transaction_type': 'Sales Invoice',
			'transaction_no':self.name,
		}]
		for row in gl_entry:
			doc = frappe.get_doc(row)
			doc.insert()
