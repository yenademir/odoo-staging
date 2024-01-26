from odoo import models, fields, api

class ProjectCompareLine(models.Model):
    _name = 'project.compare.line'
    _description = 'Project Order Comparison Line'

    project_id = fields.Many2one('project.project', string='Project')
    product_id = fields.Many2one('product.product', string='Product')
    sale_qty = fields.Float(string='Sale Quantity')
    purchase_qty = fields.Float(string='Purchase Quantity')
    sale_weight = fields.Float(string='Sale Weight (kg)')
    purchase_weight = fields.Float(string='Purchase Weight (kg)')
    # sale_order_id = fields.Many2one('sale.order', string='Sale Order')
    # purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order')

class Project(models.Model):
    _inherit = 'project.project'

    comparison_lines = fields.One2many(
        comodel_name='project.compare.line', 
        inverse_name='project_id', 
        string='Order Comparison Lines'
    )

    def compare_orders(self):
        self.ensure_one()
        # Projeye bağlı satış siparişlerini arama
        sale_orders = self.env['sale.order'].search([('project_sales', '=', self.id),
                                                     ('state', 'in', ['sale', 'done'])])
        # Projeye bağlı satın alma siparişlerini arama
        purchase_orders = self.env['purchase.order'].search([('project_purchase', '=', self.id),
                                                             ('state', 'in', ['purchase', 'done'])])
        existing_lines = {line.product_id.id: line for line in self.comparison_lines}

        # Ürün verilerini toplamak için bir sözlük oluşturma
        product_data = {}

        # Satış siparişlerindeki ürünlerin miktar ve ağırlıklarını toplama
        for order in sale_orders:
            for line in order.order_line:
                product = line.product_id
                if product.detailed_type == 'product':
                    key = product.id
                    if key not in product_data:
                        product_data[key] = {'sale_qty': 0, 'purchase_qty': 0, 'sale_weight': 0, 'purchase_weight': 0}
                    product_data[key]['sale_qty'] += line.product_uom_qty
                    product_data[key]['sale_weight'] += line.product_uom_qty * product.weight

        # Satın alma siparişlerindeki ürünlerin miktar ve ağırlıklarını toplama
        for order in purchase_orders:
            for line in order.order_line:
                product = line.product_id
                if product.detailed_type == 'product':
                    key = product.id
                    if key not in product_data:
                        product_data[key] = {'sale_qty': 0, 'purchase_qty': 0, 'sale_weight': 0, 'purchase_weight': 0}
                    product_data[key]['purchase_qty'] += line.product_qty
                    product_data[key]['purchase_weight'] += line.product_qty * product.weight

        comparison_lines = []
        existing_line_ids = []
        for product_id, data in product_data.items():
            qty_difference = data['sale_qty'] - data['purchase_qty']
            if qty_difference == 0:
                # Miktarlar eşitse ve ürün zaten listedeyse, o ürünü listeden kaldır
                if product_id in existing_lines:
                    existing_lines[product_id].unlink()
                continue  # Miktarlar eşitse bu ürünü atla

            if product_id in existing_lines:
                # Ürün zaten listedeyse, bilgileri güncelle
                existing_lines[product_id].write({
                    'sale_qty': data['sale_qty'],
                    'purchase_qty': data['purchase_qty'],
                    'sale_weight': data['sale_weight'],
                    'purchase_weight': data['purchase_weight'],
                })
                existing_line_ids.append(existing_lines[product_id].id)
            else:
                # Yeni ürünü listeye ekle
                line = self.env['project.compare.line'].create({
                    'project_id': self.id,
                    'product_id': product_id,
                    'sale_qty': data['sale_qty'],
                    'purchase_qty': data['purchase_qty'],
                    'sale_weight': data['sale_weight'],
                    'purchase_weight': data['purchase_weight'],
                })
                existing_line_ids.append(line.id)
        self.comparison_lines = [(6, 0, existing_line_ids)]      

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    project_id = fields.Many2one(
        'project.project', 
        string='Project',
        help='Select a project for this purchase order.'
    )
    @api.model
    def create(self, vals):
        # Satın alma siparişi oluştur
        record = super(PurchaseOrder, self).create(vals)
        # İlgili proje için karşılaştırma işlemini çağır
        project = record.project_purchase
        if project:
            project.compare_orders()
        return record

    def write(self, vals):
        # Satın alma siparişini güncelle
        result = super(PurchaseOrder, self).write(vals)
        # İlgili proje için karşılaştırma işlemini çağır
        for record in self:
            project = record.project_purchase
            if project:
                project.compare_orders()
        return result
    
class SaleOrder(models.Model):
    _inherit='sale.order'

    @api.model
    def create(self, vals):
        record = super(SaleOrder, self).create(vals)
        project = record.project_sales
        if project:
            project.compare_orders()
        return record

    def write(self, vals):
        result = super(SaleOrder, self).write(vals)
        for record in self:
            project = record.project_sales
            if project:
                project.compare_orders()
        return result