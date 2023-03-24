# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fax = fields.Char(string="Fax")
    exhibitor_contract_id = fields.Many2one("exhibitor.contract", string="Exhibitor Contract")
    is_agent = fields.Boolean(string="Is Agent")
