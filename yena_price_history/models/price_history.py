from odoo import models, fields,api

class SalePriceHistory(models.Model):
    _name = 'sale.price.history'
    _description = 'Sale Price History'

    product_id = fields.Many2one('product.product', string='Product')
    partner_id = fields.Many2one('res.partner', string='Customer')
    price = fields.Float(string='Price')
    date = fields.Date(string='Date')
    status = fields.Selection([
        ('draft', 'Quotation'),
        ('sent', 'Quotation Sent'),
        ('sale', 'Sales Order'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status')

class PurchasePriceHistory(models.Model):
    _name = 'purchase.price.history'
    _description = 'Purchase Price History'

    product_id = fields.Many2one('product.product', string='Product')
    partner_id = fields.Many2one('res.partner', string='Supplier')
    price = fields.Float(string='Price')
    date = fields.Date(string='Date')
    status = fields.Selection([
        ('draft', 'RFQ'),
        ('sent', 'RFQ Sent'),
        ('purchase', 'Purchase Order'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status')
    
class ProductTemplate(models.Model):
    _inherit = 'product.template'

    sale_price_history_ids = fields.One2many(
        comodel_name='sale.price.history',
        inverse_name='product_id',
        string='Sale History Lines'
    )
    purchase_price_history_ids = fields.One2many(
        comodel_name='purchase.price.history',
        inverse_name='product_id',
        string='Purchase History Lines',
 
    )
    
    def action_compute_price_history(self):
        for template in self:
            # Ürün şablonu ile ilişkilendirilmiş ürünleri bul
            product_ids = self.env['product.product'].search([('product_tmpl_id', '=', template.id)])
            for product in product_ids:
                # Satış sipariş satırlarını ara
                sale_order_lines = self.env['sale.order.line'].search([('product_id', '=', product.id)])
                for line in sale_order_lines:
                    history_vals = {
                        'product_id': product.id,
                        'partner_id': line.order_id.partner_id.id,
                        'price': line.price_unit,
                        'date': line.order_id.date_order.date(),  # date_order datetime ise, date'e çevir
                        'status': line.order_id.state,
                    }
                    # Benzersizlik koşuluna göre mevcut geçmiş kaydını kontrol et
                    existing_history = self.env['sale.price.history'].search([
                        ('product_id', '=', product.id),
                        ('partner_id', '=', line.order_id.partner_id.id),
                        ('date', '=', history_vals['date']),
                    ], limit=1)
                    if existing_history:
                        existing_history.write(history_vals)
                    else:
                        self.env['sale.price.history'].create(history_vals)

                # Satın alma sipariş satırlarını ara
                purchase_order_lines = self.env['purchase.order.line'].search([('product_id', '=', product.id)])
                for line in purchase_order_lines:
                    history_vals = {
                        'product_id': product.id,
                        'partner_id': line.order_id.partner_id.id,
                        'price': line.price_unit,
                        'date': line.order_id.date_order.date(),  # date_order datetime ise, date'e çevir
                        'status': line.order_id.state,
                    }
                    # Benzersizlik koşuluna göre mevcut geçmiş kaydını kontrol et
                    existing_history = self.env['purchase.price.history'].search([
                        ('product_id', '=', product.id),
                        ('partner_id', '=', line.order_id.partner_id.id),
                        ('date', '=', history_vals['date']),
                    ], limit=1)
                    if existing_history:
                        existing_history.write(history_vals)
                    else:
                        self.env['purchase.price.history'].create(history_vals)
