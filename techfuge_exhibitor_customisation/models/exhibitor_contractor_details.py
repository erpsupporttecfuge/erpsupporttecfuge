# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ExhibitorContractorDetails(models.Model):
    _name = 'exhibitor.contractor.details'
    _description = 'Exhibitor Contractor Details'

    exhibitor_contract_id = fields.Many2one("exhibitor.contract", string="Exhibitor Contract")
    company_name = fields.Char(string="Company Name")
    company_address = fields.Char(string="Company Address")
    company_phone = fields.Char(string="Company Phone")
    company_email = fields.Char(string="Company Email")
    contact_person_name = fields.Char(string="Name")
    contact_person_designation = fields.Char(string="Designation")
    contact_person_mobile = fields.Char(string="Mobile")
    contact_person_phone = fields.Char(string="Landline")
    contact_person_email = fields.Char(string="Email")
    upload_permit = fields.Binary(string="Upload Permit")
    status = fields.Selection(selection=[('pending', 'Pending'), ('approved', 'Approved')], default="pending",
                              string="Status")

    def approve_contractor(self):
        self.status = 'approved'
