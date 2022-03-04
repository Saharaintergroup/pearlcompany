# -*- coding: utf-8 -*-
{
    'name': "Pear Inventory",

    'depends': ['base', 'stock', 'sale', 'sale_stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/product_template.xml',
        'views/stock_picking.xml',

    ],

}
