from __future__ import unicode_literals
import frappe
from frappe import throw, _
from frappe.utils import nowdate, flt


@frappe.whitelist(allow_guest=True)	
def add_to_cart(item_name, user, qty=1, save=True, submit=False):
	user = set_party(user)
	si = get_cart_details(user)
	if not si:
		return make_sales_invoice(item_name, qty, user, save, submit)
	else:
		return update_sales_invoice(si.name, item_name, qty, save, submit )


def set_party(user):
	if user:
		user_email = frappe.session.user
		customer = frappe.get_list("Customer", filters={"email":user_email}, fields=["*"])
		if not customer:
			customer = frappe.new_doc("Customer")
			customer.customer_name = user
			customer.email = user_email
			customer.insert()
		elif customer:
			user = customer[0].customer_name
	return user


def get_cart_details(user, get_full_details=False):
	si = frappe.db.get_list("Sales Invoice", { "Customer": user, "docstatus":0})
	if not si:
		return None
	else:
		return frappe.get_doc("Sales Invoice", si[0].name)


@frappe.whitelist(allow_guest=True)
def make_sales_invoice(item_name, qty, user, save=True, submit=False):
	si = frappe.new_doc("Sales Invoice")
	si.customer = user
	si.posting_date = nowdate()
	si.payment_due_date = nowdate()
	si.debit_to = "Debtors"
	si.asset_account = "Creditors"
	si.set("items",[
		{
			"item": item_name,
			"quantity": qty
		}
	])
	if save or submit:
		si.insert()
		if submit:
			si.submit()	
	return si


@frappe.whitelist(allow_guest=True)
def update_sales_invoice(si, item_name, qty, save=True, submit=False):
	si = frappe.get_doc("Sales Invoice", si)
	items = si.items
	if item_name:
		item_exist = False
		for item in items:
			if item.item_name == item_name:
				item_exist = True
				item.update({
					"quantity": flt(qty)
					})
				break
		if not item_exist:
			print("New Item")
			si.append("items", {
				"item": item_name,
				"quantity": flt(qty)
			})
	if save or submit:
		print("doc saved")
		si.save()
		if submit:
			si.submit()	
	return si


@frappe.whitelist(allow_guest=True)
def display_cart(user):
	set_party(user)
	return get_cart_details(user)


@frappe.whitelist(allow_guest=True)
def remove_item(si, item_name):
	si = frappe.get_doc("Sales Invoice", si)
	items = si.items
	if item_name:
		for item in items:
			if item.item_name == item_name:
				si.remove(item)
				break
	if len(items)==0:
		si.delete()
		si = "Null"
	else:
		si.save()
		si = frappe.get_doc("Sales Invoice", si)
	return si


@frappe.whitelist(allow_guest=True)
def place_order(si, submit=False):
	invoice = frappe.get_doc("Sales Invoice", si)
	if invoice and invoice.docstatus == 0:
		if submit:
			invoice.submit()
	return invoice
