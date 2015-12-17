# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

from datetime import datetime
from dateutil.relativedelta import relativedelta
from openerp.osv import fields, osv
from openerp.tools.translate import _

class whytec_account_aged_trial_balance(osv.osv_memory):
    _inherit = 'account.aged.trial.balance'

    _columns = {
        'period_id': fields.many2one('account.period','Select a Period'),
    }
    
    def _print_report(self, cr, uid, ids, data, context=None):
        period_obj = self.pool.get('account.period')
        data = self.pre_print_report(cr, uid, ids, data, context=context)
        data['form'].update(self.read(cr, uid, ids, ['period_length', 'direction_selection', 'period_id'])[0])
        period_length = 30
        res = {}
        stop = ''
        if data['form']['filter'] == 'filter_no':
            if not data['form']['period_id']:
                raise osv.except_osv(_('User Error!'), _('You must select a period.'))
            data['form'].update(self.read(cr, uid, ids, ['period_id'])[0])
            period_id = data['form']['period_id'][0]
            period = period_obj.browse(cr, uid, period_id, context=context)
            start = datetime.strptime(period.date_stop, "%Y-%m-%d")
            data['form']['date_from'] = period.date_stop
        elif data['form']['filter'] == 'filter_period':
            period_from = period_obj.browse(cr, uid, data['form']['period_from'], context=context)
            period_to = period_obj.browse(cr, uid, data['form']['period_to'], context=context)
            start = datetime.strptime(period_from.date_start, "%Y-%m-%d")
            stop = datetime.strptime(period_to.date_stop, "%Y-%m-%d")
            data['form']['date_from'] = period_to.date_stop
        elif data['form']['filter'] == 'filter_date':
            start = datetime.strptime(data['form']['date_from'], "%Y-%m-%d")
            stop = datetime.strptime(data['form']['date_to'], "%Y-%m-%d")
            data['form']['date_from'] = str(data['form']['date_to'])

        if data['form']['direction_selection'] == 'past':
            for i in range(5)[::-1]:
                if not stop:
                    stop = start - relativedelta(days=period_length)
                else:
                    stop = stop - relativedelta(days=period_length)
                res[str(i)] = {
                    'name': (i!=0 and (str((5-(i+1)) * period_length) + '-' + str((5-i) * period_length)) or ('+'+str(4 * period_length))),
                    'stop': start.strftime('%Y-%m-%d'),
                    'start': (i!=0 and stop.strftime('%Y-%m-%d') or False),
                }
                start = stop - relativedelta(days=1)
        else:
            for i in range(5):
                if not stop:
                    stop = start + relativedelta(days=period_length)
                else:
                    stop = stop + relativedelta(days=period_length)
                res[str(5-(i+1))] = {
                    'name': (i!=4 and str((i) * period_length)+'-' + str((i+1) * period_length) or ('+'+str(4 * period_length))),
                    'start': start.strftime('%Y-%m-%d'),
                    'stop': (i!=4 and stop.strftime('%Y-%m-%d') or False),
                }
                start = stop + relativedelta(days=1)
        data['form'].update(res)
        context['landscape'] = True
        return self.pool['report'].get_action(cr, uid, [], 'account.report_agedpartnerbalance', data=data, context=context)
    