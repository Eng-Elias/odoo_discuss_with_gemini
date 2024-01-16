# -*- coding: utf-8 -*-
# from odoo import http


# class GeminiDiscussIntegration(http.Controller):
#     @http.route('/gemini_discuss_integration/gemini_discuss_integration', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gemini_discuss_integration/gemini_discuss_integration/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gemini_discuss_integration.listing', {
#             'root': '/gemini_discuss_integration/gemini_discuss_integration',
#             'objects': http.request.env['gemini_discuss_integration.gemini_discuss_integration'].search([]),
#         })

#     @http.route('/gemini_discuss_integration/gemini_discuss_integration/objects/<model("gemini_discuss_integration.gemini_discuss_integration"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gemini_discuss_integration.object', {
#             'object': obj
#         })

