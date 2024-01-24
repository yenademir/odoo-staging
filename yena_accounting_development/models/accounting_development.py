from odoo import api, fields, models

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    customer_reference = fields.Char(string='Customer Reference', compute='_compute_customer_reference', store=True, readonly=False)

    @api.depends('move_id.invoice_origin')
    def _compute_customer_reference(self):
        for record in self:
            sale_order = self.env['sale.order'].search([('name', '=', record.move_id.invoice_origin)], limit=1)
            if sale_order:
                record.customer_reference = sale_order.customer_reference
            else:
                record.customer_reference = False
                
class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_references = fields.Char(compute='_compute_customer_references')

    def _compute_customer_references(self):
        for record in self:
            move_lines = record.line_ids
            # customer_reference'ları sayısal olarak sırala
            customer_refs = set(line.customer_reference for line in move_lines if line.customer_reference)
            # Sayısal olarak sıralamak için önce int'e çevir
            customer_refs = sorted(customer_refs, key=lambda x: int(x))
            record.customer_references = ', '.join(customer_refs)


