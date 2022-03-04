import math
from datetime import timedelta

from odoo import fields, models, api,_
from odoo.tools import float_compare, float_round


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.onchange('product_id', 'product_uom_qty', 'product_uom')
    def _onchange_suggest_packaging(self):
        # remove packaging if not match the product
        if self.product_packaging_id.product_id != self.product_id:
            self.product_packaging_id = False
        # suggest biggest suitable packaging
        if self.product_id and self.product_uom_qty and self.product_uom:
            self.product_packaging_id = self.product_id.packaging_ids.filtered('sales')

    @api.onchange('product_packaging_id')
    def _onchange_product_packaging_id(self):
        if self.product_packaging_id and self.product_uom_qty:
            newqty = self.product_packaging_id._check_qty(self.product_uom_qty, self.product_uom, "UP")
            pass
            # if float_compare(newqty, self.product_uom_qty, precision_rounding=self.product_uom.rounding) != 0:
            #     return {
            #         'warning': {
            #             'title': _('Warning'),
            #             'message': _(
            #                 "This product is packaged by %(pack_size).2f %(pack_name)s. You should sell %(quantity).2f %(unit)s.",
            #                 pack_size=self.product_packaging_id.qty,
            #                 pack_name=self.product_id.uom_id.name,
            #                 quantity=newqty,
            #                 unit=self.product_uom.name
            #             ),
            #         },
            #     }

    @api.onchange('product_packaging_id', 'product_uom', 'product_uom_qty')
    def _onchange_update_product_packaging_qty(self):

        if not self.product_packaging_id:
            self.product_packaging_qty = False
        else:
            packaging_uom = self.product_packaging_id.product_uom_id
            packaging_uom_qty = self.product_uom._compute_quantity(self.product_uom_qty, packaging_uom)
            # self.product_packaging_qty = float_round(packaging_uom_qty / self.product_packaging_id.qty, precision_rounding=packaging_uom.rounding,rounding_method="UP")
            self.product_packaging_qty = math.ceil(packaging_uom_qty / self.product_packaging_id.qty)


    def _prepare_procurement_values(self, group_id=False):
        """ Prepare specific key for moves or other components that will be created from a stock rule
        comming from a sale order line. This method could be override in order to add other custom key that could
        be used in move/po creation.
        """
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        values.update({'product_packaging_qty': self.product_packaging_qty})
        return values