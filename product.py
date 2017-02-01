#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
#! -*- coding: utf8 -*-
from trytond.pool import *
from trytond.model import fields
from trytond.pyson import Eval
from trytond.pyson import Id
from trytond.report import Report
from trytond.transaction import Transaction
from trytond.modules.company import CompanyReport
from trytond.pool import Pool

__all__ = ['Template']
__metaclass__ = PoolMeta

class Template:
    __name__ = 'product.template'

    @staticmethod
    def default_default_uom():
        Uom = Pool().get('product.uom')
        uoms = Uom.search([('symbol', '=', 'u'), ('name', '=', 'Unidad')])
        if len(uoms) >= 1:
            for uom in uoms:
                return uom.id

    @staticmethod
    def default_cost_price_method():
        return 'average'

    @classmethod
    def __setup__(cls):
        super(Template, cls).__setup__()
        cls._sql_constraints += [
            ('name', 'UNIQUE(name)',
                'NAME Product already exists'),
        ]

    def get_full_name(self, name):
        return self.name
