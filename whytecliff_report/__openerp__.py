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
{
    'name': 'Accounting - Report Customizations',
    'version': '1.0',
    'author': 'Whytecliff Group Pvt. Ltd.',
    'category': 'Accounting & Finance',
    'summary': 'Customization of P&L and Balance Sheet Reports',
    'website': 'https://www.whytecliffgroup.com',
    'description': """
Report Customization
====================
    * Balance sheet
    * Balance Sheet Period Analysis
    * General Ledger Profit and Loss Report
    * Net Aged AR AP In Local By Org Report
    * Profit And Loss Period Analysis

""",
    'images': [],
    'depends': ['account'],
    'data': [
        'wizard/profit_loss_view.xml',
        'wizard/general_ledger_view.xml',
        'wizard/aged_partner_balance_view.xml',
        'wizard/profit_loss_variance_view.xml',
        'wizard/ar_aged_outstanding_view.xml',
        'views/report_ar_aged_outstanding.xml',
        'views/report_profit_loss_variance.xml',
        'views/report_aged_partner_balance.xml',
        'views/report_profit_loss.xml',
        'views/report_balance_sheet.xml',
        'views/report_generalledger.xml',
        'whytecliff_report.xml',
     ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: