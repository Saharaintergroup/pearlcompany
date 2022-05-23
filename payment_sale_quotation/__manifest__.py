# -*- coding: utf-8 -*-
{
    'name': "Payment Sale Quotation",

    'depends': ['base', 'account', 'sale_management'],
    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_views.xml',
        'wizard/sale_order_wizard_views.xml',
        'report/sale_order_report.xml',
    ],
    # only loaded in demonstration mode

}
