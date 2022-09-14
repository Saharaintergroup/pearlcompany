# -*- coding: utf-8 -*-
{
    'name': "Sales Commission",

    'description': """
        Sales Commission Structure
    """,

    'depends': ['base','account','sale'],

    # always loaded
    'data': [
       'security/ir.model.access.csv',
        'views/res_partner.xml',
        'views/account_move.xml',
        # 'views/product_template.xml',
        'views/sales_commission.xml',

    ],

}
