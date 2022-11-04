from odoo import models, fields, api


class JobsManagement(models.Model):
    _inherit = 'jobs.management'

    purchase_order_id = fields.Many2one(comodel_name='purchase.order', string='PO Number')

    def write(self, vals):
        res = super(JobsManagement, self).write(vals)
        if 'purchase_order_id' in vals:
            po_id = vals.get('purchase_order_id')
            po = self.env['purchase.order'].sudo().search([('id', '=', po_id)])
            po.job_id = self.id
        return res
