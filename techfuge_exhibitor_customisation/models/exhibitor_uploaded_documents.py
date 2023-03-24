# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ExhibitorUploadedDocuments(models.Model):
    _name = 'exhibitor.uploaded.documents'
    _description = 'Exhibitor Uploaded Documents'

    exhibitor_contract_id = fields.Many2one("exhibitor.contract", string="Exhibitor Contract")
    hotel_request_id = fields.Many2one("exhibitor.hotel.request", string="Hotel Request")
    other_request_id = fields.Many2one("exhibitor.other.request", string="Other Request")
    document_type_id = fields.Many2one("exhibitor.document.type", string="Document Type")
    document_note = fields.Text(string="Note")
    document_file = fields.Binary(string="File")
    allow_upload_again = fields.Boolean(string="Re upload")
