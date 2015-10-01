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

from openerp import models, fields, api, _

class playerlayer_sale_order(models.Model):
    _inherit = "sale.order"
    
    state = fields.Selection([
           ('draft', 'Draft Quotation'),
           ('sent', 'Quotation Sent'),
           ('approval1','Approval By School'),
           ('approval2','Approval By Sales Manager'),
           ('cancel', 'Cancelled'),
           ('waiting_date', 'Waiting Schedule'),
           ('progress', 'Sales Order'),
           ('manual', 'Sale to Invoice'),
           ('shipping_except', 'Shipping Exception'),
           ('invoice_except', 'Invoice Exception'),
           ('done', 'Done'),
           ], 'Status', readonly=True, copy=False, help="Gives the status of the quotation or sales order.\
             \nThe exception status is automatically set when a cancel operation occurs \
             in the invoice validation (Invoice Exception) or in the picking list process (Shipping Exception).\nThe 'Waiting Schedule' status is set when the invoice is confirmed\
              but waiting for the scheduler to run on the order date.", select=True)
              
    @api.multi
    def action_button_confirm(self):
        self.signal_workflow('order_approval2')
        res = super(playerlayer_sale_order,self).action_button_confirm()
        return res

    @api.multi
    def action_button_confirm_school(self):
        return self.write({'state':'approval2'})
    
    @api.multi
    def action_button_confirm_sale(self):
        self.write({'state':'approval1'})
        return True
