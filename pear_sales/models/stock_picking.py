from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    customer_name = fields.Char("Customer Name")
    customer_phone = fields.Char("Customer Phone")
