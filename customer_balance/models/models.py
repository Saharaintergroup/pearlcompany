# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_balance = fields.Float('',compute='_compute_customer_balance',)

    @api.depends('partner_id')
    def _compute_customer_balance(self):
        for rec in self:
            total_due = 0.0
            customer_balance = 0.0
            if rec.partner_id and not rec.partner_id.cash_sale_customer:
                total_due = rec.partner_id.total_due
                customer_balance = abs(total_due)
            rec.customer_balance = customer_balance



