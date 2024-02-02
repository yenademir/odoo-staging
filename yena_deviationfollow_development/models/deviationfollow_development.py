from odoo import models, fields, api

class DeviationFollowUp(models.Model):
    _name = 'deviation.followup'
    _description = 'Deviation Follow Up'

    name = fields.Char(string="Name")
    customer_id = fields.Many2one('res.partner', string='Customer')
    project_number = fields.Many2one('account.analytic.account', string='Project Number')
    product_id = fields.Many2one('product.product', string='Drawing No')
    purchase_no = fields.Many2one('purchase.order', string='Purchase No')
    question_for_customer = fields.Char(string='Question for Customer')
    subject = fields.Selection([
        ('material', 'Material'),
        ('dimension', 'Dimension'),
        ('coating', 'Coating'),
        ('packaging', 'Packaging'),
    ], string='Subject')
    remove_material_id = fields.Many2one('material.certificate', string='Remove Material')
    add_material_id = fields.Many2one('material.certificate', string='Add Material')
    approval_status = fields.Char(string='Approval Status')
    customer_approve_reject_date = fields.Date(string='Customer Approve/Reject Date')
    approver_id = fields.Many2one('res.partner', string='Approver')
    subject_of_mail = fields.Char(string='Subject of Mail')
    note = fields.Html(string='Note')
    contact_user = fields.Many2one('res.users', string='Contact')
    wizard_id = fields.Many2one('document.upload.wizard', string='Related Wizard')

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            material_ids = self.product_id.product_tmpl_id.material_certificate.ids
            return {
                'domain': {'remove_material_id': [('id', 'in', material_ids)]}
            }
        else:
            return {
                'domain': {'remove_material_id': []}
            }

    @api.model
    def create(self, vals):
        # Diğer kodlarınız...
        record = super(DeviationFollowUp, self).create(vals)
        self._update_document_upload_wizard_line(record)
        return record

    def write(self, vals):
        # Diğer kodlarınız...
        res = super(DeviationFollowUp, self).write(vals)
        for record in self:
            self._update_document_upload_wizard_line(record)
        return res

    def _update_document_upload_wizard_line(self, record):
        if record.subject == 'material':
            if record.wizard_id:
                document_wizard_lines = self.env['document.upload.wizard.line'].search([
                    ('wizard_id', '=', record.wizard_id.id),
                    ('material_certificate_id', '=', record.remove_material_id.id)
                ])
                for line in document_wizard_lines:
                    line.write({'uploaded_document': 'SAPMA VAR'})

                if record.add_material_id:
                    material_name = record.add_material_id.name  
                    self.env['document.upload.wizard.line'].create({
                        'wizard_id': record.wizard_id.id,
                        'material_certificate_id': record.add_material_id.id,
                        'required_document': material_name, 
                    })

        elif record.subject == 'dimension':
            if record.wizard_id:
                measurement_reports = self.env['document.upload.wizard.measurement.report'].search([
                    ('wizard_id', '=', record.wizard_id.id),
                    ('name', '=', 'Ölçü Boyut Kontrol')
                ])
                for report in measurement_reports:
                    report.write({'uploaded_document': 'SAPMA VAR'})
        
        elif record.subject == 'coating':
            if record.wizard_id:
                galvanize = self.env['document.upload.wizard.galvanize'].search([
                    ('wizard_id', '=', record.wizard_id.id),
                    ('name', '=', 'Galvanizing / Painting / Coating')
                ])
                for report in galvanize:
                    report.write({'uploaded_document': 'SAPMA VAR'})

        elif record.subject == 'packaging':
            if record.wizard_id:
                packaging = self.env['document.upload.wizard.packaging'].search([
                    ('wizard_id', '=', record.wizard_id.id),
                    ('name', '=', 'Paketleme')
                ])
                for report in packaging:
                    report.write({'uploaded_document': 'SAPMA VAR'})

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    wizard_id = fields.Many2one('document.upload.wizard', string='Related Wizard')

    def create_deviation_follow_up(self):
        self.ensure_one()  
        deviation_model = self.env['deviation.followup']

        new_deviation = deviation_model.create({
            'customer_id': self.account_analytic_id.partner_id.id,
            'project_number': self.account_analytic_id.id,
            'product_id': self.product_id.id,
            'purchase_no': self.order_id.id,
            'wizard_id': self.wizard_id.id if self.wizard_id else False,
        })
        return {
            'type': 'ir.actions.act_window',
            'name': 'Deviation Follow Up',
            'res_model': 'deviation.followup',
            'view_mode': 'form',
            'res_id': new_deviation.id,  
        }

class ProductProduct(models.Model):
    _inherit = 'product.template'

    deviation_followup_ids = fields.One2many(
        'deviation.followup', 'product_id', string='Deviation Follow Ups'
    )
