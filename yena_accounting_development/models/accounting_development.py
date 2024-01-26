from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    customer_reference = fields.Char(string='Müşteri Referansı')

    @api.model
    def create(self, vals):
        # Yeni bir account.move.line kaydı oluşturulurken, ilişkili sale.order'dan customer_reference al
        record = super(AccountMoveLine, self).create(vals)
        if record.move_id.invoice_origin:
            order_name = record.move_id.invoice_origin.split(', ')[0].strip()
            sale_order = self.env['sale.order'].search([('name', '=', order_name)], limit=1)
            if sale_order:
                record.customer_reference = sale_order.customer_reference
        return record

class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_references = fields.Char(compute='_compute_customer_references', string='Müşteri Referansları')

    @api.depends('invoice_line_ids.customer_reference')
    def _compute_customer_references(self):
        for record in self:
            references = list(set(line.customer_reference for line in record.invoice_line_ids if line.customer_reference))
            record.customer_references = ', '.join(references)
