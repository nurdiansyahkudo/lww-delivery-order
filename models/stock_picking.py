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
    customer_id = fields.Many2one(
        'res.partner', string="Delivery Address",
        check_company=True, index='btree_not_null')
    sale_id = fields.Many2one('sale.order', compute="_compute_sale_id", inverse="_set_sale_id", string="Sales Order", store=True, index='btree_not_null')
    project_id = fields.Many2one('project.project', string="Project")

    print_template = fields.Selection([
        ('with_header', 'With Header'),
        ('without_header', 'Without Header'),
    ], string="Print Template", default='with_header', required=True)

    @api.constrains('project_id', 'picking_type_code')
    def _check_project_required_for_outgoing(self):
        for rec in self:
            if rec.picking_type_code == 'outgoing' and not rec.project_id:
                raise ValidationError("Project is required for Delivery Order.")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        return {
            'domain': {'project_id': [('partner_id', '=', self.partner_id.id)]},
            'value': {'project_id': False},
        }
    
    @api.onchange('project_id')
    def _onchange_project_id(self):
        if self.project_id:
            return {
                'domain': {
                    'sale_id': [('project_id', '=', self.project_id.id)]
                }
            }
    
    # @api.depends('group_id', 'project_id')
    # def _compute_sale_id(self):
    #     for picking in self:
    #         if picking.group_id and picking.group_id.sale_id:
    #             picking.sale_id = picking.group_id.sale_id
    #         elif (
    #             picking.project_id
    #             and hasattr(picking.project_id, 'reinvoiced_sale_order_id')
    #             and picking.project_id.reinvoiced_sale_order_id
    #         ):
    #             picking.sale_id = picking.project_id.reinvoiced_sale_order_id
    #         else:
    #             picking.sale_id = False

    # def _set_sale_id(self):
    #     for picking in self:
    #         if picking.group_id:
    #             picking.group_id.sale_id = picking.sale_id
    #         else:
    #             vals = {
    #                 'sale_id': picking.sale_id.id,
    #                 'name': picking.sale_id.name,
    #             } if picking.sale_id else {}

    #             pg = self.env['procurement.group'].create(vals)
    #             picking.group_id = pg

    # print DO with header
    def action_print_report(self):
        company = self.env['res.company'].browse(self.env.company.id)
        
        if company.name == 'PT. BINA SERVICE':
            return self.env.ref('lww_delivery.action_report_bs_do').report_action(self)
        elif company.name == 'PT. SPARTADUA RIBUJAYA':
            return self.env.ref('lww_delivery.action_report_spartadua_do').report_action(self)
        elif company.name == 'PT. PRATAMA DATAMAKSIMA':
            return self.env.ref('lww_delivery.action_report_pratama_do').report_action(self)
        elif company.name == 'PT. AMANERA BERSAMA ABADI':
            return self.env.ref('lww_delivery.action_report_amanera_do').report_action(self)
        elif company.name == 'PT. IMADEA MAGKASAMA':
            return self.env.ref('lww_delivery.action_report_imadea_do').report_action(self)
        else:
            # Jika perusahaan tidak cocok dengan ketiganya, menggunakan laporan default
            return self.env.ref('lww_delivery.action_report_limawira_do').report_action(self)
    
    # print DO without header
    def action_print_report_no_header(self):
        company = self.env['res.company'].browse(self.env.company.id)

        if company.name == 'PT. BINA SERVICE':
            return self.env.ref('lww_delivery.action_report_bs_do_no_header').report_action(self)
        elif company.name == 'PT. SPARTADUA RIBUJAYA':
            return self.env.ref('lww_delivery.action_report_spartadua_do_no_header').report_action(self)
        elif company.name == 'PT. PRATAMA DATAMAKSIMA':
            return self.env.ref('lww_delivery.action_report_pratama_do_no_header').report_action(self)
        elif company.name == 'PT. IMADEA MAGKASAMA':
            return self.env.ref('lww_delivery.action_report_imadea_do_no_header').report_action(self)
        elif company.name == 'PT. AMANERA BERSAMA ABADI':
            return self.env.ref('lww_delivery.action_report_amanera_do_no_header').report_action(self)
        else:
            return self.env.ref('lww_delivery.action_report_limawira_do_no_header').report_action(self)
    
    def action_print_receipt_report(self):
        company = self.env['res.company'].browse(self.env.company.id)
        
        if company.name == 'PT. BINA SERVICE':
            return self.env.ref('lww_delivery.action_report_bs_receipt').report_action(self)
        elif company.name == 'PT. SPARTADUA RIBUJAYA':
            return self.env.ref('lww_delivery.action_report_spartadua_receipt').report_action(self)
        elif company.name == 'PT. PRATAMA DATAMAKSIMA':
            return self.env.ref('lww_delivery.action_report_pratama_receipt').report_action(self)
        elif company.name == 'PT. IMADEA MAGKASAMA':
            return self.env.ref('lww_delivery.action_report_imadea_receipt').report_action(self)
        elif company.name == 'PT. AMANERA BERSAMA ABADI':
            return self.env.ref('lww_delivery.action_report_amanera_receipt').report_action(self)
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
