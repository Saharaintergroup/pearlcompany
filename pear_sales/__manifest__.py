# -*- coding: utf-8 -*-
{
    'name': "Pear Sales",

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'purchase'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'reports/report.xml',
        'wizards/so_report.xml',
        'views/res_partner.xml',
        'views/sale_order.xml',
        'views/account_move.xml',
        'views/sale_order_report.xml',
        'views/invoice_report.xml',
        'views/purchase_report.xml',
        'views/res_users.xml',
        'views/report_so_report.xml',

    ]

}
