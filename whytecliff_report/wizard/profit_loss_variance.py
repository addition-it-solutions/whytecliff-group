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
from openerp.osv import fields, osv

class profit_loss_variance_report(osv.osv_memory):
    _name = "profit.loss.variance.report"
    _inherit = "account.common.report"
    _description = "Profit & Loss Variance"
    
    _columns = {
            'period_id': fields.many2one('account.period','Select a Period', required=True)
    }
    def _build_contexts(self, cr, uid, ids, data, context=None):
        result = super(profit_loss_variance_report, self)._build_contexts(cr, uid, ids, data=data, context=context)
        result['period_id'] = 'period_id' in data['form'] and data['form']['period_id'] or False
        return result

    def _print_report(self, cr, uid, ids, data, context=None):
        data['form'].update(self.read(cr, uid, ids, ['period_id'], context=context)[0])
        if isinstance(data['form']['period_id'], tuple):
            data['form']['period_id'] = data['form']['period_id'][0]
        if not context:
            context = {}
#         context['landscape'] = True
        return self.pool['report'].get_action(cr, uid, [], 'whytecliff_report.report_profitlossvariance', data=data, context=context)
