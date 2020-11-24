# Copyright (c) 2013, Frappe and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import re
import functools
from frappe import _
from past.builtins import cmp
from frappe.utils import flt, getdate


def execute(filters=None):
    columns, data = [], []
    fiscal_year = get_fiscal_year(filters.fiscal_year)
    asset = get_data("Asset", fiscal_year)
    liability = get_data("Liability", fiscal_year)
    data = []
    data.extend(asset or [])
    if asset:
        data.extend([{
            "account": "Total Assets",
            "account_balance": asset[0].account_balance
        }])
    data.extend(liability or [])
    if liability:
        data.extend([{
            "account": "Total Liabilities",
            "account_balance": liability[0].account_balance
        }])
    columns = get_columns(filters.fiscal_year)
    return columns, data


def get_fiscal_year(fiscal_year):
    return frappe.db.get_list('Fiscal Year', filters={'name': fiscal_year}, fields = ['start_date', 'end_date'])


def get_data(account_type, fiscal_year):
    accounts = get_accounts(account_type)
    if not accounts:
        return None    
    accounts, accounts_by_name = filter_accounts(accounts)
    total_balance = get_total_account_balance(accounts_by_name, accounts)
    result = prepare_data(accounts, fiscal_year)
    return result


def get_accounts(account_type):
    accounts = frappe.get_list("Accounts", filters={"account_type":account_type}, fields=["*"], order_by="lft")
    return accounts


def get_total_account_balance(accounts_by_name, accounts):
    for d in reversed(accounts):
        if d.get("parent_accounts"):
            accounts_by_name[d.parent_accounts]["account_balance"] = accounts_by_name[d.parent_accounts]["account_balance"] + d.account_balance


def filter_accounts(accounts, depth=10):
    accounts_by_name = {}
    parent_children_map = {}
    for account in accounts:
        accounts_by_name[account.account_name] = account
        parent_children_map.setdefault(account.parent_accounts or None, []).append(account)
    filtered_accounts = []
    def set_indent(parent, level):
        if level < depth:
            children = parent_children_map.get(parent) or []
            for child in children:
                child.indent = level
                filtered_accounts.append(child)
                set_indent(child.name, level + 1)

    set_indent(None, 0)
    return filtered_accounts, accounts_by_name


def prepare_data(accounts, fiscal_year):
    data = []
    start_date = fiscal_year[0].start_date.strftime("%Y-%m-%d")
    end_date = fiscal_year[0].end_date.strftime("%Y-%m-%d")
    for d in accounts:
        row = frappe._dict({
            "account": _(d.name),
            "parent_accounts": _(d.parent_accounts) if d.parent_accounts else '',
            "indent": flt(d.indent),
            "start_date": start_date,
            "end_date": end_date,
            "account_type": d.account_type,
            "is_group": d.is_group,
            "account_balance": d.get("account_balance", 0.0),
            "account_name": d.account_name
        })
        data.append(row)
    return data


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