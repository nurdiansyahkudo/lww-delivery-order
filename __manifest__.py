# -*- coding: utf-8 -*-
{
    'name': "Limawira Delivery and Receipt",
    'summary': '',
    'author': '',
    'category': 'Uncategorized',
    'version': '1.0',
    'depends': ['base', 'stock'],
    'data': [
        # RECEIPT GOODS
        'report/lww_receipt_report.xml',
        'views/lww_receipt_template.xml',
        'views/bs_receipt_template.xml',
        # 'views/spartadua_receipt_template.xml',
        # DELIVERY ORDER
        'report/lww_do_report.xml',
        'views/lww_do_template.xml',
        'views/bs_do_template.xml',
        'views/spartadua_do_template.xml',
        # DELIVERY ORDER NO HEADER
        'views/lww_do_template_no_header.xml',
        # FORM VIEW
        'views/stock_picking_view.xml',
        # SECURITY (ACCESS)
        # 'security/ir.model.access.csv',
    ],
    'installable': True,
    'application': False,
}

