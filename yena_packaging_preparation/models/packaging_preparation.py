from odoo import models, fields, api
import requests
import base64
from io import BytesIO
from datetime import datetime

class PackagingPreparation(models.Model):
    _name = 'packaging.preparation'
    _description = 'Packaging Preparation'

    name = fields.Char('Name')
    batch_id = fields.Many2one('stock.picking.batch', string='Batch Reference')
    customer_reference = fields.Char('Customer Reference')
    product_id = fields.Many2one('product.product', string='Product')
    description = fields.Text('Description')
    origin = fields.Char('Origin')
    package_quantity = fields.Float('Quantity')
    unit_of_measure = fields.Many2one('uom.uom', string='Unit of Measure')
    unit_net_weight = fields.Float('Unit Net Weight')
    total_net_weight = fields.Float('Total Net Weight')
    gross_weight = fields.Float('Gross Weight')
    total_gross_weight = fields.Float('Total Gross Weight')
    package_no = fields.Char('Package Number')
    width = fields.Float('Width')
    length = fields.Float('Length')
    height = fields.Float('Height')
    stackable = fields.Boolean('Stackable')
    pallet_no = fields.Integer('Pallet Number')
    purchase_order_line_id = fields.Many2one('purchase.order.line', string="Purchase Order Line")

    @api.onchange('gross_weight')
    def _onchange_gross_weight(self):
        for record in self:
            record.total_gross_weight = record.gross_weight + record.total_net_weight

class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'

    packaging_preparation_ids = fields.One2many(
        comodel_name='packaging.preparation',
        inverse_name='batch_id',
        string='Packaging Preparations'
    )

    def delete_packaging_preparations(self):
        for batch in self:
            preparations_to_delete = batch.packaging_preparation_ids
            preparations_to_delete.unlink()

    def create_packaging_preparations(self):
        PackagingPreparation = self.env['packaging.preparation']
        for batch in self:
            pallet_no = 1
            no_package_data = []  # Paket bilgisi olmayan kayıtlar için geçici liste

            for line in batch.move_line_ids:
                purchase_order_line = line.move_id.purchase_line_id
                if line.package_quantity <= 0 or line.package_quantity is False:
                    # Transfer edilen toplam adeti kullanarak tek bir kayıt oluştur
                    vals = {
                            'name': line.product_id.name,
                            'batch_id': batch.id,
                            'customer_reference': line.customer_reference,
                            'product_id': line.product_id.id,
                            'package_quantity': line.qty_done,
                            'description': line.product_id.description_sale,
                            'origin' : line.product_id.origin_country_id.name,
                            'unit_of_measure': line.product_uom_id.id,
                            'unit_net_weight': line.product_id.weight, 
                            'total_net_weight': line.product_id.weight * line.qty_done,
                            'package_no': 1,
                            'width': line.width,
                            'length': line.length,
                            'height': line.height,
                            'stackable': line.stackable,
                            'pallet_no': pallet_no,
                            'purchase_order_line_id': purchase_order_line.id if purchase_order_line else False,
                        }
                    no_package_data.append(vals)

                else:
                    # Tam paketler ve kalan miktar için kayıtlar oluştur
                    full_packages = int(line.qty_done / line.package_quantity)
                    for _ in range(full_packages):
                        vals = {
                            'name': line.product_id.name,
                            'batch_id': batch.id,
                            'customer_reference': line.customer_reference,
                            'product_id': line.product_id.id,
                            'package_quantity': line.package_quantity,
                            'description': line.product_id.description_sale,
                            'origin' : line.product_id.origin_country_id.name,
                            'unit_of_measure': line.product_uom_id.id,
                            'unit_net_weight': line.product_id.weight, 
                            'total_net_weight': line.product_id.weight * line.package_quantity,
                            'package_no': 1,
                            'width': line.width,
                            'length': line.length,
                            'height': line.height,
                            'stackable': line.stackable,
                            'pallet_no': pallet_no,
                            'purchase_order_line_id': purchase_order_line.id if purchase_order_line else False,
                        }
                        PackagingPreparation.create(vals)
                        pallet_no += 1

                    remaining_qty = line.qty_done % line.package_quantity
                    if remaining_qty > 0:
                        vals = {
                            'name': line.product_id.name,
                            'batch_id': batch.id,
                            'customer_reference': line.customer_reference,
                            'product_id': line.product_id.id,
                            'package_quantity': remaining_qty,
                            'description': line.product_id.description_sale,
                            'origin' : line.product_id.origin_country_id.name,
                            'unit_of_measure': line.product_uom_id.id,
                            'unit_net_weight': line.product_id.weight, 
                            'total_net_weight': line.product_id.weight * line.package_quantity,
                            'package_no': 1,
                            'width': line.width,
                            'length': line.length,
                            'height': line.height,
                            'stackable': line.stackable,
                            'pallet_no': pallet_no,
                            'purchase_order_line_id': purchase_order_line.id if purchase_order_line else False,
                        }
                        PackagingPreparation.create(vals)
                        pallet_no += 1

            for vals in no_package_data:
                PackagingPreparation.create(vals)
                pallet_no += 1

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    package_quantity = fields.Float(
        string='Package Quantity',
        related='product_id.packaging_ids.qty',
        store=True,
        readonly=True 
    )
    length = fields.Integer(
        string='Length',
        related='product_id.packaging_ids.length',
        store=True,
        readonly=True
    )
    width = fields.Integer(
        string='Width',
        related='product_id.packaging_ids.width',
        store=True,
        readonly=True
    )
    height = fields.Integer(
        string='Height',
        related='product_id.packaging_ids.height',
        store=True,
        readonly=True
    )
    stackable = fields.Boolean(
        string='Stackable',
        related='product_id.packaging_ids.stackable',
        store=True,
        readonly=True
    )
    customer_reference = fields.Char(
        string='Customer Reference',
        related='picking_id.purchase_id.customer_reference',
        store=True,
        readonly=True
    )

class PackagingType(models.Model):
    _name = 'type.packaging'
    _description = 'Type of Packaging'

    name = fields.Char(string='Name')

class ProductPackaging(models.Model):
    _inherit = 'product.packaging'

    length = fields.Integer('Length')
    width = fields.Integer('Width')
    height = fields.Integer('Height')
    stackable = fields.Boolean('Stackable')
    gross_weight = fields.Float('Gross Weight')
    type = fields.Many2one('type.packaging', string='Type')

class PackagingPreparationReportXlsx(models.AbstractModel):
    _name = 'report.yena_packaging_preparation.report_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    def generate_xlsx_report(self, workbook, data, batches):
        centered_format = workbook.add_format({
            'align': 'center', 
            'valign': 'vcenter', 
            'size': 13,
            'border': 1,
            })
        centered_format_bg = workbook.add_format({
            'align': 'center', 
            'valign': 'vcenter', 
            'size': 13,
            'bg_color': '#ededed',
            'border': 1,
            })
        merge_format18 = workbook.add_format({
            'text_wrap': True,
            'align': 'left',
            'valign': 'vcenter',
            'bold': True,
            'size': 18
        })
        merge_format14left = workbook.add_format({
            'text_wrap': True,
            'align': 'left',
            'valign': 'vcenter',
            'bold': True,
            'size': 14,
            'bg_color': '#ededed',
            'border': 1,
        })
        merge_format14 = workbook.add_format({
            'align': 'center',
            'valign': 'vbottom',
            'bold': True,
            'size': 14
        })
        merge_format10 = workbook.add_format({
            'size': 10
        })
        header_format = workbook.add_format({
            'bg_color': '#d9d9d9',
            'border': 1,
            'align': 'center',
            'valign': 'vcenter',
            'text_wrap': True,  # Metni sarmalar
            'bold': True,  # Metni kalın yapar
        })

        for batch in batches:
            sheet = workbook.add_worksheet('ALL')

            # PO(s) # için müşteri referanslarını topla
            customer_references = set(line.customer_reference for line in batch.move_line_ids if line.customer_reference)
            po_text = 'PO(s) # ' + ', '.join(customer_references)

            # Project No(s) # için proje numaralarını topla
            project_nos = set(project.name for project in batch.project_ids)
            project_text = 'Project No(s) # ' + ', '.join(project_nos)

            transportation_code = batch.transportation_code if batch.transportation_code else ''
            despatch_date = batch.edespatch_date if batch.edespatch_date else ''
            
            # Tarih formatını ayarla (eğer despatch_date varsa)
            if despatch_date:
                despatch_date = datetime.strftime(despatch_date, '%Y-%m-%d')

            shipment_info_text = f'Shipment Number: {transportation_code} / Shipment Date: {despatch_date}'

            # Sütun genişliklerini ayarla
            column_widths = [6, 9, 25, 25, 15.5, 10, 6.50, 16, 23, 16.5, 17.5, 24, 12.5, 12.5, 12.5, 13.5, 12]
            for i, width in enumerate(column_widths):
                sheet.set_column(i, i, width)

            url = 'https://yenastorage.blob.core.windows.net/odoo-container/YENA_logo.png'
            response = requests.get(url)
            if response.status_code == 200:
                image_data = BytesIO(response.content)
                sheet.insert_image('A1:D8', 'YENA_logo.png', {'image_data': image_data, 'x_scale': 0.3, 'y_scale': 0.3})

            
            # İlk 9 satırı ve A - E hücrelerini birleştir
            sheet.merge_range('A1:C9', 'PACKING LIST', merge_format14)
            sheet.merge_range('A10:D10', po_text, merge_format14left)
            sheet.merge_range('A11:D11', project_text, merge_format14left)
            sheet.merge_range('A12:D12', shipment_info_text, merge_format14left)
            sheet.merge_range('F1:I1', 'İRSALİYE NO / WAY BILL NO :', merge_format10)
            sheet.merge_range('F2:I2', 'İHRACATÇI /SHIPPER:', merge_format10)
            sheet.merge_range('F3:I9', 'YENA DEMİR ÇELİK SAN. TİC.LTD.ŞTİ.\nOsmanağa Mah. Rıhtım Caddesi\nNo:8/5 34714 \nKadıköy/İstanbul', merge_format18)
            sheet.merge_range('F10:I10', 'ÜRÜN MENŞEE : TÜRKİYE ORIGIN OF THE MATERIAL : TÜRKİYE', merge_format14)
            sheet.merge_range('J1:N1', 'FATURA / INVOICE :' , merge_format10)
            sheet.merge_range('J2:N2', 'ALICI / RECEIVER:' , merge_format10)
            sheet.merge_range('J3:N9', 'YENA ENGINEERING B.V. \nWTC ROTTERDAM BEURSPLEIN 37\n3011 AA\nROTERDAM/ NETHERLANDS' , merge_format18)
            
            # Başlıkları ekle
            headers = [
                'PALLET NO', 'ORDER NO', 'POSE', 'Antlaşma No:\nO.A NO:',
                'MIKTARI\nQUANTITY', 'BİRİM\nUNIT', 'NET AĞIRLIK (KG)\nNET WEIGHT (KG)',
                'TOPLAM NET AĞIRLIK (KG)\nTOTAL NET WEIGHT (KG)',
                'DARA AĞIRLIK (KG)\nTARE WEİGHT (KG)', 'BRÜT AĞIRLIK (KG)\nGROSS WEİGHT (KG)',
                'EN (MM)\nWIDTH (MM)', 'BOY (MM)\nLENGTH (MM)', 'YÜKSEKLİK (MM)\nHEIGHT (MM)', 'STACKABLE',
            ]
            pallet_data = {}
            for line in batch.packaging_preparation_ids:
                pallet_no = line.pallet_no
                if pallet_no not in pallet_data:
                    pallet_data[pallet_no] = {
                        'lines': [],
                        'unit_net_weight': 0,
                        'total_net_weight': 0,
                        'gross_weight': 0,
                        'total_gross_weight': 0,
                    }
                pallet_data[pallet_no]['lines'].append(line)
                pallet_data[pallet_no]['unit_net_weight'] += line.unit_net_weight
                pallet_data[pallet_no]['total_net_weight'] += line.total_net_weight
                pallet_data[pallet_no]['gross_weight'] += line.gross_weight
                pallet_data[pallet_no]['total_gross_weight'] += line.total_gross_weight
            row = 12  # 13. satırdan başla (0-indexed)

            # Başlık satırını yaz ve kalın biçimi uygula
            for col, header in enumerate(headers):
                sheet.write(row, col, header, header_format)

            for pallet_no, data in pallet_data.items():
                start_row = row + 1  # Grup için başlangıç satırı
                all_stackable = True 
                max_volume = 0  # En büyük hacmi saklamak için
                max_dimensions = {}  # En büyük hacme sahip boyutları saklamak için
                for line in data['lines']:
                    row += 1

                    if not line.stackable:
                        all_stackable = False
                    
                    volume = line.width * line.length * line.height
                    if volume > max_volume:
                        max_volume = volume
                        max_dimensions = {
                            'width': line.width,
                            'length': line.length,
                            'height': line.height,
            }
                    # S.NO
                    sheet.write(row, 0, line.pallet_no, centered_format)
                    # ORDER NO (Customer Reference)
                    sheet.write(row, 1, line.customer_reference or '', centered_format)
                    # Drawing Number (Product)
                    sheet.write(row, 2, line.product_id.display_name, centered_format)
                    # Outline Aggrement
                    partner_ref = line.purchase_order_line_id.blanket_order_line.order_id.partner_ref if line.purchase_order_line_id.blanket_order_line.order_id.partner_ref else '-'
                    sheet.write(row, 3, partner_ref, centered_format)
                    # Quantity (Package Quantity)
                    sheet.write(row, 4, line.package_quantity, centered_format)
                    # UNIT (Unit of Measure)
                    sheet.write(row, 5, line.unit_of_measure.name, centered_format)
                    # Net(kg) (Unit Net Weight)
                    sheet.write(row, 6, line.unit_net_weight, centered_format)
                    # Net(kg) (Total Net Weight)
                    sheet.write(row, 7, line.total_net_weight, centered_format)
                    # Brüt(kg) (Gross Weight)
                    sheet.write(row, 8, line.gross_weight, centered_format)
                    # Brüt(kg) (Total Gross Weight)
                    sheet.write(row, 9, line.total_gross_weight, centered_format)
                    # Package Width (EN (MT) WIDTH)
                    sheet.write(row, 10, line.width, centered_format)
                    # Package Length (EN (MT) LENGTH)
                    sheet.write(row, 11, line.length, centered_format)
                    # Package Height (EN (MT) HEIGTH)
                    sheet.write(row, 12, line.height, centered_format)
                    # STACKABLE
                    sheet.write(row, 13, '✓' if line.stackable else '×', centered_format)
                    # Package Number (Pallet Number)

                total_row = row + 1  # Toplamlar için bir boş satır bırak
                sheet.write(total_row, 7, sum(data['total_net_weight'] for data in pallet_data.values()), centered_format_bg)
                # Dara ağırlık toplamı (Varsa)
                # Brüt ağırlık toplamı
                sheet.write(total_row, 8, sum(data['gross_weight'] for data in pallet_data.values()), centered_format_bg)
                # Toplam brüt ağırlık
                sheet.write(total_row, 9, sum(data['total_gross_weight'] for data in pallet_data.values()), centered_format_bg)

                end_row = row  # Grup için bitiş satırı
                stackable_value = '✓' if all_stackable else '×'
                if len(data['lines']) > 1:
                    # İlk satırı al ve birleştir
                    first_line = data['lines'][0]
                    sheet.merge_range(start_row, 0, end_row, 0, first_line.pallet_no, centered_format)
                    sheet.merge_range(start_row, 7, end_row, 7, data['total_net_weight'], centered_format)
                    sheet.merge_range(start_row, 8, end_row, 8, data['gross_weight'], centered_format)
                    sheet.merge_range(start_row, 9, end_row, 9, data['total_gross_weight'], centered_format)
                    sheet.merge_range(start_row, 10, row, 10, max_dimensions.get('width', ''), centered_format)
                    sheet.merge_range(start_row, 11, row, 11, max_dimensions.get('length', ''), centered_format)
                    sheet.merge_range(start_row, 12, row, 12, max_dimensions.get('height', ''), centered_format)
                    sheet.merge_range(start_row, 13, row, 13, stackable_value, centered_format)

