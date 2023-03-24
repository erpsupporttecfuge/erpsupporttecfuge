# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ExhibitorContract(models.Model):
    _name = 'exhibitor.contract'
    _description = 'Exhibitor Contract'
    _inherit = ['mail.thread']

    name = fields.Char(string='Name', default=lambda self: _('New'), readonly=True)
    exhibitor_name = fields.Char(string="Exhibitor Name", readonly=True)
    title = fields.Selection(selection=[
        ('Mr.', 'Mr.'),
        ('Ms.', 'Ms.'),
        ('Mrs.', 'Mrs.'),
    ], string='Title', readonly=True)
    first_name = fields.Char(string="First Name", readonly=True)
    last_name = fields.Char(string="Last Name", readonly=True)
    mobile = fields.Char(string="Mobile", readonly=True)
    landline = fields.Char(string="Landline", readonly=True)
    email = fields.Char(string="Email", readonly=True)
    company_name = fields.Char(string="Company Name", readonly=True)
    company_address = fields.Char(string="Company Address", readonly=True)
    country_name = fields.Char(string="Country", readonly=True)
    partner_id = fields.Many2one("res.partner", string="Partner", readonly=True)
    sale_order_id = fields.Many2one("sale.order", string="Sale Order", readonly=True)
    so_amount_total = fields.Monetary(string="SO Amount Total", readonly=True)
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.company, readonly=True)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', readonly=True)
    event_id = fields.Many2one("event.event", string="Event", readonly=True)
    no_of_stands = fields.Integer(string="No. of Stands")
    no_of_badges = fields.Integer(string="Badge Count")
    enable_hotel_request = fields.Boolean(string="Enable Hotel Request")
    enable_shipment_section = fields.Boolean(string="Enable Shipment Section")
    amount_untaxed = fields.Monetary(string="Untaxed Amount", store=True, compute='_compute_amounts')
    amount_tax = fields.Monetary(string="Taxes", store=True, compute='_compute_amounts')
    amount_total = fields.Monetary(string="Total", store=True, compute='_compute_amounts')
    tax_totals = fields.Binary(compute='_compute_tax_totals', exportable=False)
    stand_ids = fields.One2many("contract.stand.details", "exhibitor_contract_id", string="Stand Details")
    commercial_items_ids = fields.One2many("exhibitor.commercial.items", "exhibitor_contract_id",
                                           string="Commercial Items")
    badge_ids = fields.One2many("event.registration", "exhibitor_contract_id", string="Badge Details")
    hotel_request_ids = fields.One2many("exhibitor.hotel.request", "exhibitor_contract_id", string="Hotel Requests")
    shipment_detail_ids = fields.One2many("exhibitor.shipment.details", "exhibitor_contract_id",
                                          string="Shipment Details")
    other_request_ids = fields.One2many("exhibitor.other.request", "exhibitor_contract_id", string="Other Requests")
    uploaded_document_ids = fields.One2many("exhibitor.uploaded.documents", "exhibitor_contract_id",
                                            string="Uploaded Documents")
    contractor_ids = fields.One2many("exhibitor.contractor.details", "exhibitor_contract_id",
                                     string="Contractor Details")
    exhibitor_payment_stage_ids = fields.One2many("exhibitor.payment.stages", "exhibitor_contract_id",
                                                  string="Exhibitor Payment Stages")

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('exhibitor.contract') or _("New")
        return super(ExhibitorContract, self).create(vals_list)

    @api.depends('commercial_items_ids.price_subtotal', 'commercial_items_ids.price_tax',
                 'commercial_items_ids.price_total')
    def _compute_amounts(self):
        for contract in self:
            commercial_item_lines = contract.commercial_items_ids
            contract.amount_untaxed = sum(commercial_item_lines.mapped('price_subtotal'))
            contract.amount_total = sum(commercial_item_lines.mapped('price_total'))
            contract.amount_tax = sum(commercial_item_lines.mapped('price_tax'))

    def _compute_tax_totals(self):
        for contract in self:
            order_lines = contract.sale_order_id.order_line.filtered(lambda x: not x.display_type)
            contract.tax_totals = self.env['account.tax']._prepare_tax_totals(
                [x._convert_to_tax_base_line_dict() for x in order_lines],
                contract.sale_order_id.currency_id or contract.sale_order_id.company_id.currency_id,
            )

    def write(self, vals):
        res = super().write(vals)
        if self.no_of_stands and self.exhibitor_stand_ids:
            if len(self.exhibitor_stand_ids) > self.no_of_stands:
                raise ValidationError(_("You cannot add more stands than the defined number of stands"))
        return res
