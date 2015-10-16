# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-2016 Whytecliff Group.
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

class whytec_account_partner_balance(osv.osv_memory):
    _inherit = 'account.common.report'
    _name = 'whytec.partner.balance'
    _description = 'Aged Partner Balance'
    
    _columns = {
        'partner_ids': fields.many2many('res.partner', string="Partner"),
    }
    
    def _build_contexts(self, cr, uid, ids, data, context=None):
        result = super(whytec_account_partner_balance, self)._build_contexts(cr, uid, ids, data=data, context=context)
        result['partner_ids'] = 'partner_ids' in data['form'] and data['form']['partner_ids'] or False
        return result
    
    def _print_report(self, cr, uid, ids, data, context=None):
        if context is None:
            context = {}
#         data = self.pre_print_report(cr, uid, ids, data, context=context)
        data['form'].update(self.read(cr, uid, ids, ['partner_ids'])[0])
        return self.pool['report'].get_action(cr, uid, [], 'whytecliff_report.report_netbalance', data=data, context=context)
    
#     def pre_print_report(self, cr, uid, ids, data, context=None):
#         if context is None:
#             context = {}
#         data['form'].update(self.read(cr, uid, ids, ['partner_ids'], context=context)[0])
#         return super(whytec_account_partner_balance, self).pre_print_report(cr, uid, ids, data=data, context=context)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: