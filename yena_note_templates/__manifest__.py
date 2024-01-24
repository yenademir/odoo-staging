{
    'name': "YENA Note Template Development",
    'version': '15.1.0',
    'summary': "Development about the note template in Sale.Order",
    'author': "Selçuk Atav",
    'website': "https://yenaengineering.nl",
    'category': 'Sales',
    'license': 'LGPL-3',
    'depends': ['sale', 'crm','yena_sales_development'],
    'data': [
        'views/sales_note_templates.xml',
        'security/ir.model.access.csv',
    ],
    'installable': True,
    'auto_install': False,
}
