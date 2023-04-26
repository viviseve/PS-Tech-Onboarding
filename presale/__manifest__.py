{
    'name': 'Presales order',
    'version': '16.0.1.0.0',
    'description': 'An app to manage pre-saling',
    'website': 'https://www.odoo.com',
    'summary': 'Manage your presales',
    'author': 'Vincent Sevestre, Odoo PS',
    'license': 'OEEL-1',
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
