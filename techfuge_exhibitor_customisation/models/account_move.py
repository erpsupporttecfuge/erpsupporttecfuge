# -*- coding: utf-8 -*-

from odoo import api, fields, models


class AccountMove(models.Model):
    _inherit = 'account.move'

    exhibitor_package_component_ids = fields.One2many("exhibitor.package.components", "move_id",
                                                      string="Exhibitor Package Components")
    exhibitor_payment_stage_ids = fields.One2many("exhibitor.payment.stages", "move_id",
                                                  string="Exhibitor Payment Stages")

    def action_invoice_sent(self):
        res = super().action_invoice_sent()
        mail_template = self.env.ref('techfuge_exhibitor_customisation.mail_template_send_invoice_exhibitor')
        res['context']['default_template_id'] = mail_template.id
        return res
