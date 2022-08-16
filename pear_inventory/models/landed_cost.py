# from odoo import fields, models, api
#
#
# class StockLandedCost(models.Model):
#     _inherit = 'stock.landed.cost'
#
#     def button_cancel(self):
#         if any(cost.state == 'done' for cost in self):
#             pass
#         return self.write({'state': 'cancel'})
