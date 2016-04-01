#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from trytond.model import ModelView, fields
from trytond.pool import PoolMeta, Pool
from trytond.report import Report
from decimal import Decimal
__all__ = ['Invoice', 'InvoiceReport']
        
__metaclass__ = PoolMeta


class Invoice:
    'Invoice'
    __name__ = 'account.invoice'  
    #campos necesarios para guia de remision y comprobante de retencion
    fecha_modificacion = fields.Date(u'Fecha de Factura que se modifica')
    number_w = fields.Char('Number', size=20, readonly=True, select=True)
    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()
       
class InvoiceReport(Report):
    __name__ = 'account.invoice'
    
    @classmethod
    def parse(cls, report, records, data, localcontext):
        pool = Pool()
        User = pool.get('res.user')
        Invoice = pool.get('account.invoice')

        invoice = records[0]
        
        localcontext['descuento'] = cls._get_descuento(Invoice, invoice)
        localcontext['subtotal_12'] = cls._get_subtotal_12(Invoice, invoice)
        localcontext['subtotal_0'] = cls._get_subtotal_0(Invoice, invoice)

        return super(InvoiceReport, cls).parse(report, records, data,
                localcontext=localcontext)              
        
    @classmethod
    def _get_descuento(cls, Invoice, invoice):
        descuento = Decimal(0.00)
        descuento_parcial = Decimal(0.00)
                
        for line in invoice.lines:
            descuento_parcial = Decimal(line.product.template.list_price - line.unit_price)
            descuento = descuento + descuento_parcial
            
        return descuento
        
    @classmethod
    def _get_subtotal_12(cls, Invoice, invoice):
        subtotal0 = Decimal(0.00)
        subtotal12 = Decimal(0.00)
        pool = Pool()
        Taxes1 = pool.get('product.category-customer-account.tax')
        Taxes2 = pool.get('product.template-customer-account.tax')
        
        for line in invoice.lines:
            taxes1 = Taxes1.search([('category','=', line.product.category)])
            taxes2 = Taxes2.search([('product','=', line.product)])
            taxes3 = Taxes2.search([('product','=', line.product.template)])
        
            if taxes1:
                for t in taxes1:
                    if str('{:.0f}'.format(t.tax.rate*100)) == '12':
                        subtotal12= subtotal12 + (line.amount)
            elif taxes2:
                for t in taxes2:
                    if str('{:.0f}'.format(t.tax.rate*100)) == '12':
                        subtotal12= subtotal12 + (line.amount)
            elif taxes3:
                for t in taxes3:
                    if str('{:.0f}'.format(t.tax.rate*100)) == '12':
                        subtotal12= subtotal12 + (line.amount)
                        
            
        return subtotal12
                 
    @classmethod
    def _get_subtotal_0(cls, Invoice, invoice):
        subtotal0 = Decimal(0.00)
        subtotal12 = Decimal(0.00)
        pool = Pool()
        Taxes1 = pool.get('product.category-customer-account.tax')
        Taxes2 = pool.get('product.template-customer-account.tax')
                
        for line in invoice.lines:
            taxes1 = Taxes1.search([('category','=', line.product.category)])
            taxes2 = Taxes2.search([('product','=', line.product)])
            taxes3 = Taxes2.search([('product','=', line.product.template)])
            
            if taxes1:
                for t in taxes1:
                    if str('{:.0f}'.format(t.tax.rate*100)) == '0':
                        subtotal0= subtotal0 + (line.amount)
            elif taxes2:
                for t in taxes2:
                    if str('{:.0f}'.format(t.tax.rate*100)) == '0':
                        subtotal0= subtotal0 + (line.amount)
                        
            elif taxes3:
                for t in taxes3:
                    if str('{:.0f}'.format(t.tax.rate*100)) == '0':
                        subtotal0= subtotal0 + (line.amount)
                        
        return subtotal0
