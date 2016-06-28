#This file is part of Tryton.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.

from trytond.model import ModelView, fields
from trytond.pool import PoolMeta, Pool
from trytond.report import Report
from decimal import Decimal
from trytond.wizard import Wizard, StateView, StateTransition, StateAction, \
    Button
from trytond.transaction import Transaction

conversor = None
try:
    from numword import numword_es
    conversor = numword_es.NumWordES()
except:
    print("Warning: Does not possible import numword module!")
    print("Please install it...!")

__all__ = ['Invoice', 'InvoiceReport', 'CreditInvoice']


class Invoice:
    __metaclass__ = PoolMeta
    __name__ = 'account.invoice'
    #campos necesarios para guia de remision y comprobante de retencion
    fecha_modificacion = fields.Date(u'Fecha de Factura que se modifica')
    number_w = fields.Char('Number', size=20, readonly=True, select=True)
    @classmethod
    def __setup__(cls):
        super(Invoice, cls).__setup__()

    def get_amount2words(self, value):
        if conversor:
            return (conversor.cardinal(int(value))).upper()
        else:
            return ''

class InvoiceReport(Report):
    __metaclass__ = PoolMeta
    __name__ = 'account.invoice'
    @classmethod
    def parse(cls, report, records, data, localcontext):
        pool = Pool()
        User = pool.get('res.user')
        Invoice = pool.get('account.invoice')
        Sale = pool.get('sale.sale')
        invoice = records[0]
        sale = Sale.search([('reference','=', invoice.description)])
        print "La venta ", sale
        TermLines = pool.get('account.invoice.payment_term.line')
        cont = 0
        if invoice.total_amount:
            d = str(invoice.total_amount)
            decimales = d[-2:]
        """
        if sale:
            for s in sale:
                if s.tipo_p:
                    tipo = (s.tipo_p).upper()
                else:
                    tipo = None
        else:
            tipo = None
        """
        tipo = None
        if invoice.payment_term:
            term = invoice.payment_term
            termlines = TermLines.search([('payment', '=', term.id)])
            for t in termlines:
                t_f = t
                cont += 1

        if cont == 1 and t_f.days == 0:
            forma = 'CONTADO'
        else:
            forma = 'CREDITO'

        localcontext['descuento'] = cls._get_descuento(Invoice, invoice)
        localcontext['subtotal_12'] = cls._get_subtotal_12(Invoice, invoice)
        localcontext['subtotal_14'] = cls._get_subtotal_14(Invoice, invoice)
        localcontext['subtotal_0'] = cls._get_subtotal_0(Invoice, invoice)
        localcontext['forma'] = forma
        localcontext['tipo'] = tipo
        localcontext['amount2words']=cls._get_amount_to_pay_words(Invoice, invoice)
        localcontext['decimales'] = decimales
        localcontext['lineas'] = cls._get_lineas(Invoice, invoice)
        return super(InvoiceReport, cls).parse(report, records, data,
                localcontext=localcontext)

    @classmethod
    def _get_amount_to_pay_words(cls, Invoice, invoice):
        amount_to_pay_words = Decimal(0.0)
        if invoice.total_amount and conversor:
            amount_to_pay_words = invoice.get_amount2words(invoice.total_amount)
        return amount_to_pay_words

    @classmethod
    def _get_lineas(cls, Invoice, invoice):
        cont = 0

        for line in invoice.lines:
            cont += 1
        return cont

    @classmethod
    def _get_descuento(cls, Invoice, invoice):
        descuento = Decimal(0.00)
        descuento_parcial = Decimal(0.00)

        for line in invoice.lines:
            descuento_parcial = Decimal(line.product.template.list_price - line.unit_price)
            descuento = descuento + descuento_parcial

        return descuento

    @classmethod
    def _get_subtotal_14(cls, Invoice, invoice):
        subtotal0 = Decimal(0.00)
        subtotal14 = Decimal(0.00)
        pool = Pool()
        Taxes1 = pool.get('product.category-customer-account.tax')
        Taxes2 = pool.get('product.template-customer-account.tax')

        for line in invoice.lines:
            taxes1 = Taxes1.search([('category','=', line.product.category)])
            taxes2 = Taxes2.search([('product','=', line.product)])
            taxes3 = Taxes2.search([('product','=', line.product.template)])

            if taxes1:
                for t in taxes1:
                    if str('{:.0f}'.format(t.tax.rate*100)) == '14':
                        subtotal14= subtotal14 + (line.amount)
            elif taxes2:
                for t in taxes2:
                    if str('{:.0f}'.format(t.tax.rate*100)) == '14':
                        subtotal14= subtotal14 + (line.amount)
            elif taxes3:
                for t in taxes3:
                    if str('{:.0f}'.format(t.tax.rate*100)) == '14':
                        subtotal14= subtotal14 + (line.amount)


        return subtotal14

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


class CreditInvoice(Wizard):
    __metaclass__ = PoolMeta
    __name__ = 'account.invoice.credit'

    @classmethod
    def __setup__(cls):
        super(CreditInvoice, cls).__setup__()

    def default_start(self, fields):
        Invoice = Pool().get('account.invoice')
        default = {
            'with_refund': True,
            }
        origin = Invoice.browse(Transaction().context['active_ids'])
        def in_group():
            pool = Pool()
            ModelData = pool.get('ir.model.data')
            User = pool.get('res.user')
            Group = pool.get('res.group')
            group = Group(ModelData.get_id('nodux_account_ec_pymes',
                        'group_sale_return'))
            transaction = Transaction()
            user_id = transaction.user
            if user_id == 0:
                user_id = transaction.context.get('user', user_id)
            if user_id == 0:
                return True
            user = User(user_id)
            return origin and group in user.groups
        if not in_group():
            self.raise_user_error("No esta autorizado a generar Nota de credito")

        for invoice in Invoice.browse(Transaction().context['active_ids']):
            if (invoice.state != 'posted'
                    or invoice.payment_lines
                    or invoice.type in ('in_invoice', 'in_credit_note')):
                default['with_refund'] = False
                break
        return default
