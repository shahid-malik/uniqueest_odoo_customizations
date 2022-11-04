from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class JobsManagement(models.Model):
    _name = 'jobs.management'
    _description = "Job Management"
    _inherit = ["mail.thread", 'mail.activity.mixin', 'portal.mixin']

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    name = fields.Char('Job Number', readonly=True, copy=False, required=True, default=lambda self: _('New'))
    partner_id = fields.Many2one('res.partner', string='Customer', required=True,)
    company_id = fields.Many2one('res.company', string='Company', index=True, required=True, default=lambda self: self.env.company, readonly=True)
    currency_id = fields.Many2one('res.currency', string='Currency', required=True, default=lambda self: self._default_currency_id())
    user_id = fields.Many2one('res.users', string='User', index=True, required=True, default=lambda self: self.env.user)
    next_assign = fields.Many2one('res.users', string='Next Assign', required=True, index=True, default=lambda self: self.env.user)
    user_ids = fields.Many2many('res.users', 'job_rel_id', 'user_id_rel', string='User Ids', compute='_get_users')
    expense_ids = fields.Many2many('hr.expense', 'job_rel_id', 'expense_id_rel', string='Job Expense', compute='_get_expense')
    type = fields.Char('Type of work', required=True)
    date = fields.Date('Date', required=True, default=fields.Date.today)
    purchase_number = fields.Char('PO Number')
    invoice_number = fields.Char('Invoice Number')
    total = fields.Monetary('Total With VAT', compute='compute_total')
    total_amount_received = fields.Monetary('Total Payment Received')
    total_amount_pending = fields.Monetary('Total Payment Pending', compute='compute_total_pending_amount')
    without_vat_total = fields.Monetary('Total Without VAT', required=True)
    without_vat_total_readonly = fields.Monetary('Total without VAT', compute='onchange_without_vat_total_readonly')
    vat_amount = fields.Monetary('VAT Amount', compute='compute_total')
    remark = fields.Text('Remark')
    vat = fields.Float('VAT in %', required=True)
    total_payable = fields.Float('Total Payable %')
    total_payable_amount = fields.Monetary('Total Payable Amount', compute='compute_total_payable')
    total_paid_amount = fields.Monetary('Total Paid')
    remaining_amount = fields.Monetary('Remaining Amount', compute='compute_remaining_amount')
    follow_up_date = fields.Date('Follow up date')
    status = fields.Selection([('open', 'Open'), ('close', 'Closed'), ('cancel', 'Canceled')], 'Status',
                              default='open')
    quotation = fields.Binary(string='Quotation', attachment=True,)
    purchase_order = fields.Binary(string='Purchase Order', attachment=True,)
    delivery_order = fields.Binary(string='Delivery Report', attachment=True,)
    payment_slip = fields.Binary(string='Payment Slip', attachment=True,)
    invoice = fields.Binary(string='Invoice', attachment=True,)
    job_report = fields.Binary(string='Job Report', attachment=True,)
    expenses_report = fields.Binary(string='Expenses', attachment=True,)
    other_report = fields.Binary(string='Other', attachment=True,)
    users_count = fields.Integer(compute='_compute_users_count')
    expense_count = fields.Integer(compute='_compute_expense_count', string='Expenses')
    job_expense = fields.Monetary('Total Expense', compute='get_per_job_expense')
    expense_profit = fields.Monetary(string='Profit', compute='set_per_job_profit')

    @api.onchange('without_vat_total')
    def onchange_without_vat_total_readonly(self):
        for rec in self:
            rec.without_vat_total_readonly = rec.without_vat_total

    @api.constrains('without_vat_total', 'vat')
    def _check_amount_vat(self):
        for rec in self:
            if rec.without_vat_total == 0:
                raise ValidationError(_("Total Without Vat Cannot Be 0"))
            if rec.vat == 0:
                raise ValidationError(_("Vat Percentage cannot be 0"))

    @api.onchange('total_amount_received')
    @api.depends('total_amount_received')
    def compute_total_pending_amount(self):
        for rec in self:
            rec.total_amount_pending = rec.total - rec.total_amount_received

    @api.onchange('total_paid_amount', 'total_payable_amount')
    @api.depends('total_paid_amount', 'total_payable_amount')
    def compute_remaining_amount(self):
        for rec in self:
            rec.remaining_amount = rec.total_payable_amount - rec.total_paid_amount

    @api.onchange('without_vat_total', 'total_payable')
    @api.depends('without_vat_total', 'total_payable')
    def compute_total_payable(self):
        for rec in self:
            rec.total_payable_amount = rec.without_vat_total * (rec.total_payable / 100)

    def action_confirm(self):
        for rec in self:
            if rec.status == 'close':
                raise ValidationError(_('Record Already Closed'))
            elif rec.status == 'cancel':
                raise ValidationError(_('Cannot Close Canceled Record'))
            else:
                rec.write({'status': 'close'})

    def action_cancel(self):
        for rec in self:
            if rec.status == 'close':
                raise ValidationError(_('Cannot Cancel Closed Record'))
            elif rec.status == 'cancel':
                raise ValidationError(_('Record Already Canceled'))
            else:
                rec.write({'status': 'cancel'})

    def action_reopen(self):
        for rec in self:
            if rec.status == 'open':
                raise ValidationError(_('Already On Open State'))
            else:
                rec.write({'status': 'open'})

    def action_open_users(self):
        res = self.env['ir.actions.act_window']._for_xml_id('base.action_res_users')
        return res

    # def action_expenses(self):
    #     res = self.env['ir.actions.act_window']._for_xml_id('hr_expense.hr_expense_actions_my_all')
    #     return res

    def action_open_expenses(self):
        expense_ids = self.env['hr.expense'].search([('job_management_id', '=', self.id)])
        return {
            'type': 'ir.actions.act_window',
            'name': "Expenses",
            'res_model': 'hr.expense',
            'view_mode': 'tree,form',
            'domain': [('id', 'in', [x.id for x in expense_ids])],
            'context': {'delete': False,
                        'default_job_management_id': self.id,
                        'default_company_id': self.company_id.id,
                        'default_readonly_job_id': True
                        },
            'target': 'current',
        }

    def _compute_expense_count(self):
        for rec in self:
            record = self.env['hr.expense'].search_count([('job_management_id', '=', self.id)])
            rec.expense_count = record

    def _compute_users_count(self):
        for rec in self:
            record = self.env['res.users'].search_count([])
            rec.users_count = record

    @api.depends('user_ids')
    def _get_users(self):
        for rec in self:
            c_id = []
            lst = []
            u_id = self.env['res.users'].search([])
            for lines in u_id:
                lst.append(lines.id)
            c_id = [(6, 0, lst)]
            rec.user_ids = c_id

    @api.depends('expense_ids')
    def _get_expense(self):
        for rec in self:
            c_id = []
            lst = []
            e_id = self.env['hr.expense'].search([('job_management_id', '=', self.id)])
            for lines in e_id:
                lst.append(lines.id)
            c_id = [(6, 0, lst)]
            rec.expense_ids = c_id

    def get_per_job_expense(self):
        for rec in self:
            tot = 0
            for ex in rec.expense_ids:
                tot += ex.total_amount_company
            rec.job_expense = tot

    def set_per_job_profit(self):
        for rec in self:
            rec.expense_profit = rec.without_vat_total - rec.job_expense

    @api.onchange('vat', 'without_vat_total')
    @api.depends('vat', 'without_vat_total')
    def compute_total(self):
        for rec in self:
            rec.vat_amount = rec.without_vat_total * (rec.vat/100)
            rec.total = rec.vat_amount + rec.without_vat_total

    # @api.model
    # def create(self, vals):
    #     res = super(JobsManagement, self).create(vals)
    #     if res.user_id.job_sequence < 10:
    #         seq = '00'+str(res.user_id.job_sequence)
    #     elif res.user_id.job_sequence >= 10 and res.user_id.job_sequence <= 99 :
    #         seq = '0' + str(res.user_id.job_sequence)
    #     else:
    #         seq = str(res.user_id.job_sequence)
    #     res.name = res.user_id.job_prefix + '-' + seq
    #     res.sudo().user_id.job_sequence += 1
    #     return res

    @api.model
    def create(self, vals):
        res = super(JobsManagement, self).create(vals)
        seq = res.user_id.job_sequence
        res.name = res.user_id.job_prefix + seq
        int_seq = int(seq)
        int_seq += 1
        str_seq = str(int_seq)
        res.sudo().user_id.job_sequence = str_seq
        return res

