# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-2016 Addition IT Solutions Pvt. Ltd. (<http://www.aitspl.com>).
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

class report_standing_data(report_sxw.rml_parse):
    _name = 'report.standing.data'
    
    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(report_standing_data, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_asset_categories': self._get_asset_categories,
        })
        self.context = context

    def _get_asset_categories(self):
        asset_categ_obj = self.pool.get('account.asset.category')
        categories = []
        new_ids = asset_categ_obj.search(self.cr, self.uid, [])
        fields = ['name', 'method', 'method_time', 'method_number', 'method_period', 'prorata']
        for category in asset_categ_obj.read(self.cr, self.uid, new_ids, fields):
            if category['method_time'] == 'number':
                category.update({'method_time': 'Number of Depreciations'})
            elif category['method_time'] == 'end':
                category.update({'method_time': 'Ending Date'})
                
            if category['method'] == 'linear':
                category.update({'method': 'Linear'})
            elif category['method'] == 'degressive':
                category.update({'method': 'Degressive'})
            
            categories.append(category)
        return categories

class report_standingdata(osv.AbstractModel):
    _name = 'report.addsol_cnx_asset.report_standingdata'
    _inherit = 'report.abstract_report'
    _template = 'addsol_cnx_asset.report_standingdata'
    _wrapped_report_class = report_standing_data

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: