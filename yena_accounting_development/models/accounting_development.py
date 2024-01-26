from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    customer_reference = fields.Char(string='Müşteri Referansı', compute='_compute_customer_reference', store=True, readonly=False)

    @api.depends('move_id.invoice_origin')
    def _compute_customer_reference(self):
        for record in self:
            if record.move_id.invoice_origin:
                # Faturanın kökenini kullanarak ilgili satış siparişini bul
                sale_order = self.env['sale.order'].search([('name', '=', record.move_id.invoice_origin)], limit=1)
                if sale_order:
                    record.customer_reference = sale_order.customer_reference
                else:
                    record.customer_reference = False
            else:
                record.customer_reference = False

class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_references = fields.Char(compute='_compute_customer_references', string='Müşteri Referansları')

    @api.depends('invoice_line_ids.customer_reference')
    def _compute_customer_references(self):
        for record in self:
            # Fatura satırlarındaki benzersiz müşteri referanslarını topla
            references = set()
            for line in record.invoice_line_ids:
                if line.customer_reference:
                    references.add(line.customer_reference)
            record.customer_references = ', '.join(references)
