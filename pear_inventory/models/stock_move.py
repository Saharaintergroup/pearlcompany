from odoo import fields, models, api


class StockMoveLine(models.Model):
    _inherit = 'stock.move'

    product_packaging_qty = fields.Float("Product Packaging Qty")

class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id, values):
        res = super(StockRule, self)._get_stock_move_values(product_id,product_qty,product_uom,location_id,name,origin,company_id,values)
        res['product_packaging_qty'] = values.get('product_packaging_qty',False)
        return res


