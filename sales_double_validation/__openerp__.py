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
    'name': 'Sale Order Workflow',
    'version': '1.0',
    'author': 'Whytecliff Group Pvt. Ltd.',
    'category': 'Sales',
    'summary': 'Double approval on sales order',
    'website': 'https://www.whytecliffgroup.com',
    'description': """
    
* Double approval on sales order

""",
    'images': [],
    'depends': ['sale'],
    'data': [
        #'security/ir.model.access.csv',
        'sales_double_validation_view.xml',
        'sales_double_validation_workflow.xml'
        #'views/payment_form_report.xml',
        #'whytecliff_payment_report.xml',
     ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
