import math

from odoo import fields, models, api


class ReturnPickingLine(models.TransientModel):
    _inherit = "stock.return.picking.line"

    product_packaging_id = fields.Many2one('product.packaging', string='Packaging', default=False, domain="[('sales', '=', True), ('product_id','=',product_id)]", check_company=True)

    product_packaging_qty = fields.Float('Packaging Quantity')
    product_uom = fields.Many2one('uom.uom', string='Unit of Measure')


    @api.onchange('product_packaging_id', 'uom_id', 'quantity')
    def _onchange_update_product_packaging_qty(self):

        if not self.product_packaging_id:
            self.product_packaging_qty = False
        else:
            packaging_uom = self.product_packaging_id.product_uom_id
            packaging_uom_qty = self.product_uom._compute_quantity(self.uom_id, packaging_uom)
            # self.product_packaging_qty = float_round(packaging_uom_qty / self.product_packaging_id.qty, precision_rounding=packaging_uom.rounding,rounding_method="UP")
            self.product_packaging_qty = math.ceil(packaging_uom_qty / self.product_packaging_id.qty)
