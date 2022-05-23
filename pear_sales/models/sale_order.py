from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_name = fields.Char("Customer Name")
    customer_phone = fields.Char("Customer Phone")
    is_customer_cash = fields.Boolean(default=False, string="Check")
    partner_id = fields.Many2one(
        'res.partner', string='Customer', change_default=False, default=lambda a: a.env.user.allowed_customer)
    readonly_customer = fields.Boolean(compute='_check_customer_readonly', store=True)

    @api.onchange('partner_id')
    def check_customer_cash(self):
        if self.partner_id.cash_sale_customer:
            self.is_customer_cash = True
        else:
            self.is_customer_cash = False

    @api.depends('user_id.readonly_customer')
    def _check_customer_readonly(self):
        for rec in self:
            if rec.user_id.readonly_customer:
                rec.readonly_customer = True
            else:
                rec.readonly_customer = False

    def _prepare_invoice(self):
        """
        Prepare the dict of values to create the new invoice for a sales order. This method may be
        overridden to implement custom invoice generation (making sure to call super() to establish
        a clean extension chain).
        """
        res = super(SaleOrder, self)._prepare_invoice()
        res.update({'is_customer_cash': self.is_customer_cash, 'customer_name': self.customer_name,
                    'customer_phone': self.customer_phone})
        return res


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    # def _prepare_invoice_line(self, **optional_values):
    #     res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
    #     res.update({
    #         'product_packaging_qty': self.product_packaging_qty,
    #         'product_packaging_id': self.product_packaging_id.id,
    #     })

    def _prepare_invoice_line(self, **optional_values):
        """
        Prepare the dict of values to create the new invoice line for a sales order line.

        :param qty: float quantity to invoice
        :param optional_values: any parameter that should be added to the returned invoice line
        """
        self.ensure_one()
        res = {
            'display_type': self.display_type,
            'sequence': self.sequence,
            'name': self.name,
            'product_id': self.product_id.id,
            'product_uom_id': self.product_uom.id,
            'quantity': self.qty_to_invoice,
            'discount': self.discount,
            'price_unit': self.price_unit,
            'tax_ids': [(6, 0, self.tax_id.ids)],
            'analytic_account_id': self.order_id.analytic_account_id.id,
            'analytic_tag_ids': [(6, 0, self.analytic_tag_ids.ids)],
            'sale_line_ids': [(4, self.id)],
            'product_packaging_qty': self.product_packaging_qty,
            'product_packaging_id': self.product_packaging_id.id,
        }
        if optional_values:
            res.update(optional_values)
        if self.display_type:
            res['account_id'] = False
        return res
