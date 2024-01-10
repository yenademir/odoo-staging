from odoo import api, fields, models

class PurchaseOrderLinePriceHistory(models.TransientModel):
    _name = "purchase.order.line.price.history"
    _description = "Purchase order line price history"

    @api.model
    def _default_partner_id(self):
        return (
            self.env["purchase.order.line"]
            .browse(self.env.context.get("active_id"))
            .partner_id.id
        )

    purchase_order_line_id = fields.Many2one(
        comodel_name="purchase.order.line",
        string="Purchase order line",
        default=lambda self: self.env.context.get("active_id"),
    )
    product_id = fields.Many2one(related="purchase_order_line_id.product_id")
    partner_id = fields.Many2one(
        comodel_name="res.partner",
        string="Supplier",
        default=_default_partner_id,
    )
    line_ids = fields.One2many(
        comodel_name="purchase.order.line.price.history.line",
        inverse_name="history_id",
        string="History lines",
        
        readonly=True,
    )
    include_rfq = fields.Boolean(
        string="Include RFQ",
        help="Include 'Requests for Quotation' lines in the purchase history",
        default=True,

    )
    include_cancelled=fields.Boolean(string= "Include Cancelleds", default=True)

    include_commercial_partner = fields.Boolean(
        string="Include commercial entity",
        default=True,
        help="Include commercial entity and its contacts in the purchase history",
    )

    @api.onchange("partner_id", "include_rfq", "include_commercial_partner", "include_cancelled")
    def _onchange_partner_id(self):
        self.line_ids = False
        states = ["purchase", "done"]
        if self.include_rfq:
            states += ["draft", "sent", "to approve"]
        domain = [
            ("product_id", "=", self.product_id.id),
            ("order_id.state", "in", states),
        ]
        if self.include_cancelled:
            states += ["cancel"]
        if self.partner_id:
            if self.include_commercial_partner:
                commercial_ids = self.partner_id.commercial_partner_id.ids
                domain += [("partner_id", "child_of", commercial_ids)]
            else:
                domain += [("partner_id", "child_of", self.partner_id.ids)]
       
        order_lines = self.env["purchase.order.line"].search(domain)
        
        vals = [
            (0, False, {"purchase_order_line_id": order_line.id})
            for order_line in order_lines
        ]
        self.line_ids = vals


class PurchaseOrderLinePriceHistoryLine(models.TransientModel):
    _name = "purchase.order.line.price.history.line"
    _description = "Purchase order line price history line"
    cancelled = fields.Boolean(string="Cancelled")
    cancel_reason = fields.Text(string="Cancel Reason")
    state=fields.Selection(string="Status", readonly=True , related="order_id.state")


    blanket_order_line = fields.Many2one(
        comodel_name="purchase.blanket.order.line",
        related="purchase_order_line_id.blanket_order_line",
        string="Blanket Order Line",
        readonly=True,
    )

    history_id = fields.Many2one(
        comodel_name="purchase.order.line.price.history",
        string="History",
    )
    purchase_order_line_id = fields.Many2one(
        comodel_name="purchase.order.line",
        string="Purchase order line",
    )
    order_id = fields.Many2one(related="purchase_order_line_id.order_id")
    partner_id = fields.Many2one(related="purchase_order_line_id.partner_id")
    purchase_order_date_order = fields.Datetime(
        related="purchase_order_line_id.order_id.date_order",
    )
    product_qty = fields.Float(related="purchase_order_line_id.product_qty")
    product_uom = fields.Many2one(related="purchase_order_line_id.product_uom")
    price_unit = fields.Float(related="purchase_order_line_id.price_unit")

    def _prepare_purchase_order_line_vals(self):
        self.ensure_one()
        return {"price_unit": self.price_unit}

    def action_set_price(self):
        self.ensure_one()
        active_id = self.env.context.get("active_id")
        order_line = self.env["purchase.order.line"].browse(active_id)
        vals = self._prepare_purchase_order_line_vals()
        order_line.write(vals)
