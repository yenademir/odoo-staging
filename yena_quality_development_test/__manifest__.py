{
    'name': 'Yena Quality Development',
    'version': '1.0',
    'summary': 'Custom Quality Development Module for Yena Engineering',
    'description': 'This module provides specialized quality control and development processes for use by Yena Engineering.',
    'category': 'Custom',
    'author': 'Emre Mataracı',
    'website': 'www.yenaengineering.nl',
    'depends': ['product', 'stock', 'purchase', 'base','delivery', 'yena_purchase_development_test', 'yena_inventory_development_test'],
    'data': [
        'views/quality_development.xml',
        'security/ir.model.access.csv',
        'views/quality_overview.xml',
        'wizards/upload_document.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'yena_quality_development_test/static/src/js/url_viewer.js',
           # 'yena_quality_development_test/static/src/js/material_type_widget.js',
        ],
        'web.assets_qweb': [
            'yena_quality_development_test/static/src/xml/url_viewer.xml',
           # 'yena_quality_development_test/static/src/xml/template.xml',
        ],
    },
    

    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
