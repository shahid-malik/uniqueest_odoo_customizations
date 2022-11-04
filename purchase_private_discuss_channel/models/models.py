# -*- coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseOrder(models.Model):

    _inherit = 'purchase.order'

    @api.model
    def get_discuss_user_domains(self):
        users = self.env['res.users'].sudo().search([])
        res = list()
        for user in users:
            res.append(user.partner_id.id)
        return [('id','in', res)]

    private_channel_partner_ids = fields.Many2many("res.partner", string="Discussion Users", domain=lambda self:self.get_discuss_user_domains())

    source_document_file = fields.Binary("Source Document File")
    final_approved_file = fields.Binary("Final Approved File")

    private_discuss_channel_id = fields.Many2one('mail.channel', string="Discussion Channel")

    job_number = fields.Char("Job Number")

    freight = fields.Monetary("Freight Charges")

    work_type = fields.Char("Type of Work")
    quote_status = fields.Char("Quote Status")
    quote_submit_user_id = fields.Many2one("res.partner", "Quote Submitted By", domain=[("company_type", "=", "person")])
    order_status = fields.Char("Order Status")
    contact_person = fields.Char("Contact Person")
    contact_number = fields.Char("Contact Number")
    contact_email = fields.Char("Contact Email")
    pr_remarks = fields.Text("PR Remarks")

    @api.depends('order_line.price_total', 'freight')
    def _amount_all(self):
        for order in self:
            amount_untaxed = amount_tax = 0.0
            for line in order.order_line:
                line._compute_amount()
                amount_untaxed += line.price_subtotal
                amount_tax += line.price_tax
            order.update({
                'amount_untaxed': order.currency_id.round(amount_untaxed),
                'amount_tax': order.currency_id.round(amount_tax),
                'amount_total': amount_untaxed + amount_tax + order.freight,
            })

    @api.model
    def create(self, vals):
        """
        """
        res = super(PurchaseOrder, self).create(vals)
        if res.private_channel_partner_ids: 
            vals = {
                'name':res.name,
                'description':"Discussion Channel for {}".format(res.name),
            }
            channel_id = self.env['mail.channel'].sudo().create(vals)
            for partner in res.private_channel_partner_ids:
                self.env['mail.channel.partner'].sudo().create({
                        'partner_id':partner.id,
                        'channel_id':channel_id.id,
                    })
            res.write({'private_discuss_channel_id':channel_id.id})
        return res

    def update_private_channel(self):
        """
        """
        if self.private_discuss_channel_id:
            self.private_discuss_channel_id.channel_last_seen_partner_ids.unlink()
            for partner in self.private_channel_partner_ids:
                self.env['mail.channel.partner'].create({
                        'partner_id':partner.id,
                        'channel_id':self.private_discuss_channel_id.id,
                    })

    def open_discuss_wizard(self):
        """
        """
        action_id = self.env.ref("mail.action_discuss").id
        return {                   
            'name'     : 'Go to website',
            'res_model': 'ir.actions.act_url',
            'type'     : 'ir.actions.act_url',
            'target'   : 'new',
            'url'      : "/web#action={}&active_id=mail.channel_{}&menu_id={}".format( action_id,self.private_discuss_channel_id.id,self.env.ref("mail.menu_root_discuss").id)
        }
