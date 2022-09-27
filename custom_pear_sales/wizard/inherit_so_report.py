from odoo import fields, models, api
from dateutil.relativedelta import relativedelta
from datetime import date, datetime


class InheritCreateWizard(models.TransientModel):
    _inherit = 'so.report'
    _description = 'So Report'


    def _get_report_pdf(self):
        cash_so_report = self.env['sale.order'].sudo().search(
            [('user_id', '=', self.user_id.id),
             ('partner_id.cash_sale_customer', '=', False)])
        no_cash_so_report = self.env['sale.order'].sudo().search(
            [('user_id', '=', self.user_id.id),
             ('partner_id.cash_sale_customer', '=', True)])
        out_refund = self.env['account.move'].sudo().search(
            [('invoice_date', '=', self.date), ('invoice_user_id', '=', self.user_id.id),
             ('move_type', '=', 'out_refund')])
        receipts_cash = self.env['account.payment'].sudo().search(
            [('date', '=', self.date), ('user_id', '=', self.user_id.id),
             ('payment_type', '=', 'inbound'), ('journal_id.type', '=', 'cash')])
        receipts_bank = self.env['account.payment'].sudo().search(
            [('date', '=', self.date), ('user_id', '=', self.user_id.id),
             ('payment_type', '=', 'inbound'), ('journal_id.type', '=', 'bank')])
        payments_cash = self.env['account.payment'].sudo().search(
            [('date', '=', self.date), ('user_id', '=', self.user_id.id),
             ('payment_type', '=', 'outbound'), ('journal_id.type', '=', 'cash')])
        payments_bank = self.env['account.payment'].sudo().search(
            [('date', '=', self.date), ('user_id', '=', self.user_id.id),
             ('payment_type', '=', 'outbound'), ('journal_id.type', '=', 'bank')])
        total_cash = 0.0
        total_no_cash = 0.0
        total_out_refund = 0.0
        total_receipts_cash = 0.0
        total_receipts_bank = 0.0
        total_payments_cash = 0.0
        total_payments_bank = 0.0
        for so in cash_so_report:
            if so.date_order.date() == self.date:
                total_cash += so.amount_total
        for so in no_cash_so_report:
            if so.date_order.date() == self.date:
                total_no_cash += so.amount_total
        for out in out_refund:
            total_out_refund += out.amount_total
        for rec_cash in receipts_cash:
            total_receipts_cash += rec_cash.amount
        for rec_bank in receipts_bank:
            total_receipts_bank += rec_bank.amount
        for pay_cash in payments_cash:
            total_payments_cash += pay_cash.amount
        for pay_bank in payments_bank:
            total_payments_bank += pay_bank.amount

        return {
            'user_id': self.user_id.name,

            'date': self.date,
            'total_cash': total_cash,
            'total_no_cash': total_no_cash,
            'total_out_refund': total_out_refund,
            'total_receipts_cash': total_receipts_cash,
            'total_receipts_bank': total_receipts_bank,
            'total_payments_cash': total_payments_cash,
            'total_payments_bank': total_payments_bank,
            'available_cash': total_receipts_cash - total_payments_cash,
            'available_bank': total_receipts_bank - total_payments_bank,
        }
