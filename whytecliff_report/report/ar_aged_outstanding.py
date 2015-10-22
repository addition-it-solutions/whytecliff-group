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
from dateutil.relativedelta import relativedelta
from dateutil import rrule

from openerp.osv import osv
from openerp.report import report_sxw
from openerp.addons.account.report.common_report_header import common_report_header


class ar_aged_outstanding(report_sxw.rml_parse, common_report_header):
    _name = 'report.profit.loss.variance'

    def set_context(self, objects, data, ids, report_type=None):
        new_ids = ids
        obj_move = self.pool.get('account.move.line')
        self.query = obj_move._query_get(self.cr, self.uid, obj='l', context=data['form'].get('used_context',{}))
        ctx2 = data['form'].get('used_context',{}).copy()
        self.init_query = obj_move._query_get(self.cr, self.uid, obj='l', context=ctx2)
        self.target_move = data['form'].get('target_move', 'all')
        ctx = self.context.copy()
        ctx['fiscalyear'] = data['form']['fiscalyear_id']
        ctx['period_id'] = data['form']['period_id']
        ctx['state'] = data['form']['target_move']
        self.context.update(ctx)
        if (data['model'] == 'ir.ui.menu'):
            new_ids = [data['form']['chart_account_id']]
            objects = self.pool.get('account.account').browse(self.cr, self.uid, new_ids)
        return super(ar_aged_outstanding, self).set_context(objects, data, new_ids, report_type=report_type)

    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(ar_aged_outstanding, self).__init__(cr, uid, name, context=context)
        self.query = ""
        self.result_acc = []
        self.localcontext.update({
            'time': time,
            'lines': self.lines,
            'get_fiscalyear': self._get_fiscalyear,
            'get_account': self._get_account,
            'get_target_move': self._get_target_move,
            'get_period': self._get_period,
            'get_currency': self._get_currency,
        })
        self.context = context
    
    def _get_period(self, data):
        if data.get('form', False) and data['form'].get('period_id', False):
            return self.pool.get('account.period').browse(self.cr,self.uid,data['form']['period_id']).name
        return ''
    
    def _get_currency(self):
        currency_obj = self.pool.get('res.currency')
        currency = []
        for curr_id in currency_obj.search(self.cr, self.uid, []):
            currency.append(currency_obj.browse(self.cr, self.uid, curr_id))
        return currency
    
    def lines(self, data, currency):
#         obj_fiscalyear = self.pool.get('account.fiscalyear')
        current_date = datetime.now()
#         total_months = 2
#         fiscalyear = obj_fiscalyear.browse(self.cr, self.uid, data['form'].get('fiscalyear_id'))
#         fiscal_date_start = fiscalyear.date_start
        date_stop = (current_date + relativedelta(months=-3)).strftime('%Y-%m-01')
        self.cr.execute("""
            select  
                curr.name as currency,
                part.name as name,
                sum(inv.residual) as residual
            from account_invoice inv
                left join res_currency curr on curr.id=inv.currency_id
                left join res_partner part on part.id=inv.partner_id
            where inv.residual <> 0.0 and
                  inv.date_invoice <= '%s' and
                  inv.date_invoice >= '%s' and
                  curr.name = '%s'
            group by part.name, curr.name
            order by curr.name
        """% (current_date.strftime('%Y-%m-%d'),date_stop,currency))
        query_res = self.cr.dictfetchall()
        current_date = current_date.replace(day=1)
        end_date = current_date + relativedelta(months=-3) + relativedelta(day=31)
        end_date_until = current_date + relativedelta(day=31)
        starting_dates = rrule.rrule(rrule.MONTHLY, dtstart=(current_date + relativedelta(months=-3)), until=current_date)
        ending_dates = list(rrule.rrule(rrule.MONTHLY, dtstart=end_date, until=end_date_until,bymonthday=(31, -1),bysetpos=1))
        res = []
        for dates in starting_dates:
            for edates in ending_dates:
                if dates.month == edates.month:
                    res.append((dates.strftime('%Y-%m-%d'),edates.strftime('%Y-%m-%d')))
        return query_res

class report_ar_agedoutstanding(osv.AbstractModel):
    _name = 'report.whytecliff_report.report_aragedoutstanding'
    _inherit = 'report.abstract_report'
    _template = 'whytecliff_report.report_aragedoutstanding'
    _wrapped_report_class = ar_aged_outstanding
