# -*- coding: utf-8 -*-
{
    'name': "MC Purchase Order and Job Management Customizations",

    'summary': """
        Customization of Modules by Mediod Consulting """,

    'description': """
        Customization of Job management and purchase order modules.
    """,

    'author': "Mediod Consulting",
    'website': "http://www.mediodconsulting.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Purchase',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase', 'manage_jobs', 'contacts', 'purchase_private_discuss_channel'],

    # always loaded
    'data': [
        'views/purchase_order.xml',
        'views/job_management.xml',
        'views/res_partner.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
