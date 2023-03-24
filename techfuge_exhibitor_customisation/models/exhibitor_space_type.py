# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ExhibitorSpaceType(models.Model):
    _name = 'exhibitor.space.type'
    _description = 'Exhibitor Space Type'

    name = fields.Char(string="Name")
    product_template_id = fields.Many2one("product.template", string="Product")
