from odoo import fields, models,api

class SaleNoteTemplate(models.Model):
    _name = 'yena.sale.note.template'
    _description = 'Sale Note Template'

    name = fields.Char(string="Template Name")
    customer_id = fields.Many2one('res.partner', string="Customer")
    notes = fields.Html(string="Notes")

class PurchaseNoteTemplate(models.Model):
    _name = 'yena.purchase.note.template'
    _description = 'Purchase Note Template'

    name = fields.Char(string="Template Name")
    vendor_id = fields.Many2one('res.partner', string="Vendor")
    notes = fields.Html(string="Notes")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    sale_note_template_id = fields.Many2one("yena.sale.note.template", string="Sale Quotation Note Template",
                                            domain="[('customer_id', '=', partner_id)]")

    @api.onchange('sale_note_template_id')
    def onchange_sale_note_template_id(self):
        if self.sale_note_template_id:
            self.note = self.sale_note_template_id.notes
        else:
            self.note = ""

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    purchase_note_template_id = fields.Many2one("yena.purchase.note.template", string="Purchase Note Template",
                                                domain="[('vendor_id', '=', partner_id)]")

    @api.onchange('purchase_note_template_id')
    def onchange_purchase_note_template_id(self):
        if self.purchase_note_template_id:
            self.notes = self.purchase_note_template_id.notes
        else:
            self.notes = ""
