# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ExhibitorDocumentType(models.Model):
    _name = 'exhibitor.document.type'
    _description = 'Exhibitor Document Type'

    name = fields.Char(string='Name')
