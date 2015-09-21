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
from openerp import tools, SUPERUSER_ID
#import openerp.addons.decimal_precision as dp

class whytecliff_debrand(models.Model):
    _inherit = "mail.notification"
    
    @api.model
    def get_signature_footer(self, user_id, res_model=None, res_id=None, context=None, user_signature=True):
        
        footer = ""
        if not user_id:
            return footer

        # add user signature
        user = self.env['res.users'].browse([user_id])[0]
        if user_signature:
            if user.signature:
                signature = user.signature
            else:
                signature = "--<br />%s" % user.name
            footer = tools.append_content_to_html(footer, signature, plaintext=False)
        # add company signature
        if user.company_id.website:
            website_url = ('http://%s' % user.company_id.website) if not user.company_id.website.lower().startswith(('http:', 'https:')) \
                else user.company_id.website
            company = "<a style='color:inherit' href='%s'>%s</a>" % (website_url, user.company_id.name)
        else:
            company = user.company_id.name
            
        sent_by = _('Sent by %(company)s using %(odoo)s')
        
        company_name = user.company_id.name
        
        if company_name == 'Vytal Support (Hong Kong) Ltd':
            signature_company = '<br /><small>%s</small>' % (sent_by % {
                'company': company,
                'odoo': "<a style='color:inherit' href='http://managerhkg.vytalsupport.com/'>Vytal Support (Hong Kong) Ltd</a>"
            })
        elif company_name == 'Cliff Premiums Ltd':
            signature_company = '<br /><small>%s</small>' % (sent_by % {
                'company': company,
                'odoo': "<a style='color:inherit' href='http://cliffpremiums.com/'>Cliff Premiums Ltd</a>"
            })
        elif company_name == 'Whytecliff Group':
            signature_company = '<br /><small>%s</small>' % (sent_by % {
                'company': company,
                'odoo': "<a style='color:inherit' href='http://manager.whytecliff.com/'>Whytecliff Group</a>"
            })
        elif company_name == 'Whytecliff Consultants Ltd':
            signature_company = '<br /><small>%s</small>' % (sent_by % {
                'company': company,
                'odoo': "<a style='color:inherit' href='http://manager.whytecliffconsultants.com/'>Whytecliff Consultants Ltd</a>"
            })
        elif company_name == 'Vytal Support (Thailand) Co Ltd':
            signature_company = '<br /><small>%s</small>' % (sent_by % {
                'company': company,
                'odoo': "<a style='color:inherit' href='http://manager.vytalsupport.com/'>Vytal Support (Thailand) Co Ltd</a>"
            })
        elif company_name == 'Playerlayer HKG':
            signature_company = '<br /><small>%s</small>' % (sent_by % {
                'company': company,
                'odoo': "<a style='color:inherit' href='https://manager.playerlayer.com.hk/'>Playerlayer HKG</a>"
            })
        else:
            signature_company = '<br /><small>%s</small>' % (sent_by % {
                'company': company,
                'odoo': "<a style='color:inherit' href='http://www.odoo.com/'>Odoo</a>"
            })

        footer = tools.append_content_to_html(footer, signature_company, plaintext=False, container_tag='div')

        return footer


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: