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
############## Done By: Addition IT Solutions Pvt. Ltd. ######################

import time
from datetime import datetime

from openerp.osv import osv
from openerp.report import report_sxw
from openerp.addons.account.report.common_report_header import common_report_header


class account_statement(report_sxw.rml_parse, common_report_header):
    _name = 'report.account.statement'

    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(account_statement, self).__init__(cr, uid, name, context=context)
        self.query = ""
        self.result_acc = []
        self.localcontext.update({
            'time': time,
            'lines': self.lines,
            'get_fiscalyear': self._get_fiscalyear,
            'get_account': self._get_account,
            'get_target_move': self._get_target_move,
            'get_partner': self._get_partner,
            'get_currency': self._get_currency,
            'get_total_balance': self._get_total_balance,
        })
        self.context = context
    
    def _get_partner(self, data):
        if data.get('form', False) and data['form'].get('partner_id', False):
            return self.pool.get('res.partner').browse(self.cr,self.uid,data['form']['partner_id'])
        return ''
    
    def _get_currency(self, data):
        if data.get('form', False) and data['form'].get('currency_id', False):
            return self.pool.get('res.currency').browse(self.cr,self.uid,data['form']['currency_id']).name
        return ''
    
    def _get_total_balance(self, data):
        currency = self._get_currency(data)
        current_date = datetime.today()
        start_date = (current_date.replace(day=1)).strftime('%Y-%m-%d')
        partner = self._get_partner(data)
        self.cr.execute("""
            select sum(inv.residual)
            from account_invoice inv
            left join res_currency cur on cur.id=inv.currency_id
            where inv.residual > 0.0
            and cur.name = '%s'
            and inv.type = 'out_invoice'
            and inv.partner_id = %s
        """ %(currency, partner.id))
        result = self.cr.dictfetchall()[0]
        return result.get('sum',0.0)
    
    def lines(self, data):
        currency = self._get_currency(data)
        current_date = datetime.today()
        start_date = (current_date.replace(day=1)).strftime('%Y-%m-%d')
        partner = self._get_partner(data)
        self.cr.execute("""
            select inv.name, inv.number, inv.internal_number, inv.date_invoice, inv.date_due, inv.amount_total, inv.amount_untaxed, inv.residual
            from account_invoice inv
            left join res_currency cur on cur.id=inv.currency_id
            where inv.residual > 0.0
            and cur.name = '%s'
            and inv.type = 'out_invoice'
            and inv.partner_id = %s
            order by inv.id
        """ %(currency, partner.id))
        result = self.cr.dictfetchall()
        return result

class report_account_statement(osv.AbstractModel):
    _name = 'report.whytecliff_report.report_accountstatement'
    _inherit = 'report.abstract_report'
    _template = 'whytecliff_report.report_accountstatement'
    _wrapped_report_class = account_statement


