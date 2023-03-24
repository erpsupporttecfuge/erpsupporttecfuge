# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ExhibitorHotelRequest(models.Model):
    _name = 'exhibitor.hotel.request'
    _description = 'Exhibitor Hotel Request'
    _rec_name = 'attendee_full_name'

    exhibitor_contract_id = fields.Many2one("exhibitor.contract", string="Exhibitor Contract")
    attendee_id = fields.Many2one("event.registration", string="Attendee")
    event_id = fields.Many2one("event.event", string="Event")
    attendee_full_name = fields.Char(string="Attendee Name")
    room_type = fields.Char(string="Room Type")
    no_of_rooms = fields.Integer(string="No. of Rooms")
    checkin_datetime = fields.Datetime(string="Check In Date")
    checkout_datetime = fields.Datetime(string="Check Out Date")
    no_of_nights = fields.Integer(string="No. of Nights", compute="_compute_number_of_nights")
    booking_status = fields.Selection(selection=[
        ('pending', 'Pending'),
        ('completed', 'Completed')
    ], string="Booking Status", default="pending")
    upload_voucher = fields.Binary(string="Upload Voucher")
    uploaded_document_ids = fields.One2many("exhibitor.uploaded.documents", "hotel_request_id",
                                            string="Uploaded Documents")

    @api.depends('checkin_datetime', 'checkout_datetime')
    def _compute_number_of_nights(self):
        for rec in self:
            no_of_nights = 0
            if rec.checkin_datetime and rec.checkout_datetime:
                date_diff = rec.checkout_datetime - rec.checkin_datetime
                no_of_nights = date_diff.days
            rec.no_of_nights = no_of_nights
