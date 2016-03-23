#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from decimal import Decimal
from datetime import date
import operator
from sql.aggregate import Sum
from itertools import izip, groupby
from collections import OrderedDict
from trytond.model import ModelView, ModelSQL, fields
from trytond.wizard import Wizard, StateView, StateAction, Button
from trytond.report import Report
from trytond.pyson import Eval, PYSONEncoder
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond.modules.company import CompanyReport

__all__ = ['BalanceSheet', 'IncomeStatement']
         
__metaclass__ = PoolMeta

def fmt_acc(val):
    # Format account number function
    fmt = '%s' + '0' * (8 - len(str(val)))
    account_code_fmt = int(fmt % val)
    return account_code_fmt


class BalanceSheet(Report):
    'Sheet Balance'
    __name__ = 'account.balance_sheet'

    @classmethod
    def parse(cls, report, objects, data, localcontext):
        localcontext['company'] = Transaction().context.get('company.rec_name')
        localcontext['date'] = Transaction().context.get('date')
        return super(BalanceSheet, cls).parse(report, objects, data, localcontext)


class IncomeStatement(Report):
    'Income Statement'
    __name__ = 'account.income_statement'

    @classmethod
    def parse(cls, report, objects, data, localcontext):
        localcontext['company'] = Transaction().context.get('company.rec_name')
        localcontext['date'] = Transaction().context.get('date')
        return super(IncomeStatement, cls).parse(report, objects, data, localcontext)

