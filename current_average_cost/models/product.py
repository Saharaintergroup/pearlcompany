# -*- encoding: utf-8 -*-
from itertools import chain

from odoo import models, fields,tools, api
from odoo.exceptions import UserError

from odoo.fields import Selection


class ProductProduct(models.Model):
    _inherit = "product.product"

    avarage_cost = fields.Float('Current Average Cost', compute="_get_avg_cost",
                                digits='Product Price', help='Current Stock Average Cost')

    def _get_avg_cost(self):
        for prod in self:
            prod.avarage_cost = prod.value_svl / prod.qty_available if prod.qty_available else 0.0


    def price_compute(self, price_type, uom=False, currency=False, company=None):
        # TDE FIXME: delegate to template or not ? fields are reencoded here ...
        # compatibility about context keys used a bit everywhere in the code
        if not uom and self._context.get('uom'):
            uom = self.env['uom.uom'].browse(self._context['uom'])
        if not currency and self._context.get('currency'):
            currency = self.env['res.currency'].browse(self._context['currency'])

        products = self
        if price_type == 'standard_price':
            # standard_price field can only be seen by users in base.group_user
            # Thus, in order to compute the sale price from the cost for users not in this group
            # We fetch the standard price as the superuser
            products = self.with_company(company or self.env.company).sudo()
        elif price_type == 'avarage_cost':
            # standard_price field can only be seen by users in base.group_user
            # Thus, in order to compute the sale price from the cost for users not in this group
            # We fetch the standard price as the superuser
            products = self.with_company(company or self.env.company).sudo()
        prices = dict.fromkeys(self.ids, 0.0)
        for product in products:
            prices[product.id] = product[price_type] or 0.0
            if price_type == 'list_price':
                prices[product.id] += product.price_extra
                # we need to add the price from the attributes that do not generate variants
                # (see field product.attribute create_variant)
                if self._context.get('no_variant_attributes_price_extra'):
                    # we have a list of price_extra that comes from the attribute values, we need to sum all that
                    prices[product.id] += sum(self._context.get('no_variant_attributes_price_extra'))

            if uom:
                prices[product.id] = product.uom_id._compute_price(prices[product.id], uom)

            # Convert from current user company currency to asked one
            # This is right cause a field cannot be in more than one currency
            if currency:
                prices[product.id] = product.currency_id._convert(
                    prices[product.id], currency, product.company_id, fields.Date.today())

        return prices


class ProductTemplate(models.Model):
    _inherit = "product.template"

    avarage_cost = fields.Float('Current Average Cost', compute="_get_avg_cost",
                                digits='Product Price')
    show_current_avarage_cost = fields.Boolean(compute='_compute_show_current_avarage_cost')

    def _compute_show_current_avarage_cost(self):
        module_id = self.env['ir.module.module'].search(
            [('name', '=', 'wh_enhancement_privileges'), ('state', '=', 'installed')], limit=1)
        show_field = True
        if module_id:
            show_field = self.env.user.has_group('wh_enhancement_privileges.group_allow_product_cost')
        for rec in self:
            rec.show_current_avarage_cost = show_field

    def _get_avg_cost(self):
        products = self.env['product.product'].search([('product_tmpl_id', 'in', self.ids)])
        dic = {}
        for prod in products:
            if prod.product_tmpl_id.id not in dic:
                dic[prod.product_tmpl_id.id] = {'cost': 0.0, 'count': 0}
            dic[prod.product_tmpl_id.id]['cost'] += prod.value_svl
            dic[prod.product_tmpl_id.id]['count'] += prod.qty_available
        for record in self:
            average_cost = 0.0
            if record.id in dic:
                average_cost = dic[record.id]['cost'] / dic[record.id]['count'] if dic[record.id]['count'] else 0.0
            record.avarage_cost = average_cost


class PricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    base = fields.Selection([
        ('list_price', 'Sales Price'),
        ('standard_price', 'Cost'),
        ('avarage_cost','Average Cost'),
        ('pricelist', 'Other Pricelist')], "Based on",
        default='list_price', required=True,
        help='Base price for computation.\n'
             'Sales Price: The base price will be the Sales Price.\n'
             'Cost Price : The base price will be the cost price.\n'
             'Other Pricelist : Computation of the base price based on another Pricelist.')


    def _compute_price(self, price, price_uom, product, quantity=1.0, partner=False):
        """Compute the unit price of a product in the context of a pricelist application.
           The unused parameters are there to make the full context available for overrides.
        """
        self.ensure_one()
        date = self.env.context.get('date') or fields.Date.today()
        convert_to_price_uom = (lambda price: product.uom_id._compute_price(price, price_uom))
        if self.compute_price == 'fixed':
            price = convert_to_price_uom(self.fixed_price)
        elif self.compute_price == 'percentage':
            price = (price - (price * (self.percent_price / 100))) or 0.0
        else:
            # complete formula
            price_limit = price
            price = (price - (price * (self.price_discount / 100))) or 0.0
            if self.base == 'standard_price':
                price_currency = product.cost_currency_id
            elif self.base == 'avarage_cost':
                price_currency = product.cost_currency_id
            elif self.base == 'pricelist':
                price_currency = self.currency_id
            # Already converted before to the pricelist currency
            else:
                price_currency = product.currency_id
            if self.price_round:
                price = tools.float_round(price, precision_rounding=self.price_round)

            def convert_to_base_price_currency(amount):
                return self.currency_id._convert(amount, price_currency, self.env.company, date, round=False)

            if self.price_surcharge:
                price_surcharge = convert_to_base_price_currency(self.price_surcharge)
                price_surcharge = convert_to_price_uom(price_surcharge)
                price += price_surcharge

            if self.price_min_margin:
                price_min_margin = convert_to_base_price_currency(self.price_min_margin)
                price_min_margin = convert_to_price_uom(price_min_margin)
                price = max(price, price_limit + price_min_margin)

            if self.price_max_margin:
                price_max_margin = convert_to_base_price_currency(self.price_max_margin)
                price_max_margin = convert_to_price_uom(price_max_margin)
                price = min(price, price_limit + price_max_margin)
        return price

    def _compute_price_rule(self, products_qty_partner, date=False, uom_id=False):
        """ Low-level method - Mono pricelist, multi products
        Returns: dict{product_id: (price, suitable_rule) for the given pricelist}

        Date in context can be a date, datetime, ...

            :param products_qty_partner: list of typles products, quantity, partner
            :param datetime date: validity date
            :param ID uom_id: intermediate unit of measure
        """
        self.ensure_one()
        if not date:
            date = self._context.get('date') or fields.Datetime.now()
        if not uom_id and self._context.get('uom'):
            uom_id = self._context['uom']
        if uom_id:
            # rebrowse with uom if given
            products = [item[0].with_context(uom=uom_id) for item in products_qty_partner]
            products_qty_partner = [(products[index], data_struct[1], data_struct[2]) for index, data_struct in enumerate(products_qty_partner)]
        else:
            products = [item[0] for item in products_qty_partner]

        if not products:
            return {}

        categ_ids = {}
        for p in products:
            categ = p.categ_id
            while categ:
                categ_ids[categ.id] = True
                categ = categ.parent_id
        categ_ids = list(categ_ids)

        is_product_template = products[0]._name == "product.template"
        if is_product_template:
            prod_tmpl_ids = [tmpl.id for tmpl in products]
            # all variants of all products
            prod_ids = [p.id for p in
                        list(chain.from_iterable([t.product_variant_ids for t in products]))]
        else:
            prod_ids = [product.id for product in products]
            prod_tmpl_ids = [product.product_tmpl_id.id for product in products]

        items = self._compute_price_rule_get_items(products_qty_partner, date, uom_id, prod_tmpl_ids, prod_ids, categ_ids)

        results = {}
        for product, qty, partner in products_qty_partner:
            results[product.id] = 0.0
            suitable_rule = False

            # Final unit price is computed according to `qty` in the `qty_uom_id` UoM.
            # An intermediary unit price may be computed according to a different UoM, in
            # which case the price_uom_id contains that UoM.
            # The final price will be converted to match `qty_uom_id`.
            qty_uom_id = self._context.get('uom') or product.uom_id.id
            qty_in_product_uom = qty
            if qty_uom_id != product.uom_id.id:
                try:
                    qty_in_product_uom = self.env['uom.uom'].browse([self._context['uom']])._compute_quantity(qty, product.uom_id)
                except UserError:
                    # Ignored - incompatible UoM in context, use default product UoM
                    pass

            # if Public user try to access standard price from website sale, need to call price_compute.
            # TDE SURPRISE: product can actually be a template
            price = product.price_compute('list_price')[product.id]

            price_uom = self.env['uom.uom'].browse([qty_uom_id])
            for rule in items:
                if not rule._is_applicable_for(product, qty_in_product_uom):
                    continue
                if rule.base == 'pricelist' and rule.base_pricelist_id:
                    price_tmp = rule.base_pricelist_id._compute_price_rule([(product, qty, partner)], date, uom_id)[product.id][0]  # TDE: 0 = price, 1 = rule
                    price = rule.base_pricelist_id.currency_id._convert(price_tmp, self.currency_id, self.env.company, date, round=False)
                else:
                    # if base option is public price take sale price else cost price of product
                    # price_compute returns the price in the context UoM, i.e. qty_uom_id
                    price = product.price_compute(rule.base)[product.id]

                if price is not False:
                    # pass the date through the context for further currency conversions
                    rule_with_date_context = rule.with_context(date=date)
                    price = rule_with_date_context._compute_price(price, price_uom, product, quantity=qty, partner=partner)
                    suitable_rule = rule
                break
            # Final price conversion into pricelist currency
            if suitable_rule and suitable_rule.compute_price != 'fixed' and suitable_rule.base != 'pricelist':
                if suitable_rule.base == 'standard_price':
                    cur = product.cost_currency_id
                elif suitable_rule.base == 'avarage_cost':
                    cur = product.currency_id
                price = cur._convert(price, self.currency_id, self.env.company, date, round=False)

            if not suitable_rule:
                cur = product.currency_id
                price = cur._convert(price, self.currency_id, self.env.company, date, round=False)

            results[product.id] = (price, suitable_rule and suitable_rule.id or False)

        return results