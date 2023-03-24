# -*- coding: utf-8 -*-

from odoo import api, fields, models
import random


class CRMLead(models.Model):
    _inherit = 'crm.lead'

    sent_registration_mails = fields.Boolean(string="Sent Registration Mail", default=False)
    agent_id = fields.Many2one("res.partner", string="Agent", domain=[('is_agent', '=', True)])

    def send_exhibitor_registration_mail_to_exhibitor(self):
        user = self.env.ref('base.user_admin')
        mail_template = self.env.ref(
            'techfuge_customisation.email_template_exhibitor_registration_mail_to_exhibitor')
        mail_template.with_user(user.id).sudo().send_mail(self.id, force_send=True)

    def send_exhibitor_registration_mail_to_planner(self):
        user = self.env.ref('base.user_admin')
        mail_template = self.env.ref(
            'techfuge_customisation.email_template_exhibitor_registration_mail_to_planner')
        mail_template.sudo().with_user(user.id).send_mail(self.id, force_send=True)

    @api.model_create_multi
    def create(self, vals_list):
        res = super(CRMLead, self).create(vals_list)

        partner_full_name = ''
        if res.title_abbr:
            partner_full_name += res.title_abbr + ' '
        if res.contact_name:
            partner_full_name += res.contact_name + ' '
        if res.last_name:
            partner_full_name += res.last_name
        res.partner_full_name = partner_full_name

        if res.event_id and res.event_id.analytic_account_id:
            res.analytic_account_id = res.event_id.analytic_account_id.id

        if res.event_id:
            if res.partner_name:
                res.name = res.event_id.name + ' -  ' + res.partner_name
            res.send_exhibitor_registration_mail_to_exhibitor()
            res.send_exhibitor_registration_mail_to_planner()
            res.sent_registration_mails = True

        return res

    def _prepare_contact_name_from_partner(self, partner):
        res = super()._prepare_contact_name_from_partner(partner=partner)
        if self.event_id:
            res['contact_name'] = self.contact_name
        return res

    def action_send_exhibitor_registration_mails(self):
        for lead in self.filtered(lambda l: not l.sent_registration_mails):
            if lead.event_id:
                lead.send_exhibitor_registration_mail_to_exhibitor()
                lead.send_exhibitor_registration_mail_to_planner()
                lead.sent_registration_mails = True

    def _prepare_customer_values(self, partner_name, is_company=False, parent_id=False):
        res = super()._prepare_customer_values(partner_name, is_company=is_company, parent_id=parent_id)

        if partner_name == self.contact_name:
            res['name'] = self.partner_full_name

        if self.event_id and res['is_company']:
            res['customer_rank'] = 1
        return res

    def _prepare_opportunity_quotation_context(self):
        res = super()._prepare_opportunity_quotation_context()
        if self.event_id:
            if self.analytic_account_id:
                analytic_account = self.analytic_account_id
            else:
                analytic_account = self.event_id.analytic_account_id
            res['default_analytic_account_id'] = analytic_account.id
            res['default_event_id'] = self.event_id.id
        return res

    @api.model
    def create_portal_user_for_exhibitor(self):
        """ For creating a portal user for the exhibitor"""
        res_users = self.env['res.users'].sudo()
        user_password = self.generate_random_password()
        if self.partner_full_name:
            partner_full_name = self.partner_full_name
        else:
            partner_full_name = ''
            if self.title_abbr:
                partner_full_name += self.title_abbr + ' '
            if self.contact_name:
                partner_full_name += self.contact_name + ' '
            if self.last_name:
                partner_full_name += self.last_name

        if not res_users.search([('login', '=', self.email_from)]):
            if self.contact_name and self.email_from:
                exhibitor_user = res_users.with_context(create_exhibitor_user=True).create({
                    'name': partner_full_name,
                    'email': self.email_from,
                    'login': self.email_from,
                    'password': user_password,
                    'groups_id': [(6, 0, [self.env.ref('base.group_portal').id])],
                })
                self.sudo().write({
                    'exhibitor_user_id': exhibitor_user.id,
                    'exhibitor_user_login': exhibitor_user.login,
                    'exhibitor_user_password': user_password,
                })
                user = self.env.ref('base.user_admin')
                mail_template = self.env.ref(
                    'techfuge_customisation.email_template_exhibitor_registration_confirmed_mail')
                mail_template.with_user(user.id).sudo().with_context(partner_full_name=partner_full_name).send_mail(
                    self.id, force_send=True)

    def generate_random_password(self):
        """ Returns random password string containing alphanumeric characters """

        alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pw_length = 8
        password = ""
        for i in range(pw_length):
            next_index = random.randrange(len(alphabet))
            password = password + alphabet[next_index]
        return password
