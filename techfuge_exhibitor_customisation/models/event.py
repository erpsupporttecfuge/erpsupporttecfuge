# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class Event(models.Model):
    _inherit = 'event.event'

    exhibitor_contracts_count = fields.Integer(string='No. of Contracts', store=False, readonly=True,
                                               compute='_compute_exhibitor_contracts_count')
    exhibitor_stand_ids = fields.One2many("exhibitor.stand.details", "event_id", string="Stand Details")
    event_logo = fields.Binary(string="Event Logo")

    def _compute_exhibitor_contracts_count(self):
        for event in self:
            exhibitor_contracts_count = self.env['exhibitor.contract'].sudo().search_count([])
            event.exhibitor_contracts_count = exhibitor_contracts_count


class EventRegistration(models.Model):
    _inherit = 'event.registration'

    exhibitor_contract_id = fields.Many2one("exhibitor.contract", string="Exhibitor Contract")
