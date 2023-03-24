# -*- coding: utf-8 -*-

from odoo import api, fields, models


class ExhibitorPaymentStages(models.Model):
    _name = 'exhibitor.payment.stages'
    _description = 'Exhibitor Payment Stages'

    exhibitor_contract_id = fields.Many2one("exhibitor.contract", string="Exhibitor Contract")
    sale_order_id = fields.Many2one("sale.order", string="Sale Order")
    move_id = fields.Many2one("account.move", string="Invoice")
    name = fields.Char(string="Description")
    payment_type = fields.Selection(selection=[
        ('percentage', 'Percentage'),
        ('amount', 'Amount')
    ], string="Type")
    paid_percentage = fields.Float(string="Percentage(%)")
    paid_amount = fields.Float(string="Amount", compute="_compute_paid_amount")
    payment_due_date = fields.Date(string="Due Date")
    currency_id = fields.Many2one(related='sale_order_id.currency_id')

    @api.depends('paid_percentage', 'sale_order_id.order_line')
    def _compute_paid_amount(self):
        for payment in self:
            payment.paid_amount = 0
            if payment.paid_percentage:
                paid_amount = (payment.sale_order_id.amount_total * payment.paid_percentage) / 100
                payment.paid_amount = paid_amount
