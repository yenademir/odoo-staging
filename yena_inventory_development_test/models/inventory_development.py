from odoo import api, fields, models
import requests
import base64
from io import BytesIO
from datetime import datetime, timedelta

class Picking(models.Model):
    _inherit = 'stock.picking'

    sale_id=fields.Many2one("sale.order",string="Sale Order")
    purchase_id=fields.Many2one("purchase.order",string="Purchase Order")
    sequence_code = fields.Char(string='Sequence Code', related='picking_type_id.sequence_code', store=True)
    logistic_company = fields.Char (string="Logistic Company", store=True)
    arrive_date = fields.Date(string="Arrive Date")
    


    
class StockMove(models.Model):
    _inherit = "stock.move"
    
    arrive_date = fields.Date(related="picking_id.arrive_date", string="Arrive Date")
    picking_type_id = fields.Many2one(related="picking_id.picking_type_id", string="Operation Type", store=True)
    related_partner = fields.Many2one(related="picking_id.partner_id", string="Receive From / Delivery Adress", store=True)
    situation = fields.Selection(related="picking_id.situation", string="Situation", store=True)
    transportation_code = fields.Char(related="picking_id.transportation_code", string="Transportation Code", store=True)
    edespatch_delivery_type = fields.Selection(related="picking_id.edespatch_delivery_type", string="Delivery Type")
    scheduled_date = fields.Datetime(related='picking_id.scheduled_date', store=True, readonly=True)
    arrival_date = fields.Date(related='picking_id.arrival_date', store=True, readonly=True)
    purchase_id=fields.Many2one(related='picking_id.purchase_id',string="Purchase Order")
    edespatch_date=fields.Datetime(related='picking_id.edespatch_date',string="Purchase Order")

    
    
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    coating = fields.Selection([
        ("hot_dip_galvanized", "Hot Dip Galvanized"),
        ("electrogalvanized", "Electrogalvanized"),
        ("centrifugal_galvanise", "Centrifugal galvanise"),
        ("electrostatic_powder_coating_red", "Electrostatic powder coating Red"),
        ("epoxy_coating", "Epoxy Coating"),
        ("uncoated", "Uncoated"),
        ("electrostatic_powder_coating_black", "Electrostatic powder coating Black"),
        ("shop_primer", "Shop Primer")
    ], string="Coating")
    material = fields.Many2many('product.yena_material', string="Material")
    min_order_qty = fields.Char(string="Min. Order Quantity")
    customer = fields.Many2one('res.partner', domain=[('is_company', '=', True)], string="Customer")
    technical_drawing = fields.Binary(string='Technical Drawing')
    technical_drawing_filename = fields.Char()
    technical_drawing_url = fields.Char(string='Technical Drawing URL', readonly=True)
    technical_drawing_revision = fields.Char(string='Technical Drawing Revision')
    technical_drawing_link = fields.Html(string='Technical Drawing Link', compute="_compute_technical_drawing_link")
    manufacturing_instructions = fields.Many2many('ir.attachment', 'manufacturing_instruction_rel', 'product_id', 'attachment_id', string='Standart Operation Procedure')
    packaging_instructions = fields.Many2many('ir.attachment', 'packaging_instruction_rel', 'product_id', 'attachment_id', string='Packaging Instructions')
    packaging_images = fields.Many2many('ir.attachment', 'packaging_image_rel', 'product_id', 'attachment_id', string='Packaging Photos')
    origin_country_id = fields.Many2one("res.country", string="Origin")
    hs_code_description = fields.Char(string="HS Code Description", store=True)
    description_sale_en = fields.Char(string="Sale Description English", store=True)


    class PackageTypes(models.Model):
        _inherit = "stock.package.type"

        gross_weight = fields.Float(string="Gross Weight")
        net_weight = fields.Float(string="Net Weight")
        stackable = fields.Boolean(string="Stackable")

    class PurchaseOrderLine(models.Model):
        _inherit = 'purchase.order.line'

        coating = fields.Selection(related="product_id.coating", string="Coating", readonly=True)
        unit_weight = fields.Float(related="product_id.weight", string="Unit Weight", readonly=True)
        product_category = fields.Many2one('product.category', related="product_id.categ_id", string="Product Category")
        product_type = fields.Selection(related='product_id.detailed_type', string='Product Type', store=True)
        totalweight = fields.Float(string="Total Weight", readonly=True, compute="_compute_total_weight")
        pricekg = fields.Float(string="KG Price", readonly=True, compute="_compute_pricekg")

        @api.depends('unit_weight', 'product_qty')
        def _compute_total_weight(self):
            for record in self:
                record.totalweight = record.unit_weight * record.product_qty

        @api.depends('price_subtotal', 'totalweight')
        def _compute_pricekg(self):
            for record in self:
                if record.totalweight != 0:
                    record.pricekg = record.price_subtotal / record.totalweight
                else:
                    record.pricekg = 0

    class SaleOrderLine(models.Model):
        _inherit = 'sale.order.line'

        product_type = fields.Selection(related='product_id.detailed_type', string='Product Type', store=True)
        product_category = fields.Many2one('product.category', related="product_id.categ_id", string="Product Category")
        totalweight = fields.Float(string='Total Weight', store=True, readonly=True)
        coating = fields.Selection(related="product_id.coating", string="Coating", readonly=True)
        pricekg = fields.Float(string='KG Price', readonly=True, store=True)
        unit_weight = fields.Float(related="product_id.weight", string="Unit Weight", readonly=True)


