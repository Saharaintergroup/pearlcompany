# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError


class SaleOrderWizard(models.TransientModel):
    _name = "sale.order.wizard"

    sale_order_id = fields.Many2one('sale.order', string='Sales Order')
    currency_id = fields.Many2one(related='sale_order_id.currency_id', string='Currency', )
    total_amount = fields.Monetary(string='Total Amount', currency_field='currency_id')
    amount = fields.Monetary(string='Amount', currency_field='currency_id')
    journal_id = fields.Many2one('account.journal',
                                 domain=[('type', 'in', ('bank', 'cash'))],
                                 string='Journal', )

    def create_register_payment(self):
        # if self.amount > self.total_amount:
        #     raise ValidationError(_(''))
        payment = self.env['account.payment'].create(
            {
                'payment_type': 'inbound',
                'state': 'draft',
                'partner_id': self.sale_order_id.partner_id.id,
                'sale_order_id': self.sale_order_id.id,
                'amount': self.amount,
                'journal_id': self.journal_id.id,
            }
        )
