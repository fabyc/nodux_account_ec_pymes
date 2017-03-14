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
import pytz
from datetime import datetime,timedelta
import time

__all__ = ['BalanceSheet', 'IncomeStatement']

def fmt_acc(val):
    # Format account number function
    fmt = '%s' + '0' * (8 - len(str(val)))
    account_code_fmt = int(fmt % val)
    return account_code_fmt


class BalanceSheet(Report):
    __metaclass__ = PoolMeta
    __name__ = 'account.balance_sheet'

    @classmethod
    def get_context(cls, records, data):
        pool = Pool()
        User = pool.get('res.user')

        user = User(Transaction().user)

        if user.company.timezone:
            timezone = pytz.timezone(user.company.timezone)
            dt = datetime.now()
            hora = datetime.astimezone(dt.replace(tzinfo=pytz.utc), timezone)
        report_context = super(BalanceSheet, cls).get_context(records, data)

        report_context['fecha'] = hora.strftime('%d/%m/%Y')
        report_context['hora'] = hora.strftime('%H:%M:%S')
        report_context['company'] = user.company
        report_context['date'] = Transaction().context.get('date')
        return report_context


class IncomeStatement(Report):
    __metaclass__ = PoolMeta
    __name__ = 'account.income_statement'

    @classmethod
    def get_context(cls, records, data):
        pool = Pool()
        User = pool.get('res.user')
        user = User(Transaction().user)
        if user.company.timezone:
            timezone = pytz.timezone(user.company.timezone)
            dt = datetime.now()
            hora = datetime.astimezone(dt.replace(tzinfo=pytz.utc), timezone)

        report_context = super(IncomeStatement, cls).get_context(records, data)

        report_context['fecha'] = hora.strftime('%d/%m/%Y')
        report_context['hora'] = hora.strftime('%H:%M:%S')
        report_context['company'] = user.company
        report_context['date'] = Transaction().context.get('date')
        return report_context
