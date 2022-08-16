from odoo import fields, models, api


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    def unlink(self):
        return super().unlink()
