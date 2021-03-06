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
from openerp import models, api, _

class whytecliff_debrand(models.Model):
    _inherit = "mail.notification"
    
    @api.model
    def get_signature_footer(self, user_id, res_model=None, res_id=None, context=None, user_signature=True):
        footer = super(whytecliff_debrand,self).get_signature_footer(user_id)
        footer = str(footer)
        modify_sign = footer[footer.find('using'):]
        footer = footer.replace(modify_sign,"</small>")
        return footer

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
