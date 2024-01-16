# -*- coding: utf-8 -*-

# from odoo import models, fields, api


# class gemini_discuss_integration(models.Model):
#     _name = 'gemini_discuss_integration.gemini_discuss_integration'
#     _description = 'gemini_discuss_integration.gemini_discuss_integration'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

