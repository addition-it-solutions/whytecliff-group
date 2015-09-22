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
from openerp.osv import fields, osv

class profit_loss_report(osv.osv_memory):
    _name = "profit.loss.report"
    _inherit = "account.common.report"
    _description = "P&L Report"

    _columns = {
        'account_report_id': fields.many2one('account.financial.report', 'Account Reports', required=True),
    }
    
    def _get_account_report(self, cr, uid, context=None):
        # TODO deprecate this it doesnt work in web
        menu_obj = self.pool.get('ir.ui.menu')
        report_obj = self.pool.get('account.financial.report')
        report_ids = []
        if context.get('active_id'):
            menu = menu_obj.browse(cr, uid, context.get('active_id')).name
            report_ids = report_obj.search(cr, uid, [('name','ilike',menu)])
        return report_ids and report_ids[0] or False

    _defaults = {
            'account_report_id': _get_account_report,
            'filter': 'filter_period',
    }
    
    def check_report(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = super(profit_loss_report, self).check_report(cr, uid, ids, context=context)
        data = {}
        data['form'] = self.read(cr, uid, ids, ['account_report_id','journal_ids', 'chart_account_id', 'target_move'], context=context)[0]
        for field in ['chart_account_id', 'account_report_id']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        return res

    def _print_report(self, cr, uid, ids, data, context=None):
        data['form'].update(self.read(cr, uid, ids, ['account_report_id', 'target_move'], context=context)[0])
        if not context:
            context = {}
        context['landscape'] = True
        return self.pool['report'].get_action(cr, uid, [], 'whytecliff_report.report_profitloss', data=data, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
