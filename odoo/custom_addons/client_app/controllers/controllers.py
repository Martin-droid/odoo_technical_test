# -*- coding: utf-8 -*-
# from odoo import http


# class ClientApp(http.Controller):
#     @http.route('/client_app/client_app', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/client_app/client_app/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('client_app.listing', {
#             'root': '/client_app/client_app',
#             'objects': http.request.env['client_app.client_app'].search([]),
#         })

#     @http.route('/client_app/client_app/objects/<model("client_app.client_app"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('client_app.object', {
#             'object': obj
#         })
