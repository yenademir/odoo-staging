from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    customer_reference = fields.Char(string='Müşteri Referansı', compute='_compute_customer_reference', store=True, readonly=False)

    @api.depends('sale_line_ids.order_id')
    def _compute_customer_reference(self):
        for record in self:
            if record.sale_line_ids:
                # Fatura satırı ile ilişkili ilk satış siparişi satırını al
                sale_order_line = record.sale_line_ids[0]
                record.customer_reference = sale_order_line.order_id.customer_reference
            else:
                record.customer_reference = False

class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_references = fields.Char(compute='_compute_customer_references', string='Müşteri Referansları')

    @api.depends('invoice_line_ids.customer_reference')
    def _compute_customer_references(self):
        for record in self:
            # Farklı customer_reference değerlerini al
            references = list(set(line.customer_reference for line in record.invoice_line_ids if line.customer_reference))
            record.customer_references = ', '.join(references)
