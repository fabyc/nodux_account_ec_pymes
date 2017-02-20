#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from trytond.pool import Pool
from .party import *
from .invoice import *
from .account import *
from .product import *

def register():
    Pool.register(
        Invoice,
        Party,
        BankAccountNumber,
        Company,
        Template,
        module='nodux_account_ec_pymes', type_='model')
    Pool.register(
        BalanceSheet,
        IncomeStatement,
        InvoiceReport,
        module='nodux_account_ec_pymes', type_='report')
    Pool.register(
        CreditInvoice,
        module='nodux_account_ec_pymes', type_='wizard')
