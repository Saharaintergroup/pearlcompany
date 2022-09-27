# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    commission_percentage = fields.Float("Commission Percentage %")
    commission_depends = fields.Selection([('invoiced', 'Invoiced'),
                                           ('paid', 'Paid')], "Commission Depends", default='invoiced')
    has_commission = fields.Boolean("Has Commission")
