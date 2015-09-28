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

class report_far_common(object):

    def _get_fiscalyear(self, data):
        if data.get('form', False) and data['form'].get('fiscalyear_id', False):
            return self.pool.get('account.fiscalyear').browse(self.cr, self.uid, data['form']['fiscalyear_id']).name
        return ''
    
    def get_start_period(self, data):
        if data.get('form', False) and data['form'].get('period_from', False):
            return self.pool.get('account.period').browse(self.cr,self.uid,data['form']['period_from']).name
        return ''

    def get_end_period(self, data):
        if data.get('form', False) and data['form'].get('period_to', False):
            return self.pool.get('account.period').browse(self.cr, self.uid, data['form']['period_to']).name
        return ''
    
    def _get_assets(self, category, data):
        asset_obj = self.pool.get('account.asset.asset')
        period_obj = self.pool.get('account.period')
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        cr = self.cr
        uid = self.uid
        res = []
        states = ['open','close']
        fiscalyear_id = period_from = period_to = False
        if data.get('form', False): 
            if data['form'].get('fiscalyear_id', False):
                fiscalyear_id = data['form']['fiscalyear_id']
            if data['form'].get('period_from', False):
                period_from = data['form']['period_from']
            if data['form'].get('period_to', False):
                period_to = data['form']['period_to']
            if data['form'].get('state',''):
                states = [data['form']['state']]
        start_date = end_date = False
        if fiscalyear_id:
            start_date = fiscalyear_obj.browse(cr, uid, fiscalyear_id).date_start
            end_date = fiscalyear_obj.browse(cr, uid, fiscalyear_id).date_stop
        if period_from and period_to:
            start_date = period_obj.browse(cr, uid, period_from).date_start
            end_date = period_obj.browse(cr, uid, period_to).date_stop
        domain = [('purchase_date','>=',start_date), ('purchase_date','<=',end_date),('category_id','=',category.id),('state','in',states)]
        asset_ids = asset_obj.search(cr, uid, domain)
        for asset in asset_obj.browse(cr, uid, asset_ids):
            res.append(asset)
        return res
    
