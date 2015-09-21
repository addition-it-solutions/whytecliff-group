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
    'name': 'Accounting - Payment Authorisation',
    'version': '1.0',
    'author': 'Whytecliff Group Pvt. Ltd.',
    'category': 'Accounting & Finance',
    'summary': 'Authorisation form before making payments',
    'website': 'https://www.whytecliffgroup.com',
    'description': """
Payment Form
============
* A user can print out an authorisation form for a payment, in order to invite 
  i.e. accountant to process the payment, after authorisation from the CEO

""",
    'images': [],
    'depends': ['account_voucher', 'purchase'],
    'data': [
        'security/ir.model.access.csv',
        'whytecliff_payment_view.xml',
        'views/payment_form_report.xml',
        'whytecliff_payment_report.xml',
     ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: