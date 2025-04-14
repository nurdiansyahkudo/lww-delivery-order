from odoo import models, fields, api
from odoo.exceptions import ValidationError
from num2words import num2words

class StockPicking(models.Model):
    _inherit = "stock.picking"

    no_do = fields.Char(string='DO Number', store=True)
    receipt_no = fields.Char(string='Receipt Number', store=True)
    employee_id = fields.Many2many(
        'hr.employee',
        string="Responsible",
        store=True
    )
    sale_id = fields.Many2one('sale.order', compute="_compute_sale_id", inverse="_set_sale_id", string="Sales Order", store=True, index='btree_not_null', required=True)
    project_id = fields.Many2one('project.project', required=True)

    def action_print_report(self):
        company = self.env['res.company'].browse(self.env.company.id)
        
        if company.name == 'PT. BINA SERVICE':
            return self.env.ref('lww_delivery.action_report_bs_do').report_action(self)
        elif company.name == 'PT. SPARTADUA RIBUJAYA':
            return self.env.ref('lww_delivery.action_report_spartadua_do').report_action(self)
        else:
            # Jika perusahaan tidak cocok dengan ketiganya, menggunakan laporan default
            return self.env.ref('lww_delivery.action_report_limawira_do').report_action(self)
    
    def action_print_receipt_report(self):
        company = self.env['res.company'].browse(self.env.company.id)
        
        if company.name == 'PT. BINA SERVICE':
            return self.env.ref('lww_delivery.action_report_bs_receipt').report_action(self)
        elif company.name == 'PT. SPARTADUA RIBUJAYA':
            return self.env.ref('lww_delivery.action_report_spartadua_receipt').report_action(self)
        else:
            # Jika perusahaan tidak cocok dengan ketiganya, menggunakan laporan default
            return self.env.ref('lww_delivery.action_report_limawira_receipt').report_action(self)

    def write(self, vals):
        if 'no_do' in vals and vals['no_do']:
            for record in self:
                existing_record = self.env['stock.picking'].search([
                    ('no_do', '=', vals['no_do']),
                    ('id', '!=', record.id)
                ], limit=1)
                if existing_record:
                    raise ValidationError('DO Sudah Ada!')
        
        if 'receipt_no' in vals and vals['receipt_no']:
            for record in self:
                existing_receipt = self.env['stock.picking'].search([
                    ('receipt_no', '=', vals['receipt_no']),
                    ('id', '!=', record.id)
                ], limit=1)
                if existing_receipt:
                    raise ValidationError('RG Sudah Ada!')
                
        return super().write(vals)
    
    def get_print_report_name(self):
        return 'Delivery Order - %s' % (self.name)
    
    def get_receipt_report_name(self):
        return 'Receipt Goods - %s' % (self.name)
