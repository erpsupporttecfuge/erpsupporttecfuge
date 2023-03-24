# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ExhibitorOtherRequest(models.Model):
    _name = 'exhibitor.other.request'
    _description = 'Exhibitor Other Request'
    _rec_name = 'attendee_full_name'

    exhibitor_contract_id = fields.Many2one("exhibitor.contract", string="Exhibitor Contract")
    attendee_full_name = fields.Char(string="Attendee Name")
    attendee_id = fields.Many2one("event.registration", string="Attendee")
    event_id = fields.Many2one("event.event", string="Event")
    request_type_id = fields.Many2one("exhibitor.request.type", string="Request Type")
    request_note = fields.Text(string="Note")
    uploaded_document_ids = fields.One2many("exhibitor.uploaded.documents", "other_request_id",
                                            string="Uploaded Documents")
    status = fields.Selection(selection=[
        ('pending', 'Pending'),
        ('approved', 'Approved')
    ], string="Status", default="pending")
