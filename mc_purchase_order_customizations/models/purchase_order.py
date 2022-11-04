from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    job_id = fields.Many2one(comodel_name='jobs.management', string='Job Number')

    # def write(self, vals):
    #     res = super(PurchaseOrder, self).write(vals)
    #     if 'job_id' in vals:
    #         job_id = vals.get('job_id')
    #         job_rec = self.env['jobs.management'].sudo().search([('id', '=', job_id)])
    #         job_rec.purchase_order_id = self.id
    #     return res
