from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    agent = fields.Many2one('res.partner', "Agent")
    total_commission = fields.Float("Sales Commission", compute="_get_total_commission", store=True)

    @api.depends(
        'line_ids.price_subtotal',
        'state',
        'invoice_user_id',
        'invoice_user_id.partner_id',
        'invoice_user_id.partner_id.commission_percentage',
        'amount_residual')
    def _get_total_commission(self):
        commission = 0.0
        for rec in self:
            if rec.move_type in ('out_invoice', 'out_refund', 'out_receipt'):
                # if rec.state == 'posted' and rec.amount_residual > 0.0 and rec.agent.commission_depends == 'invoiced':
                #     for move in rec.invoice_line_ids:
                #         if move.product_id.has_commission == True :
                #             commission += (move.price_subtotal * rec.agent.commission_percentage / 100)

                if rec.state == 'posted' and rec.amount_residual == 0.0:
                    for move in rec.invoice_line_ids:
                        commission += (move.price_subtotal * rec.invoice_user_id.partner_id.commission_percentage / 100)
                else:
                    commission = 0.0
            rec.total_commission = commission
