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

class account_statement_report(osv.osv_memory):
    _name = "account.statement.report"
    _inherit = "account.common.report"
    _description = "Account Statement"
    
    _columns = {
        'partner_id': fields.many2one('res.partner', 'Select Account For', required=True),
        'currency_id': fields.many2one('res.currency', 'Currency', required=True),
    }

    def _print_report(self, cr, uid, ids, data, context=None):
        if not context:
            context = {}
        data['form'].update(self.read(cr, uid, ids, ['partner_id','currency_id'], context=context)[0])
        for field in ['partner_id', 'currency_id', 'period_from', 'period_to']:
            if isinstance(data['form'][field], tuple):
                data['form'][field] = data['form'][field][0]
        return self.pool['report'].get_action(cr, uid, [], 'whytecliff_report.report_accountstatement', data=data, context=context)
        
