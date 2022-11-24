from odoo import models, api, _
from odoo.exceptions import ValidationError


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'

    @api.constrains('name')
    def check_name(self):
        for rec in self:
            partner_ids = self.env['res.partner'].sudo().search([('name', '=', rec.name), ('id', '!=', rec.id)])
            if partner_ids:
                raise ValidationError(_('Name %s already exists! You must add a unique name' % rec.name))
