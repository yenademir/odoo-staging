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

    def print_customer_references(self):
        # account.move.line kayıtlarını çek
        move_lines = self.line_ids

        # customer reference'ları bir set içinde topla
        customer_refs = set(line.customer_reference for line in move_lines if line.customer_reference)

        # Benzersiz customer reference'ları formatlayıp döndür
        return ', '.join(sorted(customer_refs))
