# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    made = fields.Many2one('product.made', "Made")
    brand = fields.Many2one('product.brand', "Brand")
    category = fields.Many2one('product.class', "Class")
    measurement = fields.Many2one('product.measurement', "Measurement")


class ProductMade(models.Model):
    _name = 'product.made'
    _description = "Product Made"

    name = fields.Char("Made")


class ProductClass(models.Model):
    _name = 'product.class'
    _description = "Product Class"

    name = fields.Char("Class")


class ProductBrand(models.Model):
    _name = 'product.brand'
    _description = "Product Brand"

    name = fields.Char("Brand")


class ProductMeasurement(models.Model):
    _name = 'product.measurement'
    _description = "Product Measurement"

    name = fields.Char("Measurement")
