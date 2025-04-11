from odoo import models, fields

class PrintDoWizard(models.TransientModel):
    _name = 'print.do'
    _description = 'Print DO Wizard'

    option = fields.Selection([
        ('with_header', 'Print DO'),
        ('without_header', 'Print DO without Header')
    ], string='Print Option', required=True, default='with_header')

    def action_confirm(self):
      active_id = self.env.context.get('active_id')
      picking = self.env['stock.picking'].browse(active_id)
      company = picking.company_id
      
      # Tentukan base report berdasarkan perusahaan
      if company.name == 'PT. BINA SERVICE':
          report_template = 'lww_delivery.action_report_bs_do'
      elif company.name == 'PT. SPARTADUA RIBUJAYA':
          report_template = 'lww_delivery.action_report_spartadua_do'
      else:  # Default untuk perusahaan lain
          report_template = 'lww_delivery.action_report_limawira_do'
      
      # Tambahkan suffix "_without_header" jika diperlukan
      if self.option == 'without_header':
          report_template += '_without_header'
      
      return picking.env.ref(report_template).report_action(picking)
