from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    customer_reference = fields.Char(string='Müşteri Referansı', compute='_compute_customer_reference', store=True, readonly=False)

    @api.depends('sale_line_ids.order_id.customer_reference')
    def _compute_customer_reference(self):
        for record in self:
            # Her fatura satırı için ilgili satış siparişi satırına bak
            if record.sale_line_ids:
                sale_order = record.sale_line_ids.order_id
                record.customer_reference = sale_order.customer_reference if sale_order else False
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
