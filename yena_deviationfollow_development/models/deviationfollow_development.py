from odoo import models, fields, api

class DeviationFollowUp(models.Model):
    _name = 'deviation.followup'
    _description = 'Deviation Follow Up'

    name = fields.Char(string="Name")
    customer_id = fields.Many2one('res.partner', string='Customer')
    project_number = fields.Many2one('project.project', string='Project Number')
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
    approval_status = fields.Selection([
        ('ok', 'OK'),
        ('not_ok', 'NOT OK'),
        ('conditionally_ok', 'CONDITIONALLY OK'),
    ], string='Approval Status')
    customer_approve_reject_date = fields.Date(string='Customer Approve/Reject Date')
    approver_id = fields.Many2one('res.partner', string='Approver')
    subject_of_mail = fields.Char(string='Subject of Mail')
    note = fields.Html(string='Note')
    contact_user = fields.Many2one('res.users', string='Contact')
    wizard_id = fields.Many2one('document.upload.wizard', string='Related Wizard')

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
