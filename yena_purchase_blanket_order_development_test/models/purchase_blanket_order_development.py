from odoo import models, fields, api

class PurchaseBlanketOrder(models.Model):
    _inherit = 'purchase.blanket.order'


    invoiced_total = fields.Monetary(compute='_compute_totals', store=True, string='Invoiced Total')
    ordered_total = fields.Monetary(compute='_compute_totals', store=True, string='Ordered Total')
    remaining_invoice_total = fields.Monetary(compute='_compute_totals', store=True, string='Remaining to Invoice Total')
    remaining_total = fields.Monetary(compute='_compute_totals', store=True, string='Remaining Total')
    line_ids = fields.One2many('purchase.blanket.order.line', 'order_id', string='Order Lines')
    purchase_order_ids = fields.One2many('purchase.order', 'blanket_order_id', string='Purchase Orders')
    project_purchase_blanket_order = fields.Many2many(
        comodel_name='project.project',
        string='Project Numbers',
        compute='_compute_project_purchase_blanket_order'
    )

    @api.depends('purchase_order_ids')
    def _compute_project_purchase_blanket_order(self):
        for record in self:
            project_purchases = self.env['project.project']
            for purchase in record.purchase_order_ids:
                if purchase.project_purchase:
                    project_purchases |= purchase.project_purchase
            record.project_purchase_blanket_order = project_purchases

    @api.depends('line_ids.invoiced_subtotal', 'line_ids.ordered_subtotal', 'line_ids.remaining_invoice_subtotal', 'line_ids.remaining_subtotal','amount_untaxed')
    def _compute_totals(self):
        for order in self:
            order.invoiced_total = sum(line.invoiced_subtotal for line in order.line_ids)
            order.ordered_total = sum(line.ordered_subtotal for line in order.line_ids)
            order.remaining_invoice_total = sum(line.remaining_invoice_subtotal for line in order.line_ids)
            order.remaining_total = sum(line.remaining_subtotal for line in order.line_ids)
            if order.ordered_total > 0 and order.amount_untaxed > 0 and order.ordered_total == order.amount_untaxed:
                order.state = 'done'

class PurchaseBlanketOrderLine(models.Model):
    _inherit = 'purchase.blanket.order.line'

    order_id = fields.Many2one('purchase.blanket.order', string='Order Reference', required=True, ondelete='cascade', index=True, copy=False)
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')
    invoiced_subtotal = fields.Monetary(compute='_compute_subtotals', string='Invoiced Subtotal')
    ordered_subtotal = fields.Monetary(compute='_compute_subtotals', string='Ordered Subtotal')
    remaining_invoice_subtotal = fields.Monetary(compute='_compute_subtotals', string='Remaining Invoice Subtotal')
    remaining_subtotal = fields.Monetary(compute='_compute_subtotals', string='Remaining Subtotal')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('done', 'Done'),
        ('expired', 'Expired'),
    ], string='State', related='order_id.state', store=True, readonly=True)
    project_purchase_blanket_order_line = fields.Many2many(
        'project.project',
        'blanket_order_line_project_rel',
        'blanket_order_line_id',
        'project_id',
        string='Project Number',
        compute='_compute_project_purchase_blanket_order_line'
    )
    partner_ref = fields.Char(string='Vendor Reference', related='order_id.partner_ref', store=True, readonly=True)
    project_purchase_name = fields.Char(string='Project Number', compute='_compute_project_purchase_name', store=True, index=True)

    @api.depends('order_id.project_purchase_blanket_order')
    def _compute_project_purchase_blanket_order_line(self):
        for line in self:
            line.project_purchase_blanket_order_line = line.order_id.project_purchase_blanket_order

    @api.depends('project_purchase_blanket_order_line')
    def _compute_project_purchase_name(self):
        for line in self:
            project_names = ', '.join(line.project_purchase_blanket_order_line.mapped('name'))
            line.project_purchase_name = project_names

    @api.depends('invoiced_uom_qty', 'ordered_uom_qty', 'original_uom_qty', 'price_unit')
    def _compute_subtotals(self):
        for line in self:
            line.invoiced_subtotal = line.invoiced_uom_qty * line.price_unit
            line.ordered_subtotal = line.ordered_uom_qty * line.price_unit
            line.remaining_invoice_subtotal = (line.original_uom_qty - line.invoiced_uom_qty) * line.price_unit
            line.remaining_subtotal = (line.original_uom_qty - line.ordered_uom_qty) * line.price_unit
            
