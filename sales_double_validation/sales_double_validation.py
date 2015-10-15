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
           ('approval1','Waiting for Approval'),
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
    def action_button_confirm_sale(self):
        self.signal_workflow('order_approval1')
        self.write({'state':'approval1'})
        return True
    
    @api.multi
    def action_button_confirm(self):
        res = super(playerlayer_sale_order,self).action_button_confirm()
        return res
    
    @api.cr_uid_ids_context
    def action_ship_create(self, cr, uid, ids, context=None):
        """Create the required procurements to supply sales order lines, also connecting
        the procurements to appropriate stock moves in order to bring the goods to the
        sales order's requested location.

        :return: True
        """
        context = dict(context or {})
        context['lang'] = self.pool['res.users'].browse(cr, uid, uid).lang
        procurement_obj = self.pool.get('procurement.order')
        sale_line_obj = self.pool.get('sale.order.line')
        for order in self.browse(cr, uid, ids, context=context):
            proc_ids = []
            vals = self._prepare_procurement_group(cr, uid, order, context=context)
            if not order.procurement_group_id:
                group_id = self.pool.get('procurement.group').create(cr, uid, vals, context=context)
                order.write({'procurement_group_id': group_id})

            for line in order.order_line:
                if line.state == 'cancel':
                    continue
                #Try to fix exception procurement (possible when after a shipping exception the user choose to recreate)
                if line.procurement_ids:
                    #first check them to see if they are in exception or not (one of the related moves is cancelled)
                    procurement_obj.check(cr, uid, [x.id for x in line.procurement_ids if x.state not in ['cancel', 'done']])
                    line.refresh()
                    #run again procurement that are in exception in order to trigger another move
                    except_proc_ids = [x.id for x in line.procurement_ids if x.state in ('exception', 'cancel')]
                    procurement_obj.reset_to_confirmed(cr, uid, except_proc_ids, context=context)
                    proc_ids += except_proc_ids
                elif sale_line_obj.need_procurement(cr, uid, [line.id], context=context):
                    
                    if (line.state == 'done') or not line.product_id:
                        continue
                    vals = self._prepare_order_line_procurement(cr, uid, order, line, group_id=order.procurement_group_id.id, context=context)
                    ctx = context.copy()
                    ctx['procurement_autorun_defer'] = True
                    proc_id = procurement_obj.create(cr,uid, vals, context=ctx)
                    proc_ids.append(proc_id)
            #Confirm procurement order such that rules will be applied on it
            #note that the workflow normally ensure proc_ids isn't an empty list
            #procurement_obj.run(cr, uid, proc_ids, context=context)

            #if shipping was in exception and the user choose to recreate the delivery order, write the new status of SO
            if order.state == 'shipping_except':
                val = {'state': 'progress', 'shipped': False}

                if (order.order_policy == 'manual'):
                    for line in order.order_line:
                        if (not line.invoiced) and (line.state not in ('cancel', 'draft')):
                            val['state'] = 'manual'
                            break
                order.write(val)
        
        #self.write(cr, uid, ids, {'state':'manual'}, context=context)
        return True
    
