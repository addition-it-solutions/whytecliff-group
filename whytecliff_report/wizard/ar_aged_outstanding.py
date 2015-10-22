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

class ar_aged_outstanding_report(osv.osv_memory):
    _name = "ar.aged.outstanding.report"
    _inherit = "profit.loss.variance.report"
    _description = "AR Aged Outstanding"
    
    def _print_report(self, cr, uid, ids, data, context=None):
        super(ar_aged_outstanding_report, self)._print_report(cr, uid, ids, data, context=context)
#         context['landscape'] = True
        return self.pool['report'].get_action(cr, uid, [], 'whytecliff_report.report_aragedoutstanding', data=data, context=context)
