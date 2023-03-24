# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    exhibitor_contract_id = fields.Many2one("exhibitor.contract", string="Exhibitor Contract")
    exhibitor_package_component_ids = fields.One2many("exhibitor.package.components", "sale_order_id",
                                                      string="Exhibitor Package Components")
    exhibitor_payment_stage_ids = fields.One2many("exhibitor.payment.stages", "sale_order_id",
                                                  string="Exhibitor Payment Stages")
    space_type_id = fields.Many2one("exhibitor.space.type", string="Space Type")
    total_area = fields.Char(string="Total Area (m2)", compute="_compute_total_area")
    rate_per_m2 = fields.Char(string="Rate per m2 ($)", compute="_compute_rate_per_m2")
    stall_dimensions = fields.Char(string="Stall Dimensions", compute="_compute_stall_dimensions")
    hall_ids = fields.Many2many("event.activity.location", string="Hall Number", domain=[('event_id', '!=', False)])
    stand_ids = fields.One2many("so.stand.details", "sale_order_id", string="Stand Details")
    agreement_sent = fields.Boolean(string="Agreement Sent")
    delivery_note = fields.Char(string="Delivery Note")
    other_reference = fields.Char(string="Other Reference(s)")
    buyer_order_no = fields.Char(string="Buyer's Order No.")
    buyer_order_date = fields.Datetime(string="Buyer's Order Date")
    dispatched_document_no = fields.Char(string="Dispatched Document No.")
    dispatched_through = fields.Char(string="Dispatched Through")
    destination = fields.Char(string="Destination")
    state = fields.Selection(selection_add=[
        ('quote_accepted', 'Quotation Accepted'),
        ('review_quote', 'Review Quote'),
        ('in_progress', 'Agreement in Progress'),
        ('sale', 'Sales Order')])
    component_amount_total = fields.Binary(string="Component Total", compute="_compute_component_amount_total")
    enable_hotel_request = fields.Boolean(string="Enable Hotel Request")
    enable_shipment_section = fields.Boolean(string="Enable Shipment Section")
    hotel_special_inclusion_info = fields.Html(string="Hotel Information", readonly=False,
                                               compute="_compute_hotel_special_inclusion_info")
    include_special_condition = fields.Boolean(string="Include Special")

    # def _notify_get_recipients_groups(self, msg_vals=None):
    #     groups = super(SaleOrder, self)._notify_get_recipients_groups(msg_vals=msg_vals)
    #     if not self:
    #         return groups
    #
    #     self.ensure_one()
    #     customer_portal_group = next(group for group in groups if group[0] == 'portal_customer')
    #     if customer_portal_group:
    #         access_opt = customer_portal_group[2].setdefault('button_access', {})
    #         if self.event_id:
    #             access_opt['title'] = _('Accept & Sign Quotationss')
    #         _logger.info("\n\n\n***************** access_opt **************** %s\n\n\n", access_opt)
    #     return groups

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.check_payment_stage_validation()
        return res

    def write(self, vals):
        res = super().write(vals)
        self.check_payment_stage_validation()
        return res

    def check_payment_stage_validation(self):
        if self.exhibitor_payment_stage_ids:
            payment_stage_percentage_total = sum(self.exhibitor_payment_stage_ids.mapped('paid_percentage'))
            payment_stage_amount_total = sum(self.exhibitor_payment_stage_ids.mapped('paid_amount'))
            if payment_stage_percentage_total != 100:
                raise ValidationError(_("The percentage added in the payment stage is not equal to 100"))
            if payment_stage_amount_total != self.amount_total:
                raise ValidationError(
                    _("The amount added in the payment stage is not equal to the total amount of the quotation"))

    def action_quotation_send(self):
        res = super().action_quotation_send()
        if self.env.context.get('proforma'):
            mail_template = self.env.ref('techfuge_exhibitor_customisation.mail_template_sale_proforma_exhibitor')
        else:
            mail_template = self.env.ref('techfuge_exhibitor_customisation.mail_template_sale_quotation_exhibitor')
        res['context']['default_template_id'] = mail_template.id
        if self.opportunity_id:
            self.opportunity_id.stage_id = self.env.ref('crm.stage_lead3').id
        res['context']['default_email_layout_xmlid'] = False
        return res

    def generate_exhibitor_contract(self):
        if not self.hall_ids:
            raise UserError(_("Please add the agreement details"))

        if self.event_id:

            company_address = ''
            if self.opportunity_id.street:
                company_address += self.opportunity_id.street + ', '
            if self.opportunity_id.city:
                company_address += self.opportunity_id.city + ', '
            if self.opportunity_id.state_id:
                company_address += self.opportunity_id.state_id.name

            if self.exhibitor_contract_id:
                self.exhibitor_contract_id.commercial_items_ids.unlink()
                self.exhibitor_contract_id.stand_ids.unlink()
                self.exhibitor_contract_id.exhibitor_payment_stage_ids.unlink()

            commercial_items = []
            for line in self.order_line:
                commercial_items.append((0, 0, {
                    'product_template_id': line.product_template_id.id,
                    'name': line.name,
                    'product_uom_qty': line.product_uom_qty,
                    'product_uom_id': line.product_uom.id,
                    'price_unit': line.price_unit,
                    'tax_ids': line.tax_id.ids,
                    'price_subtotal': line.price_subtotal,
                    'price_tax': line.price_tax,
                    'price_total': line.price_total
                }))

            stand_details = []
            for stand in self.stand_ids:
                stand_details.append((0, 0, {
                    'stand_id': stand.stand_id.id,
                    'hall_id': stand.hall_id.id,
                    'stand_description': stand.stand_description,
                    'stand_width': stand.stand_width,
                    'stand_depth': stand.stand_depth,
                    'stand_size': stand.stand_size
                }))

            payment_stages = []
            for payment in self.exhibitor_payment_stage_ids:
                payment_stages.append((0, 0, {
                    'name': payment.name,
                    'payment_type': payment.payment_type,
                    'paid_percentage': payment.paid_percentage,
                    'paid_amount': payment.paid_amount,
                    'payment_due_date': payment.payment_due_date
                }))

            exhibitor_contract_vals = {
                'exhibitor_name': self.partner_id.name,
                'mobile': self.opportunity_id.mobile,
                'email': self.opportunity_id.email_from,
                'landline': self.opportunity_id.phone,
                'company_name': self.opportunity_id.partner_name,
                'company_address': company_address,
                'country_name': self.opportunity_id.country_id.name if self.opportunity_id.country_id else '',
                'sale_order_id': self.id,
                'so_amount_total': self.amount_total,
                'commercial_items_ids': commercial_items,
                'stand_ids': stand_details,
                'exhibitor_payment_stage_ids': payment_stages,
                'event_id': self.event_id.id,
                'enable_hotel_request': self.enable_hotel_request,
                'enable_shipment_section': self.enable_shipment_section,
                'partner_id': self.partner_id.id
            }

            if not self.exhibitor_contract_id:
                exhibitor_contract = self.env['exhibitor.contract'].create(exhibitor_contract_vals)
                self.exhibitor_contract_id = exhibitor_contract.id
                self.partner_id.exhibitor_contract_id = exhibitor_contract.id
            else:
                self.exhibitor_contract_id.update(exhibitor_contract_vals)

            self.sudo().write({
                'agreement_sent': True,
                'state': 'in_progress'
            })

        mail_template = self.env.ref('techfuge_exhibitor_customisation.mail_template_sale_exhibitor_agreement')
        lang = self.env.context.get('lang')
        ctx = {
            'default_model': 'sale.order',
            'default_res_id': self.id,
            'default_use_template': True,
            'default_template_id': mail_template.id if mail_template else None,
            'default_composition_mode': 'comment',
            'default_email_layout_xmlid': 'mail.mail_notification_layout_with_responsible_signature',
            'force_email': True,
            'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }

    def action_confirm(self):
        res = super().action_confirm()
        user = self.user_id if self.user_id else self.env.ref('base.user_admin')
        if self.agreement_sent:
            if self.opportunity_id:
                self.opportunity_id.action_set_won()
                self.opportunity_id.create_portal_user_for_exhibitor()
            return res
        else:
            self.with_user(user.id).sudo().write({
                'state': 'quote_accepted'
            })

    def action_view_exhibitor_contract(self):
        action = self.env['ir.actions.actions']._for_xml_id(
            'techfuge_exhibitor_customisation.action_view_exhibitor_contracts')
        form_view = [(self.env.ref('techfuge_exhibitor_customisation.view_exhibitor_contract_form').id, 'form')]
        if 'views' in action:
            action['views'] = form_view + [(state, view) for state, view in action['views'] if view != 'form']
        else:
            action['views'] = form_view
        action['res_id'] = self.exhibitor_contract_id.id
        return action

    @api.depends('stand_ids')
    def _compute_total_area(self):
        for order in self:
            order.total_area = str(sum(order.stand_ids.mapped('stand_size')))

    def _compute_rate_per_m2(self):
        for order in self:
            order.rate_per_m2 = ''
            if order.order_line:
                order.rate_per_m2 = order.order_line.mapped('price_unit')[0]

    @api.depends('stand_ids')
    def _compute_stall_dimensions(self):
        for order in self:
            order.stall_dimensions = ''
            if order.order_line:
                width = str(sum(order.stand_ids.mapped('stand_width')))
                depth = str(sum(order.stand_ids.mapped('stand_depth')))
                order.stall_dimensions = width + ' x ' + depth

    def _compute_component_amount_total(self):
        for order in self:
            component_lines = order.exhibitor_package_component_ids
            order.component_amount_total = self.env['account.tax']._prepare_tax_totals(
                [x._convert_to_tax_base_line_dict() for x in component_lines],
                order.currency_id or order.company_id.currency_id,
            )

    def _compute_hotel_special_inclusion_info(self):
        for order in self:
            order.hotel_special_inclusion_info = '<p style="margin-left: 15px; line-height: 1.4;"> ' \
                                                 '25. SPECIAL INCLUSIONS </p> ' \
                                                 '<p style="margin-left: 30px; line-height: 1.4;"> ' \
                                                 '<ul style="margin-left: 30px; line-height: 1.4;"> <li> ' \
                                                 ' 4 Nights hotel stay including breakfast on double occupancy basis ' \
                                                 'for each stand </li> <li>Stand construction for MDF stall with ' \
                                                 'lighting</li>  <li>Shipment included from Goods origin Port to ' \
                                                 'the stall</li> <li>Shipment allocation is 1 cbm for every 10 sqm ' \
                                                 'of space</li> </ul> </p>'
