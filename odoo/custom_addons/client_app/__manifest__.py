{
    'name': 'Client App',
    'version': '1.0',
    'summary': 'Module for managing client orders, payments, invoices, and dashboard analytics',
    'description': 'This module manages client orders, payments, invoices, and includes a payment analytics chart.',
    'category': 'Uncategorized',
    'author': 'Your Name',
    'depends': ['base', 'mail', 'web'],
    'data': [
        'views/client_app_views.xml',  
        'views/pivot_view.xml',        
        'views/calendar_view.xml',     
        'views/portal_view.xml',      
        'views/report_profit.xml',   
        'views/report_actions.xml',    
        'security/ir.model.access.csv' 
    ],
    'assets': {
        'web.assets_backend': [
            '/client_app/static/lib/chartjs/chart.min.js',  
            '/client_app/static/src/js/dashboard_chart.js', 
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
