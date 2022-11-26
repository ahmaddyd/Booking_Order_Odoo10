# -*- coding: utf-8 -*-
# from odoo import http


# class BookingOrderAhmadYulianDinata(http.Controller):
#     @http.route('/booking_order__ahmad_yulian_dinata/booking_order__ahmad_yulian_dinata/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/booking_order__ahmad_yulian_dinata/booking_order__ahmad_yulian_dinata/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('booking_order__ahmad_yulian_dinata.listing', {
#             'root': '/booking_order__ahmad_yulian_dinata/booking_order__ahmad_yulian_dinata',
#             'objects': http.request.env['booking_order__ahmad_yulian_dinata.booking_order__ahmad_yulian_dinata'].search([]),
#         })

#     @http.route('/booking_order__ahmad_yulian_dinata/booking_order__ahmad_yulian_dinata/objects/<model("booking_order__ahmad_yulian_dinata.booking_order__ahmad_yulian_dinata"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('booking_order__ahmad_yulian_dinata.object', {
#             'object': obj
#         })
