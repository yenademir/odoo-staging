from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    customer_reference = fields.Char(string='Müşteri Referansı', compute='_compute_customer_reference', store=True, readonly=False)

    @api.depends('sale_line_ids.order_id.customer_reference')
    def _compute_customer_reference(self):
        for record in self:
            if record.sale_line_ids:
                sale_order = record.sale_line_ids[0].order_id
                record.customer_reference = sale_order.customer_reference
            else:
                record.customer_reference = False

class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_references = fields.Char(compute='_compute_customer_references', string='Müşteri Referansları')

    @api.depends('invoice_line_ids.customer_reference')
    def _compute_customer_references(self):
        for record in self:
            references = list(set(line.customer_reference for line in record.invoice_line_ids if line.customer_reference))
            record.customer_references = ', '.join(references)
