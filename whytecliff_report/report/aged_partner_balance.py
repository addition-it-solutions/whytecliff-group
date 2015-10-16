# -*- coding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2015 Whytecliff Group
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
            'get_start_period': self.get_start_period,
            'get_end_period': self.get_end_period,
            'get_start_date': self._get_start_date,
            'get_end_date': self._get_end_date,
            'get_fiscalyear': self._get_fiscalyear,
        })
        
    def set_context(self, objects, data, ids, report_type=None):
        obj_partner = self.pool.get('res.partner')
        partner_ids = data['form'].get('partner_ids',False)
        self.partners = objects = obj_partner.browse(self.cr, SUPERUSER_ID, partner_ids)
        objects = sorted(objects, key=lambda x: (x.ref, x.name))
        return super(aged_partner_balance, self).set_context(objects, data, partner_ids, report_type)

    def lines(self, data):
        obj_partner = self.pool.get('res.partner')
        obj_fiscalyear = self.pool.get('account.fiscalyear')
        result = []
        ctx = {}
        current_date = datetime.now()
        total_months = 2
        fiscalyear = obj_fiscalyear.browse(self.cr, self.uid, data['form'].get('fiscalyear_id'))
        fiscal_date_start = fiscalyear.date_start
        date_stop = (current_date + relativedelta(months=-3) + relativedelta(day=31)).strftime('%Y-%m-%d')
        for partner in self.partners:
            res = {'name': partner.name}
            for month in range(3):
                month = month - total_months
                date_start = (current_date + relativedelta(months=month)).strftime('%Y-%m-01')
                date_end = (current_date + relativedelta(months=month) + relativedelta(day=31)).strftime('%Y-%m-%d')
                ctx['date_from'] = date_start
                ctx['date_to'] = date_end
                debit = obj_partner.browse(self.cr, self.uid, partner.id, context=ctx).debit
                credit = obj_partner.browse(self.cr, self.uid, partner.id, context=ctx).credit
                if month == 0:
                    res['current_balance'] = debit + credit
                if month == -1:
                    res['period_1'] = debit + credit
                if month == -2:
                    res['period_2'] = debit + credit
            ctx['date_from'] = fiscal_date_start
            ctx['date_to'] = date_stop
            debit = obj_partner.browse(self.cr, self.uid, partner.id, context=ctx).debit
            credit = obj_partner.browse(self.cr, self.uid, partner.id, context=ctx).credit
            res['period_3'] = debit + credit
            res['sum_net_balance'] = res['current_balance'] + res['period_1'] + res['period_2'] + res['period_3']
            result.append(res)
        return result

class report_partnerbalance(osv.AbstractModel):
    _name = 'report.whytecliff_report.report_netbalance'
    _inherit = 'report.abstract_report'
    _template = 'whytecliff_report.report_netbalance'
    _wrapped_report_class = aged_partner_balance
