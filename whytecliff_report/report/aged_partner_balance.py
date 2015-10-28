# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015-2016 Whytecliff Group Pvt. Ltd.
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
#
##############################################################################
############## Done By: Addition IT Solutions Pvt. Ltd. ######################

import time
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import osv
from openerp.report import report_sxw
from openerp.addons.account.report.common_report_header import common_report_header
from openerp import SUPERUSER_ID

class aged_partner_balance(report_sxw.rml_parse, common_report_header):

    def __init__(self, cr, uid, name, context=None):
        super(aged_partner_balance, self).__init__(cr, uid, name, context=context)
        self.init_bal_sum = 0.0
        self.amount_currency = {}
        self.localcontext.update({
            'time': time,
            'lines': self.lines,
            'get_account': self._get_account,
            'get_start_period': self.get_start_period,
            'get_end_period': self.get_end_period,
            'get_start_date': self._get_start_date,
            'get_end_date': self._get_end_date,
            'get_fiscalyear': self._get_fiscalyear,
            'get_org_type': self._get_org_type,
            'get_total_balance': self._get_total_balance,
        })
        
    def set_context(self, objects, data, ids, report_type=None):
        obj_partner = self.pool.get('res.partner')
        partner_ids = data['form'].get('partner_ids',False)
        self.partners = objects = obj_partner.browse(self.cr, SUPERUSER_ID, partner_ids)
        objects = sorted(objects, key=lambda x: (x.ref, x.name))
        return super(aged_partner_balance, self).set_context(objects, data, partner_ids, report_type)

    def _get_org_type(self):
        return ['receivable','payable']
    
    def _get_total_balance(self, data, org_type):
        sum_net_balance = total_current = total_period_1 = total_period_2 = total_period_3 = 0.0
        for data in self.lines(data, org_type):
            sum_net_balance += data['sum_net_balance']
            total_current += data['current_balance']
            total_period_1 += data['period_1']
            total_period_2 += data['period_2']
            total_period_3 += data['period_3']
        result = [sum_net_balance,total_current,total_period_1,total_period_2,total_period_3]
        return result

    def lines(self, data, org_type):
        obj_partner = self.pool.get('res.partner')
        obj_fiscalyear = self.pool.get('account.fiscalyear')
        obj_period = self.pool.get('account.period')
        result = []
        ctx = {}
        current_date = datetime.now()
        total_months = 2
        fiscalyear = obj_fiscalyear.browse(self.cr, self.uid, data['form'].get('fiscalyear_id'))
        fiscal_date_start = fiscalyear.date_start
        date_stop = (current_date + relativedelta(months=-3) + relativedelta(day=31)).strftime('%Y-%m-%d')
        for partner in self.partners:
            res = {
                   'name': partner.name,
                   'current_balance': 0.0,
                   'period_1': 0.0,
                   'period_2': 0.0,
                   'period_3': 0.0
            }
            for month in range(3):
                month = month - total_months
                date_start = (current_date + relativedelta(months=month)).strftime('%Y-%m-01')
                date_end = (current_date + relativedelta(months=month) + relativedelta(day=31)).strftime('%Y-%m-%d')
                period_ids = obj_period.search(self.cr, self.uid, [('date_start','=',date_start),('date_stop','=',date_end)])
                if not period_ids:
                    continue
                ctx['date_from'] = date_start
                ctx['date_to'] = date_end
                amount = 0.0
                if (partner.supplier and (partner.supplier or partner.customer)) and org_type == 'payable':
                    amount = (obj_partner.browse(self.cr, self.uid, partner.id, context=ctx).debit) * -1 or 0.0
                if (partner.customer and (partner.customer or partner.supplier)) and org_type == 'receivable':
                    amount = obj_partner.browse(self.cr, self.uid, partner.id, context=ctx).credit
                if month == 0:
                    res['current_balance'] = amount
                if month == -1:
                    res['period_1'] = amount
                if month == -2:
                    res['period_2'] = amount
            ctx['date_from'] = fiscal_date_start
            ctx['date_to'] = date_stop
            amount = 0.0
            if (partner.supplier and (partner.supplier or partner.customer)) and org_type == 'payable':
                amount = (obj_partner.browse(self.cr, self.uid, partner.id, context=ctx).debit) * -1 or 0.0
            if (partner.customer and (partner.customer or partner.supplier)) and org_type == 'receivable':
                amount = obj_partner.browse(self.cr, self.uid, partner.id, context=ctx).credit
            res['period_3'] = amount
            res['sum_net_balance'] = res['current_balance'] + res['period_1'] + res['period_2'] + res['period_3']
            if res['sum_net_balance'] != 0.0:
                result.append(res)
        return result

class report_partnerbalance(osv.AbstractModel):
    _name = 'report.whytecliff_report.report_netbalance'
    _inherit = 'report.abstract_report'
    _template = 'whytecliff_report.report_netbalance'
    _wrapped_report_class = aged_partner_balance
