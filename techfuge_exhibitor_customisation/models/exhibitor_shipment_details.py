# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ExhibitorShipmentDetails(models.Model):
    _name = 'exhibitor.shipment.details'
    _description = 'Exhibitor Shipment Details'

    exhibitor_contract_id = fields.Many2one("exhibitor.contract", string="Exhibitor Contract")
    event_id = fields.Many2one("event.event", string="Event")
    total_shipment_volume = fields.Float(string="Total Shipment Volume")
    allowed_cbm = fields.Float(string="Allowed CBM / 10 SQM")
    extra_cbm = fields.Float(string="Extra CBM")
    exceeding_charges = fields.Float(string="Exceeding Volume Charges / CBM")
    additional_charges = fields.Float(string="Additional Charges")
    final_charges = fields.Float(string="Final Charges")
    no_of_cartons = fields.Float(string="No of Cartons")
    net_weight = fields.Float(string="Net Weight")
    total_weight = fields.Float(string="Total Weight")
    port_of_landing = fields.Char(string="Name of Port of Landing")
    port_of_arrival_in_uae = fields.Char(string="Port of Arrival in UAE")
