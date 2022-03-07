from odoo import fields, models, api


class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_name = fields.Char("Customer Name")
    customer_phone = fields.Char("Customer Phone")
    is_customer_cash = fields.Boolean(default=False, string="Check")


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    product_packaging_qty = fields.Float("Product Package Qty")
    product_packaging_id = fields.Many2one('product.packaging', string="Packaging")
