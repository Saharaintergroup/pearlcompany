# -*- coding: utf-8 -*-
{
    'name': "Pear Inventory",

    'depends': ['base', 'stock', 'sale', 'sale_stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/product_template.xml',
        'views/stock_picking.xml',
        'views/picking_operations.xml'
        # 'views/stock_return_picking_line.xml',

    ],

}
