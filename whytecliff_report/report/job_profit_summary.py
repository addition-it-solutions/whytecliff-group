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
import time

from openerp.report import report_sxw
from openerp.tools.translate import _
from openerp.osv import osv

from openerp.addons.account.report.common_report_header import common_report_header

class report_job_profit(report_sxw.rml_parse, common_report_header):
    def __init__(self, cr, uid, name, context=None):
        super(report_job_profit, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
                'time': time,
        })
        self.context = context
    
    def set_context(self, objects, data, ids, report_type=None):
        new_ids = self.pool.get('account.invoice').search(self.cr, self.uid, [('parent_id', '=', False)])
        ctx = self.context.copy()
        ctx['fiscalyear'] = data['form']['fiscalyear_id']
        if data['form']['filter'] == 'filter_period':
            ctx['period_from'] = data['form']['period_from']
            ctx['period_to'] = data['form']['period_to']
        self.context.update(ctx)
        self.context['landscape'] = True
        if (data['model'] == 'ir.ui.menu'):
            objects = self.pool.get('account.invoice').browse(self.cr, self.uid, new_ids)
        return super(report_job_profit, self).set_context(objects, data, new_ids, report_type=report_type)

class report_jobprofit(osv.AbstractModel):
    _name = 'report.whytecliff_report.report_jobprofit'
    _inherit = 'report.abstract_report'
    _template = 'whytecliff_report.report_jobprofit'
    _wrapped_report_class = report_job_profit
