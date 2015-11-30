# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-2016 Whytecliff Group Pvt Ltd.
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

from openerp.osv import osv
from openerp.report import report_sxw

class account_invoice_cliffpremiums(report_sxw.rml_parse):
    
    def __init__(self, cr, uid, name, context=None):
        super(account_invoice_cliffpremiums, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_ship_to': self.get_ship_to,
        })
    
    def get_ship_to(self, invoice):
        sale_obj = self.pool.get('sale.order')
        self.cr.execute("select order_id from sale_order_invoice_rel where invoice_id=%s"% (invoice.id))
        sale_order_ids = [x[0] for x in self.cr.fetchall()]
        address = ""
        if sale_order_ids:
            address = sale_obj.browse(self.cr, self.uid, sale_order_ids[0]).partner_shipping_id
        return address

class report_accountinvoice(osv.AbstractModel):
    _name = 'report.account.report_invoice'
    _inherit = 'report.abstract_report'
    _template = 'account.report_invoice'
    _wrapped_report_class = account_invoice_cliffpremiums

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: