from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    customer_reference = fields.Char(string='Müşteri Referansı', compute='_compute_customer_reference', store=True, readonly=False)

    @api.depends('move_id.invoice_origin')
    def _compute_customer_reference(self):
        for record in self:
            references = []
            # invoice_origin alanındaki her bir sipariş ismi için arama yap
            if record.move_id.invoice_origin:
                order_names = record.move_id.invoice_origin.split(', ')
                for order_name in order_names:
                    sale_order = self.env['sale.order'].search([('name', '=', order_name.strip())], limit=1)
                    if sale_order:
                        references.append(sale_order.customer_reference)
            # Benzersiz referansları set olarak sakla ve birleştir
            record.customer_reference = ', '.join(set(references))

class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_references = fields.Char(compute='_compute_customer_references', string='Müşteri Referansları')

    @api.depends('invoice_line_ids.customer_reference')
    def _compute_customer_references(self):
        for record in self:
            # Fatura satırlarındaki benzersiz müşteri referanslarını topla
            references = list(set(line.customer_reference for line in record.invoice_line_ids if line.customer_reference))
            record.customer_references = ', '.join(references)
