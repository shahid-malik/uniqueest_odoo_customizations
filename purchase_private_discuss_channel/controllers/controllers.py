# -*- coding: utf-8 -*-
# from odoo import http


# class PurchasePrivateDiscussChannel(http.Controller):
#     @http.route('/purchase_private_discuss_channel/purchase_private_discuss_channel/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/purchase_private_discuss_channel/purchase_private_discuss_channel/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('purchase_private_discuss_channel.listing', {
#             'root': '/purchase_private_discuss_channel/purchase_private_discuss_channel',
#             'objects': http.request.env['purchase_private_discuss_channel.purchase_private_discuss_channel'].search([]),
#         })

#     @http.route('/purchase_private_discuss_channel/purchase_private_discuss_channel/objects/<model("purchase_private_discuss_channel.purchase_private_discuss_channel"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('purchase_private_discuss_channel.object', {
#             'object': obj
#         })
