# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    cash_sale_customer = fields.Boolean("Cash Sale Customer")
