from odoo import fields, models,api

class NoteTemplates(models.Model):
    _name='yena.note_templates'

    name=fields.Char(string="Template Name")
    customer=fields.Many2one('res.partner',string="Customer")
    notes=fields.Html(string="Notes")
    vendor=fields.Many2one('res.partner',string="Vendors")

class SaleOrder(models.Model):
    _inherit='sale.order'

    note_templates=fields.Many2one("yena.note_templates",string="Sale Quotation Note Template", domain="[('customer', '=', partner_id)]")

    @api.onchange('note_templates')
    def onchange_note_templates(self):
        if self.note_templates:
            self.note = self.note_templates.notes
        else:
            self.note = ""

class PurchaseOrder(models.Model):
    _inherit='purchase.order'

    note_templates=fields.Many2one("yena.note_templates",string="Purchase Note Template", domain="[('vendor', '=', partner_id)]")

    @api.onchange('note_templates')
    def onchange_note_templates(self):
        if self.note_templates:
            self.notes = self.note_templates.notes
        else:
            self.notes = ""