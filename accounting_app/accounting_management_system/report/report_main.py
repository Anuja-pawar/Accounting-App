from __future__ import unicode_literals
import frappe
from frappe import _

def get_fiscal_year(fiscal_year):
    return frappe.db.sql(""" select start_date, end_date from `tabFiscal Year` where name=%s """, fiscal_year, as_dict=1)


def get_columns(fiscal_year):
    columns = [
    {
        "fieldname": "account",
        "label": _("Accounts"),
        "fieldtype": "Link",
        "options": "Accounts",
        "width": 300
    },
    {
        "fieldname": "account_balance",
        "label" : fiscal_year,
        "fieldtype": "Currency",
        "width": 200
    }]
    return columns


def get_data(account_type, fiscal_year):
    accounts = get_accounts(account_type)
    if not accounts:
        return None
    accounts, accounts_by_name, parent_children_map = filter_accounts(accounts)
    gl_entries_by_account = {}
    for root in frappe.db.sql("""select lft, rgt from tabAccounts
            where account_type=%s and ifnull(parent_accounts, '') = ''""", account_type, as_dict=1):

        set_gl_entries_by_account(fiscal_year[0].start_date, fiscal_year[0].end_date, root.lft, root.rgt, gl_entries_by_account, ignore_closing_entries=False)
    
    accumulate_values_into_parents(accounts, accounts_by_name)
    out = prepare_data(accounts, fiscal_year)

    return out


def get_accounts(account_type):
    return frappe.db.sql("""
        select *
        from `tabAccounts`
        where account_type=%s order by lft""", (account_type), as_dict=1)