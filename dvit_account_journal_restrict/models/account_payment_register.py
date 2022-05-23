from odoo import fields, models, api


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    journal_id = fields.Many2one('account.journal', store=True, readonly=False,
                                 compute=False,
                                 domain="[('company_id', '=', company_id), ('type', 'in', ('bank', 'cash'))]")