{
    "name": "Jobs Management",
    "version": "1.0",
    "license": "OPL-1",
    "author": "TraceNcode Technologies",
    "category": "Project",
    "website": "https://tracencode.com/",
    "summary": '''
        This project is all about managing users and access rights for the particular users and jobs to be created and
         based on the jobs vat is calculated for the particular jobs.''',

    "depends": ['base', 'mail', 'hr_expense', 'hr'],
    "data": [
        'security/ir.model.access.csv',
        'security/manage_jobs_security.xml',
        'views/jobs_management_views.xml',
        'views/res_users_views.xml',
        'views/hr_expense_views.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
