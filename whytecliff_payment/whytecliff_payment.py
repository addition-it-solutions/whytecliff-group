# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-2016 Whytecliff Group Pvt. Ltd.
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api, _
import openerp.addons.decimal_precision as dp

class whytecliff_payment_form(models.Model):
    _name = "payment.form"
    _description = "Payment Authorisation Form"

    @api.model
    def _default_company(self):
        return self.env['res.company']._company_default_get('payment.form')

    @api.model
    def _default_currency(self):
        company_id = self._default_company()
        currency_id = self.env['res.company'].browse(company_id).currency_id
        return currency_id and currency_id.id or 1

    name = fields.Char(string='Reference/Description', index=True, required=True)
    date = fields.Date(string="Date")
    payment_date = fields.Date(string="Payment Date")
    vendor_company_id = fields.Many2one('res.partner', string="Supplier", 
                                        domain=[('supplier','=',True)])
    project_name = fields.Char(string="Project")
    invoice_id = fields.Many2one('account.invoice',string="Invoice Number")
    purchase_id = fields.Many2one('purchase.order', string="Purchase Order Number")
    balance = fields.Boolean(string='Balance')
    deposit = fields.Boolean(string='Deposit')
    payment_code = fields.Char(string='Payment Code')
    cheque_number = fields.Char(string='Cheque Number')
    company_id = fields.Many2one('res.company', string='Company',
                                 default=_default_company)
    amount_to_pay = fields.Float(string='Amount to be Paid', digits=dp.get_precision('Account'))
    bank_id = fields.Many2one('res.bank', string='Bank Name')
    payment_term_method = fields.Selection([('cc', 'CC'), ('tt', 'TT'), ('cash', 'Cash'), ('cheque', 'Cheque')], string='Payment Method', required=True)
    third_party_form = fields.Boolean(string='3rd Party Payment Form')
    employee_approval_id = fields.Many2one('res.partner', string='Employee Approval')
    line_manager_approval_id = fields.Many2one('res.partner', string='Line Manager Approval')
    senior_manager_approval_id = fields.Many2one('res.partner', string='Senior Manager Approval')
    currency_id = fields.Many2one('res.currency', string="Currency", default=_default_currency)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
