from odoo import models, fields, api, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    def _default_job_prefix(self):
        return 'UJN'

    def _default_job_sequence(self):
        return '3057700101'

    job_prefix = fields.Char('Prefix', default=_default_job_prefix,)
    job_sequence = fields.Char('Sequence', default=_default_job_sequence,)

    def update_prefix_users(self):
        for rec in self.browse(self.env.context['active_ids']):
            rec.job_prefix = 'UJN'
            rec.job_sequence = '3057700101'

