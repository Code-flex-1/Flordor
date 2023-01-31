{
    'name':
        "HR Attendance Overtime",
    'summary':
        """  HR Attendance Overtime        """,
    'author':
        "Code Flex",
    'category':
        'Uncategorized',
    'version':
        '0.1',
    'license':
        'LGPL-3',
    'depends': [
        'hr_attendance',
        'hr_payroll',
        'hr',
    ],
    'external_dependencies': {
        'python': ['toolz'],
    },
    'data': [
        'security/ir.model.access.csv',
        'views/hr_overtime.xml',
        'views/hr_misstime.xml',
        'views/hr_overtime_batch.xml',
        'data/sequences.xml',
    ],
}
