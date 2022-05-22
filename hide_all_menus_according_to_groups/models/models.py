# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class hide_all_menus_according_to_groups(models.Model):
#     _name = 'hide_all_menus_according_to_groups.hide_all_menus_according_to_groups'
#     _description = 'hide_all_menus_according_to_groups.hide_all_menus_according_to_groups'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
