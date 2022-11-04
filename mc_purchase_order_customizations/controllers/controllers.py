# -*- coding: utf-8 -*-
# from odoo import http


# class McPurchaseOrderCustomizations(http.Controller):
#     @http.route('/mc_purchase_order_customizations/mc_purchase_order_customizations/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mc_purchase_order_customizations/mc_purchase_order_customizations/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mc_purchase_order_customizations.listing', {
#             'root': '/mc_purchase_order_customizations/mc_purchase_order_customizations',
#             'objects': http.request.env['mc_purchase_order_customizations.mc_purchase_order_customizations'].search([]),
#         })

#     @http.route('/mc_purchase_order_customizations/mc_purchase_order_customizations/objects/<model("mc_purchase_order_customizations.mc_purchase_order_customizations"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mc_purchase_order_customizations.object', {
#             'object': obj
#         })
