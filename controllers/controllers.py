# -*- coding: utf-8 -*-
# from odoo import http


# class LwwDelivery(http.Controller):
#     @http.route('/lww_delivery/lww_delivery', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/lww_delivery/lww_delivery/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('lww_delivery.listing', {
#             'root': '/lww_delivery/lww_delivery',
#             'objects': http.request.env['lww_delivery.lww_delivery'].search([]),
#         })

#     @http.route('/lww_delivery/lww_delivery/objects/<model("lww_delivery.lww_delivery"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('lww_delivery.object', {
#             'object': obj
#         })

