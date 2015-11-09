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

class job_profit_report(osv.osv_memory):
    _name = "job.profit.report"
    _inherit = "account.common.report"
    _description = "Job Profit Summary Report"
    
    _defaults = {
            'filter': 'filter_period',
    }
    
    def _print_report(self, cr, uid, ids, data, context=None):
        data['form'].update(self.read(cr, uid, ids, ['target_move'], context=context)[0])
        if not context:
            context = {}
        context['landscape'] = True
        return self.pool['report'].get_action(cr, uid, [], 'whytecliff_report.report_jobprofit', data=data, context=context)
    
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: