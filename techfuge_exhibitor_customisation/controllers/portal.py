# -*- coding: utf-8 -*-

import json
import logging
import requests
import base64

from odoo import http
from odoo.http import request, Response
from odoo.exceptions import Warning
from datetime import datetime
from odoo.osv.expression import OR, AND

_logger = logging.getLogger(__name__)


class ExhibitorDashboardController(http.Controller):

    @http.route('/exhibitor_dashboard', type='http', auth='user', website=True, csrf=False)
    def portal_exhibitor_dashboard(self, **kw):
        values = {}
        return request.render("techfuge_exhibitor_customisation.portal_exhibitor_dashboard", values)

    @http.route('/exhibitor_dashboard/company_details', type='http', auth='user', website=True)
    def portal_exhibitor_dashboard_company_details(self, **kw):
        user = request.env.user
        exhibitor_contract = request.env['exhibitor.contract'].sudo().search(
            [('id', '=', user.partner_id.exhibitor_contract_id.id)])
        halls = []
        stands = []
        package_options = []
        for hall in exhibitor_contract.sale_order_id.hall_ids:
            if hall.name not in halls:
                halls.append(hall.name)
        for stand in exhibitor_contract.sale_order_id.stand_ids:
            if stand.stand_id.stand_number not in stands:
                stands.append(stand.stand_id.stand_number)
        for package in exhibitor_contract.sale_order_id.order_line:
            if package.product_template_id.name not in package_options:
                package_options.append(package.product_template_id.name)
        values = {
            'exhibitor_contract': exhibitor_contract,
            'halls': halls,
            'stands': stands,
            'package_options': package_options,
        }
        return request.render("techfuge_exhibitor_customisation.portal_exhibitor_dashboard_company_details", values)

    @http.route('/exhibitor_dashboard/attendee_details', type='http', auth='user', website=True)
    def portal_exhibitor_dashboard_attendee_details(self, **kw):
        values = {}
        user = request.env.user
        exhibitor_contract = request.env['exhibitor.contract'].sudo().search([('partner_id', '=', user.partner_id.id)],
                                                                             limit=1)
        if exhibitor_contract:
            exhibitor_attendees = request.env['event.registration'].sudo().search(
                [('exhibitor_contract_id', '=', exhibitor_contract.id)], limit=1)
            values.update({
                'exhibitor_contract': exhibitor_contract,
                'exhibitor_attendees': exhibitor_attendees
            })
        return request.render("techfuge_exhibitor_customisation.portal_exhibitor_dashboard_attendee_details", values)

    @http.route('/submit/attendee_badge_request', type='http', auth='public', csrf=False, website=True)
    def portal_submit_attendee_badge_request(self, **kwarg):
        data = kwarg
        attendee_vals = {}
        admin_user = request.env.ref('base.user_admin')
        user = request.env.user
        exhibitor_contract = request.env['exhibitor.contract'].sudo().search([('partner_id', '=', user.partner_id.id)],
                                                                             limit=1)
        exhibitor_contract_id = False
        try:
            if 'exh_title' in data:
                attendee_vals['title'] = str(data['exh_title'])

            if 'exh_first_name' in data:
                attendee_vals['name'] = str(data['exh_first_name'])

            if 'exh_last_name' in data:
                attendee_vals['last_name'] = str(data['exh_last_name'])

            if 'exh_designation' in data:
                attendee_vals['designation'] = str(data['exh_designation'])

            if 'exh_mobile' in data:
                attendee_vals['mobile'] = str(data['exh_mobile'])

            if 'exh_email' in data:
                attendee_vals['email'] = str(data['exh_email'])

            if 'exh_landline' in data:
                attendee_vals['phone'] = str(data['exh_landline'])

            if exhibitor_contract:
                exhibitor_contract_id = exhibitor_contract

            if attendee_vals:
                attendee_vals.update({
                    'attendee_type_id': request.env.ref('techfuge_customisation.attendee_type_data_exhibitor').id,
                    'source_of_registration': 'from_website',
                    'event_id': exhibitor_contract_id.event_id.id,
                    'exhibitor_contract_id': exhibitor_contract_id.id,
                    'company_name': exhibitor_contract_id.company_name
                })

            attendee_rec = request.env['event.registration'].with_user(admin_user.id).sudo().create(attendee_vals)
            attendee_rec.send_visitor_registration_mail()
            attendee_rec.badge_sent = True

            if attendee_rec and exhibitor_contract_id:
                exhibitor_contract_id.badge_ids = [(6, 0, [attendee_rec.id])]

        except Exception as error:
            _logger.warning('Visitor Registration Failed Due to : %s', error)
        return request.redirect('/exhibitor_dashboard/attendee_details')

    @http.route('/exhibitor_dashboard/hotel_requests', type='http', auth='user', website=True)
    def portal_exhibitor_dashboard_hotel_requests(self, **kw):
        values = {}
        user = request.env.user
        exhibitor_contract = request.env['exhibitor.contract'].sudo().search([('partner_id', '=', user.partner_id.id)],
                                                                             limit=1)
        if exhibitor_contract:
            exhibitor_attendees = request.env['event.registration'].sudo().search(
                [('exhibitor_contract_id', '=', exhibitor_contract.id)])
            values.update({
                'exhibitor_contract': exhibitor_contract,
                'exhibitor_attendees': exhibitor_attendees
            })
        return request.render("techfuge_exhibitor_customisation.portal_exhibitor_dashboard_hotel_requests", values)

    @http.route('/exhibitor_dashboard/contractor_details', type='http', auth='user', website=True)
    def portal_exhibitor_dashboard_contractor_details(self, **kw):
        values = {}
        return request.render("techfuge_exhibitor_customisation.portal_exhibitor_dashboard_contractor_details", values)

    @http.route('/exhibitor_dashboard/uploaded_documents', type='http', auth='user', website=True)
    def portal_exhibitor_dashboard_uploaded_documents(self, **kw):
        values = {}
        return request.render("techfuge_exhibitor_customisation.portal_exhibitor_dashboard_uploaded_documents", values)

    @http.route('/exhibitor_dashboard/shipment_details', type='http', auth='user', website=True)
    def portal_exhibitor_dashboard_shipment_details(self, **kw):
        values = {}
        return request.render("techfuge_exhibitor_customisation.portal_exhibitor_dashboard_shipment_details", values)

    @http.route('/exhibitor_dashboard/booked_stands', type='http', auth='user', website=True)
    def portal_exhibitor_dashboard_booked_stands(self, **kw):
        values = {}
        return request.render("techfuge_exhibitor_customisation.portal_exhibitor_dashboard_booked_stands", values)
