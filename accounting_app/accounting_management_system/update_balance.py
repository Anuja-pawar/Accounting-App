from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import flt

	
def balance_account(from_account,to_account,amount):
	acc = frappe.get_doc("Accounts",from_account)
	acc.account_balance -= amount
	acc.save()
	acc = frappe.get_doc("Accounts",to_account)
	acc.account_balance += amount
	acc.save()

def balance_account_je(account,credit ,debit):
	acc = frappe.get_doc("Accounts",account)
	acc.account_balance -= flt(credit)
	acc.account_balance += flt(debit)
	acc.save()