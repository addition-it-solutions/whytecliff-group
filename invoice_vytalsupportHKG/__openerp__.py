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
    'name': 'Report Layouts - Vytalsupport HKG',
    'version': '1.0',
    'author': 'Whytecliff Group Ltd.',
    'category': 'Accounting & Finance',
    'summary': 'Customization of Reports',
    'website': 'https://www.whytecliffgroup.com',
    'description': """
Report Customization
====================
    * Modified Invoice, SO, RFQ/SO layouts
    * Customized footer for all reports.

""",
    'images': [],
    'depends': ['sale','purchase'],
    'data': [
        'views/report_invoice_document_vytalHKG.xml',
        'views/report_saleorder.xml',
        'views/report_purchasequotation.xml',
        'views/report_purchaseorder.xml',
     ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: