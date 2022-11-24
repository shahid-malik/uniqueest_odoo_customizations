# -*- coding: utf-8 -*-
{
    'name': "UCTC Custom Reports",

    'summary': """
        custom reports for UCTC""",

    'description': """
        custom reports for UCTC
    """,

    'author': "Mediod Consulting",
    'website': "http://www.mediodconsulting.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Reporting',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','manage_jobs'],

    # always loaded
    'data': [
        'reports/report.xml',
        'reports/customer_payment_detail_template.xml',
        'reports/customer_jobs_report_template.xml',
    ],
    # only loaded in demonstration mode
    'installable':True,
    'application':True,
}
