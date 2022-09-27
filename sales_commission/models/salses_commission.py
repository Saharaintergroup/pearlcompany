from odoo import fields, models, api, _
from dateutil.relativedelta import relativedelta
from datetime import date, datetime


class SalesCommission(models.Model):
    _name = 'sales.commission'
    _description = 'Sales Commission'
    _rec_name = 'name'

    name = fields.Char("Commission")
    agent = fields.Many2one('res.partner', "Agent", required=1, domain="[('has_commission','=', True)]")
    date_from = fields.Date("Date From", default=lambda self: fields.Date.to_string(date.today().replace(day=1)),
                            required=True)
    date_to = fields.Date("Date To", default=lambda self: fields.Date.to_string(
        (datetime.now() + relativedelta(months=+1, day=1, days=-1)).date()))
    commission_ids = fields.One2many('commissions.lines', 'commission_id', "Commissions")
    state = fields.Selection([('draft', 'Draft'),
                              ('done', 'Done')], default='draft')
    total_commission = fields.Float("Total", compute='get_total_commission', store=True)

    @api.onchange('agent')
    def get_agent_name(self):
        if self.agent:
            self.name = "Commissions for " + str(self.agent.name) + " for Month " + str(self.date_from.month)

    def get_payment(self):
        self.ensure_one()
        context = {
            'default_amount': self.total_commission,
            'default_destination_account_id': self.agent.property_account_payable_id.id,
            'default_payment_type': 'outbound',
            'default_partner_type': 'supplier',
            'default_partner_id': self.agent.id,
        }
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'account.payment',
            'view_type': 'form',
            'view_mode': 'form',
            'views': [(False, 'form')],
            'target': 'current',
            'context': context
        }

    @api.depends('commission_ids.commission')
    def get_total_commission(self):
        t_com = 0.0
        for rec in self:
            for com in rec.commission_ids:
                t_com += com.commission
            rec.total_commission = t_com

    def compute_commission(self):
        result = [(5, 0, 0)]
        account_move = self.env['account.move'].search(
            [('invoice_user_id.partner_id', '=', self.agent.id), ('state', '=', 'posted'), ('total_commission', '>', 0.0),
             ('invoice_date', '>=', self.date_from), ('invoice_date', '<=', self.date_to)])

        for line in account_move:
            result.append((0, 0, {'name': line.id, 'commission': line.total_commission}))
        self.commission_ids = result
        self.state = 'done'

    def set_draft(self):
        self.state = 'draft'


class CommissionLines(models.Model):
    _name = 'commissions.lines'

    commission_id = fields.Many2one('sales.commission')

    name = fields.Many2one('account.move', "Invoice Number")
    commission = fields.Float("Commission")
