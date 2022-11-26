# -*- coding: utf-8 -*-
{
    'name': "booking_order_AHMADYULIANDINATA_26112022",

    'summary': """
        Technical Test Booking Order Odoo 10""",

    'description': """
        Technical Test Ahmad Yulian Dinata
    """,

    'author': "Ahmad Yulian Dinata",
    'website': "https://www.linkedin.com/in/ahmaddyd/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '0.1',
    'installable': True,
    'application': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/canceled_order_view.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/work_order_view.xml',
        'views/booking_order_view.xml',
        'views/service_team_view.xml',
        'views/menu.xml',
        'report/report_work_order.xml',
        'report/report.xml',
        'data/data.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
