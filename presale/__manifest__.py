{
    'name': 'Presales order',
    'version': '1.0',
    'description': 'An app to manage pre-saling',
    'summary': 'Manage your presales',
    'author': 'Vincent Sevestre',
    'license': 'LGPL-3',
    'category': 'Presale',
    'depends': [
        'base',
        'mail',
        'sale_management',
    ],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/presale_order_views.xml',
        'views/presale_order_line_views.xml',
        'views/presale_menus.xml',
        'views/sale_order_views.xml',
        'data/scheduler.xml',
    ],
    'auto_install': False,
    'application': True
}
