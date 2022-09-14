from odoo import fields, models, api


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    has_commission = fields.Boolean(
        default=False
    )
