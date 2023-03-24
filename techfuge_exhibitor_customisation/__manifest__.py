# -*- coding: utf-8 -*-
{
    'name': "Techfuge Exhibitor Customisations",
    'summary': """ Techfuge Exhibitor Customisations for Event Management""",
    'description': """
        Techfuge Exhibitor Customisations for Event Management
    """,
    'author': "Pragmatic",
    'website': "https://www.pragtech.co.in/",
    'category': 'Events',
    'version': '3.9',
    # any module necessary for this one to work correctly
    'depends': ['techfuge_customisation', 'crm_iap_enrich', 'crm_sms'],
    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'reports/sale_order_report.xml',
        'reports/invoice_report.xml',
        'reports/exhibitor_agreement_report.xml',
        'reports/exhibitor_badge_report.xml',
        'data/ir_sequence_data.xml',
        'data/exhibitor_data.xml',
        'data/ir_action_data.xml',
        'data/mail_template_data.xml',
        'views/exhibitor_request_type_views.xml',
        'views/exhibitor_document_type_views.xml',
        'views/exhibitor_contract_views.xml',
        'views/exhibitor_hotel_request_views.xml',
        'views/exhibitor_other_request_views.xml',
        'views/crm_lead_views.xml',
        'views/event_views.xml',
        'views/event_registration_views.xml',
        'views/res_partner_views.xml',
        'views/res_company_views.xml',
        'views/sale_views.xml',
        'views/account_move_views.xml',
        'views/exhibitor_space_type_views.xml',
        'views/sale_portal_templates.xml',
        'views/exhibitor_dashboard_templates.xml',
        'views/exhibitor_dashboard_company_templates.xml',
        'views/exhibitor_dashboard_attendee_templates.xml',
        'views/exhibitor_dashboard_hotel_templates.xml',
        'views/exhibitor_dashboard_contractor_templates.xml',
        'views/exhibitor_dashboard_document_templates.xml',
        'views/exhibitor_dashboard_shipment_templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'techfuge_exhibitor_customisation/static/src/css/exhibitor_dashboard.css',
            'techfuge_exhibitor_customisation/static/src/js/exhibitor_dashboard.js',
        ],
        'web.report_assets_common': [
            'techfuge_exhibitor_customisation/static/src/css/proforma_invoice.css',
            'techfuge_exhibitor_customisation/static/src/scss/exhibitor_badge_report.scss',
        ],
    },
    'license': 'LGPL-3',
}
