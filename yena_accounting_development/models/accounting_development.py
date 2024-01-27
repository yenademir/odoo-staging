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
            references = record.invoice_line_ids.mapped('customer_reference')
            # Flatten the list of lists into a single list of references
            flattened_references = [item for sublist in references for item in (sublist if isinstance(sublist, list) else [sublist])]
            # Filter out any non-string items and ensure uniqueness
            unique_references = set(filter(lambda x: isinstance(x, str), flattened_references))
            # Join the unique string references with a comma
            record.customer_references = ','.join(unique_references)

