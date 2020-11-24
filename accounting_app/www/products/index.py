from __future__ import unicode_literals

import frappe


def get_context(context):
    context.items = frappe.db.get_list("Item",{"show_on_website": ["=", True]},["*"],ignore_permissions=True )
    return context