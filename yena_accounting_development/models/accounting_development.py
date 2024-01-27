from odoo import models, fields, api

class AccountMoveLineInherit(models.Model):
    _inherit = 'account.move.line'

    customer_reference = fields.Char(string='Customer Reference')

    @api.model
    def create(self, vals):
        if 'sale_line_ids' in vals and vals['sale_line_ids']:
            sale_line = self.env['sale.order.line'].browse(vals['sale_line_ids'][0])
            vals['customer_reference'] = sale_line.order_id.customer_reference
        return super(AccountMoveLineInherit, self).create(vals)

class AccountMoveInherit(models.Model):
    _inherit = 'account.move'

    customer_references = fields.Char(string='Customer References', compute='_compute_customer_references', store=True)

    @api.depends('invoice_line_ids.customer_reference')
    def _compute_customer_references(self):
        for record in self:
            # customer_reference alanı boş olmayanları filtrele
            references = record.invoice_line_ids.filtered(lambda r: r.customer_reference).mapped('customer_reference')
            # references listesindeki öğelerin string türünde olduğundan emin ol
            references = [ref for ref in references if isinstance(ref, str)]
            # Benzersiz string değerleri virgülle birleştir
            record.customer_references = ','.join(set(references))
