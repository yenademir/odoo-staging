{
    'name': 'JSPDF Fix',
    'version': '1.0',
    'summary': 'Fixes JSPDF issues',
    'category': 'Tools',
    'author': 'Emre MATARACI',
    'website': 'www.yenaengineering.nl',
    'depends': ['web'],
    'data': [],
    'qweb': [],
    'assets': {
        'web.assets_frontend': [
            'jspdf_fix/static/src/js/jspdf_custom.js',
        ],
        'web.assets_backend': [
            'jspdf_fix/static/src/js/jspdf_custom.js',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
