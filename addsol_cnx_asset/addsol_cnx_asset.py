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
from datetime import datetime
from dateutil.relativedelta import relativedelta
from dateutil import rrule, parser

from openerp.osv import osv, fields
from openerp.tools.translate import _

class addsol_account_asset(osv.osv):
    _inherit = 'account.asset.asset'
    
    _columns = {
        'serial_number': fields.char('Serial Number'),
        'manufacturer': fields.char('Assets Manufacturer'),
        'location': fields.char('Assets Location'),
    }
    
    def compute_depreciation_board(self, cr, uid, ids, context=None):
        depreciation_lin_obj = self.pool.get('account.asset.depreciation.line')
        for asset in self.browse(cr, uid, ids, context=context):
            if asset.value_residual == 0.0:
                continue
            flag = asset.method_period/12 and True or False
            posted_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_check', '=', True)],order='depreciation_date desc')
            old_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_id', '=', False)])
            if old_depreciation_line_ids:
                depreciation_lin_obj.unlink(cr, uid, old_depreciation_line_ids, context=context)
 
            amount_to_depr = residual_amount = asset.value_residual
            if asset.prorata:
                depreciation_date = datetime.strptime(self._get_last_depreciation_date(cr, uid, [asset.id], context)[asset.id], '%Y-%m-%d')
            else:
                purchase_date = datetime.strptime(asset.purchase_date, '%Y-%m-%d')
                depn_start_date = datetime(purchase_date.year, purchase_date.month, purchase_date.day)
                #if we already have some previous validated entries, starting date isn't 1st January but last entry + method period
                if (len(posted_depreciation_line_ids)>0):
                    last_depreciation_date = datetime.strptime(depreciation_lin_obj.browse(cr,uid,posted_depreciation_line_ids[0],context=context).depreciation_date, '%Y-%m-%d')
                    depreciation_date = (last_depreciation_date+relativedelta(months=+asset.method_period))
                else:
                    # depreciation_date = start date of fiscal year or 1st January of purchase year
                    fiscal_date = self.pool.get('account.fiscalyear').search_read(cr, uid, [('date_start', '<=', purchase_date), ('date_stop', '>=', purchase_date)], ['date_start'], context=context)
                    if fiscal_date:
                        fis_date = datetime.strptime(fiscal_date[0]['date_start'], '%Y-%m-%d') 
                        depreciation_date = datetime(fis_date.year, fis_date.month, fis_date.day)
                        if not flag:
                            depreciation_date = depn_start_date
                    else:
                        raise osv.except_osv(_('Error!'),('No fiscal year defined for %s' %purchase_date.strftime('%Y-%m-%d')))
            day = depreciation_date.day
            month = depreciation_date.month
            year = depreciation_date.year
            total_days = (year % 4) and 365 or 366
 
            undone_dotation_number = self._compute_board_undone_dotation_nb(cr, uid, asset, depreciation_date, total_days, context=context)
            if not asset.prorata and depn_start_date.strftime('%Y-%m-%d') > fis_date.strftime('%Y-%m-%d') and flag:
                diff_month = (12 * depn_start_date.year + depn_start_date.month) - (12 * fis_date.year + fis_date.month)
            for x in range(len(posted_depreciation_line_ids), undone_dotation_number):
                new_vals = {}
                i = x + 1
                amount = self._compute_board_amount(cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=context)
                residual_amount -= amount
                vals = {
                     'amount': amount,
                     'asset_id': asset.id,
                     'sequence': i,
                     'name': str(asset.id) +'/' + str(i),
                     'remaining_value': residual_amount,
                     'depreciated_value': (asset.purchase_value - asset.salvage_value) - (residual_amount + amount),
                     'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),
                }
                if not asset.prorata and depn_start_date.strftime('%Y-%m-%d') > fis_date.strftime('%Y-%m-%d') and flag:
                    if i == 1:
                        new_amount = ((asset.method_period - diff_month) * amount)/asset.method_period
                        new_dep_value = (asset.purchase_value - asset.salvage_value) - (residual_amount + new_amount)
                        residual_amount = residual_amount + new_dep_value
                        vals.update({'amount': new_amount, 'depreciation_date': depn_start_date.strftime('%Y-%m-%d'),
                                     'remaining_value': residual_amount})
                    if undone_dotation_number > 1 and i == undone_dotation_number:
                        amount = amount_to_depr / (undone_dotation_number - len(posted_depreciation_line_ids))
                        new_residual_amount = amount - new_amount
                        dep_value = (asset.purchase_value - asset.salvage_value) - (new_residual_amount + amount)
                        vals.update({'remaining_value': new_residual_amount, 'depreciated_value': dep_value, 'amount': amount})
                        depn_end_date = depreciation_date + relativedelta(months=+asset.method_period)
                        new_vals.update({
                                    'amount': amount - new_amount,
                                     'asset_id': asset.id,
                                     'sequence': i + 1,
                                     'name': str(asset.id) +'/' + str(i + 1),
                                     'remaining_value': residual_amount,
                                     'depreciated_value': dep_value + amount,
                                     'depreciation_date': depn_end_date.strftime('%Y-%m-%d'),
                        })
                    if undone_dotation_number == 1:
                        dep_value = (asset.purchase_value - asset.salvage_value) - (residual_amount)
                        depn_end_date = depreciation_date + relativedelta(months=+asset.method_period)
                        new_vals.update({
                                    'amount': amount - new_amount,
                                     'asset_id': asset.id,
                                     'sequence': i + 1,
                                     'name': str(asset.id) +'/' + str(i + 1),
                                     'remaining_value': 0.0,
                                     'depreciated_value': dep_value,
                                     'depreciation_date': depn_end_date.strftime('%Y-%m-%d'),
                        })
                depreciation_lin_obj.create(cr, uid, vals, context=context)
                if new_vals:
                    depreciation_lin_obj.create(cr, uid, new_vals, context=context)
                # Considering Depr. Period as months
                depreciation_date = (datetime(year, month, day) + relativedelta(months=+asset.method_period))
                day = depreciation_date.day
                month = depreciation_date.month
                year = depreciation_date.year
 
        return True
    
    def automatic_journal_entries(self, cr, uid, context=None):
        fisyr_obj = self.pool.get('account.fiscalyear')
        depn_line_obj = self.pool.get('account.asset.depreciation.line')
        move_obj = self.pool.get('account.move')
        current_date = time.strftime('%Y-%m-%d')
        asset_ids = self.search(cr, uid, [('state','=','open'), ('purchase_date','<=',current_date)], context=context)
        for asset in self.browse(cr, uid, asset_ids, context=context):
            flag = asset.method_period == 1 and True or False
            depn_start_date = False
            for depn in asset.depreciation_line_ids:
                if depn.move_check:
                    continue
                if depn.depreciation_date <= current_date:
                    if flag:
                        move_ids = depn_line_obj.create_move(cr, uid, [depn.id], context=context)
                        move_obj.write(cr, uid, move_ids, {'ref': asset.category_id.name}, context=context)
                    else:
                        fiscal_date = fisyr_obj.search_read(cr, uid, [('date_start', '<=', depn.depreciation_date), 
                                                                      ('date_stop', '>=', depn.depreciation_date)], 
                                                            ['date_start', 'date_stop'], context=context)
                        if fiscal_date:
                            date_start = datetime.strptime(fiscal_date[0]['date_start'], '%Y-%m-%d')
                            date_stop = datetime.strptime(fiscal_date[0]['date_stop'], '%Y-%m-%d')
                            if depn.sequence == 1 and depn.depreciation_date > date_start.strftime('%Y-%m-%d'):
                                depn_start_date = datetime.strptime(depn.depreciation_date, '%Y-%m-%d')
                                diff_month = (12 * depn_start_date.year + depn_start_date.month) - (12 * date_start.year + date_start.month)
                                date_start = depn_start_date
                            date_range = list(rrule.rrule(rrule.MONTHLY, dtstart=date_start, 
                                                                until=date_stop))
                            if depn_start_date and depn.sequence == len(asset.depreciation_line_ids):
                                date_stop = date_start + relativedelta(months=+diff_month)
                                date_range = list(rrule.rrule(rrule.MONTHLY, dtstart=date_start, 
                                                                until=date_stop))
                            monthly_amount = depn.amount / len(date_range)
                            for date in date_range:
                                    if date.strftime('%Y-%m-%d') <= current_date:
                                        move_id = self.create_account_moves(cr, uid, asset, date, monthly_amount, context)
                                        if date.strftime('%Y-%m') == date_stop.strftime('%Y-%m'):
                                            depn_line_obj.write(cr, uid, depn.id, {'move_id': move_id}, context=context)
                    
    def create_account_moves(self, cr, uid, asset, date, amount, context=None):
        period_obj = self.pool.get('account.period')
        move_obj = self.pool.get('account.move')
        move_line_obj = self.pool.get('account.move.line')
        currency_obj = self.pool.get('res.currency')
        company_currency = asset.company_id.currency_id.id
        current_currency = asset.currency_id.id
        amount = currency_obj.compute(cr, uid, current_currency, company_currency, amount, context=context)
        sign = (asset.category_id.journal_id.type == 'purchase' and 1) or -1
        period_ids = period_obj.find(cr, uid, date.strftime('%Y-%m-%d'), context=context)
        existing_move_ids = move_obj.search(cr, uid, [('period_id','=',period_ids and period_ids[0]),
                                                      '|',('ref','=',asset.category_id.name),('ref','=',asset.name)],
                                            context=context)
        if not existing_move_ids:
            move_vals = {
                'name': '/',
                'date': date.strftime('%Y-%m-%d'),
                'ref': asset.category_id.name,
                'period_id': period_ids and period_ids[0] or False,
                'journal_id': asset.category_id.journal_id.id,
            }
            move_id = move_obj.create(cr, uid, move_vals, context=context)
        else:
            move_id = existing_move_ids[0]
        journal_id = asset.category_id.journal_id.id
        partner_id = asset.partner_id.id
        existing_move_lines = move_line_obj.search(cr, uid, [('move_id','=',move_id),
                                                             ('period_id','=',period_ids and period_ids[0]),
                                                             ('date','=',date.strftime('%Y-%m-%d')),
                                                             '|',('name','=',asset.name),('ref','=',asset.name)])
        if not existing_move_lines:
            move_line_obj.create(cr, uid, {
                'name': asset.name,
                'ref': asset.name,
                'move_id': move_id,
                'account_id': asset.category_id.account_depreciation_id.id,
                'debit': 0.0,
                'credit': amount,
                'period_id': period_ids and period_ids[0] or False,
                'journal_id': journal_id,
                'partner_id': partner_id,
                'currency_id': company_currency != current_currency and  current_currency or False,
                'amount_currency': company_currency != current_currency and - sign * amount or 0.0,
                'date': date.strftime('%Y-%m-%d'),
            })
            move_line_obj.create(cr, uid, {
                'name': asset.name,
                'ref': asset.name,
                'move_id': move_id,
                'account_id': asset.category_id.account_expense_depreciation_id.id,
                'credit': 0.0,
                'debit': amount,
                'period_id': period_ids and period_ids[0] or False,
                'journal_id': journal_id,
                'partner_id': partner_id,
                'currency_id': company_currency != current_currency and  current_currency or False,
                'amount_currency': company_currency != current_currency and sign * amount or 0.0,
                'analytic_account_id': asset.category_id.account_analytic_id.id,
                'date': date.strftime('%Y-%m-%d'),
                'asset_id': asset.id
            })
        return move_id

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: