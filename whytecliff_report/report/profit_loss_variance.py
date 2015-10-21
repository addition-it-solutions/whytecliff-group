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

from openerp.osv import osv
from openerp.report import report_sxw
from openerp.addons.account.report.common_report_header import common_report_header


class profit_loss_variance(report_sxw.rml_parse, common_report_header):
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
        return super(profit_loss_variance, self).set_context(objects, data, new_ids, report_type=report_type)

    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(profit_loss_variance, self).__init__(cr, uid, name, context=context)
        self.query = ""
        self.result_acc = []
        self.localcontext.update({
            'time': time,
            'lines': self.lines,
            'get_fiscalyear': self._get_fiscalyear,
            'get_account': self._get_account,
            'get_target_move': self._get_target_move,
            'get_period': self._get_period,
        })
        self.context = context
        
    def _get_period(self, data):
        if data.get('form', False) and data['form'].get('period_id', False):
            return self.pool.get('account.period').browse(self.cr,self.uid,data['form']['period_id']).name
        return ''
    
    def _get_balances(self, account_id):
        obj_fiscalyear = self.pool.get('account.fiscalyear')
        obj_period = self.pool.get('account.period')
        obj_account = self.pool.get('account.account')
        ctx = self.context.copy()
        period = obj_period.browse(self.cr, self.uid, ctx.get('period_id'))
        if ctx.get('fiscalyear'):
            fiscalyear = obj_fiscalyear.browse(self.cr, self.uid, ctx.get('fiscalyear'))
        else:
            fiscalyear = period.fiscalyear_id
        last_year_fiscal_from = (datetime.strptime(fiscalyear.date_start,'%Y-%m-%d') + relativedelta(years=-1)).strftime('%Y-%m-%d')
        last_year_fiscal_to = (datetime.strptime(fiscalyear.date_stop,'%Y-%m-%d') + relativedelta(years=-1)).strftime('%Y-%m-%d')
        last_year_date_from = (datetime.strptime(period.date_start,'%Y-%m-%d') + relativedelta(years=-1)).strftime('%Y-%m-%d')
        last_year_date_to = (datetime.strptime(period.date_stop,'%Y-%m-%d') + relativedelta(years=-1)).strftime('%Y-%m-%d')
        fiscal_date_start = fiscalyear.date_start

        # YTD Balance
        ctx['date_from'] = fiscal_date_start
        ctx['date_to'] = period.date_stop 
        ytd_balance = obj_account.browse(self.cr, self.uid, account_id, context=ctx)

        # Period Last
        ctx['fiscalyear'] = False
        ctx['date_from'] = last_year_date_from
        ctx['date_to'] = last_year_date_to
        period_last = obj_account.browse(self.cr, self.uid, account_id, context=ctx)

        # YTD Last
        ctx['fiscalyear'] = False
        ctx['date_from'] = last_year_fiscal_from
        ytd_last = obj_account.browse(self.cr, self.uid, account_id, context=ctx)

        #Total Last Year
        ctx['fiscalyear'] = False
        ctx['date_from'] = last_year_fiscal_from
        ctx['date_to'] = last_year_fiscal_to
        total_last = obj_account.browse(self.cr, self.uid, account_id, context=ctx)

        res = {
               'ytd_balance': ytd_balance.balance,
               'period_last': period_last.balance,
               'ytd_last': ytd_last.balance,
               'total_last': total_last.balance,
        }
        return res

    def lines(self, form, ids=None, done=None):
        def _process_child(accounts, parent, ctx={}):
                account_rec = [acct for acct in accounts if acct['id']==parent][0]
#                 currency_obj = self.pool.get('res.currency')
#                 currency = acc_id.currency_id and acc_id.currency_id or acc_id.company_id.currency_id
                vals = self._get_balances(account_rec['id'])
                if int(account_rec['code']) in range(1000,5000):
                    res = {
                        'id': account_rec['id'],
                        'type': account_rec['type'],
                        'code': account_rec['code'],
                        'name': account_rec['name'],
                        'level': account_rec['level'],
                        'period_actual': account_rec['balance'],
                        'ytd_actual': vals['ytd_balance'],
                        'period_last': vals['period_last'],
                        'ytd_last': vals['ytd_last'],
                        'total_last': vals['total_last'],
                        'period_variance': (account_rec['balance'] - vals['period_last']),
                        'parent_id': account_rec['parent_id'],
                        'bal_type': '',
                    }
                    self.result_acc.append(res)
                if account_rec['child_id']:
                    for child in account_rec['child_id']:
                        _process_child(accounts,child,ctx)

        obj_account = self.pool.get('account.account')
        if not ids:
            ids = self.ids
        if not ids:
            return []
        if not done:
            done={}

        ctx = self.context.copy()

        ctx['fiscalyear'] = form['fiscalyear_id']
        ctx['period_from'] = form['period_id']
        ctx['period_to'] = form['period_id']
        ctx['state'] = form['target_move']
        parents = ids
        child_ids = obj_account._get_children_and_consol(self.cr, self.uid, ids, ctx)
        if child_ids:
            ids = child_ids
        accounts = obj_account.read(self.cr, self.uid, ids, ['type','code','name','parent_id','level','child_id','balance'], ctx)

        for parent in parents:
                if parent in done:
                    continue
                done[parent] = 1
                _process_child(accounts,parent,ctx)
        return self.result_acc

class report_profitlossvariance(osv.AbstractModel):
    _name = 'report.whytecliff_report.report_profitlossvariance'
    _inherit = 'report.abstract_report'
    _template = 'whytecliff_report.report_profitlossvariance'
    _wrapped_report_class = profit_loss_variance
