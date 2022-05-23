from odoo import fields, models, api


class ResUsers(models.Model):
    _inherit = 'res.users'

    allowed_customer = fields.Many2one('res.partner', domain='[("cash_sale_customer", "=", True)]')
    readonly_customer = fields.Boolean("Readonly Customer")
