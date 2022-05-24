# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def create_payment(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'target': 'new',
            'name': _('Register Payment'),
            'view_mode': 'form',
            'view_id': self.env.ref('payment_sale_quotation.sale_order_wizard_form_views').id,
            'res_model': 'sale.order.wizard',
            'context': {
                'default_total_amount': self.amount_total,
                'default_sale_order_id': self.id,
            },
        }

    def view_sale_order_payments(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'target': 'current',
            'name': _('Payments'),
            'view_type': 'list',
            'view_mode': 'list',
            'views': [[False, 'list'], [False, 'form']],
            'res_model': 'account.payment',
            'domain': [('sale_order_id', '=', self.id)],
        }
