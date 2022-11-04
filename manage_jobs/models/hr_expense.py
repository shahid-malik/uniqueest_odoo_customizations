from odoo import models, fields, api, _


class Expense(models.Model):
    _inherit = "hr.expense"

    job_management_id = fields.Many2one('jobs.management', string='Job Number')
    readonly_job_id = fields.Boolean('Readonly Job Management Selection')
    submitted_by = fields.Char('Submitted By')

    @api.model
    def default_get(self, fields):
        res = super(Expense, self).default_get(fields)
        res['payment_mode'] = 'company_account'
        return res
