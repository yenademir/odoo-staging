from odoo import api, fields, models
import logging
from odoo.exceptions import UserError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    bid_time=fields.Char(string="Bid Time")
    contact_id = fields.Many2one('res.partner', string='Contact Person', store=True)
    customer_reference=fields.Char(string="Customer Reference No", store=True)
    delivery_date=fields.Char(string="C-Delivery Date (Text)")
    invoice_report=fields.Selection([("fullyinvoiced","Fully Invoiced"),("partiallyinvoice","Partially Invoiced"),("nothinginvoiced","Nothing Invoiced")],string="Invoice Report")
    lost=fields.Many2one("crm.lost.reason",string="Lost Reason")
    lost_reason=fields.Many2one("crm.lost.reason",string="Lost Reason")
    project_sales=fields.Many2one("project.project",string="Project Number", store=True)
    quo_date=fields.Date(string="C-Quotation Date")
    rfq_date=fields.Date(string="C-RFQ Date")
    rfq_reference=fields.Char(string="RFQ Reference", store=True)
    is_current_user = fields.Boolean(compute='_compute_is_current_user')
    account_note = fields.Html(string="Account Note")

    customer_meeting = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Müşteri İle Yapılan Görüşmeler')
    customer_meeting_note = fields.Char(string='Müşteri İle Yapılan Görüşmeler Notu')

    initial_info_request = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Müşteriden Gelen Talepte İlk Bilgiler')
    initial_info_request_note = fields.Char(string='Müşteriden Gelen Talepte İlk Bilgiler Notu')

    metrage_study = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Metraj Çalışması')
    metrage_study_note = fields.Char(string='Metraj Çalışması Notu')

    technical_inspection = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Teknik İncelemeler')
    technical_inspection_note = fields.Char(string='Teknik İncelemeler Notu')

    drawing_sufficiency = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Çizimlerin Yeterliliği')
    drawing_sufficiency_note = fields.Char(string='Çizimlerin Yeterliliği Notu')

    drawing_details = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Çizim Detayları')
    drawing_details_note = fields.Char(string='Çizim Detayları Notu')

    raw_material_availability = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Hammadde Tedarik Edilebilirliği')
    raw_material_availability_note = fields.Char(string='Hammadde Tedarik Edilebilirliği Notu')

    surface_treatment_info = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Yüzey İşlemi Bilgileri')
    surface_treatment_info_note = fields.Char(string='Yüzey İşlemi Bilgileri Notu')

    non_steel_elements = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Bağlantı Elemanları ve Çelik Dışı Parçalar')
    non_steel_elements_note = fields.Char(string='Bağlantı Elemanları ve Çelik Dışı Parçalar Notu')

    assembly_scope = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Montaj Kapsamı')
    assembly_scope_note = fields.Char(string='Montaj Kapsamı Notu')

    ndt_request = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='NDT Talebi')
    ndt_request_note = fields.Char(string='NDT Talebi Notu')

    certifications_documents = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Sertifikasyon ve Belgeler')
    certifications_documents_note = fields.Char(string='Sertifikasyon ve Belgeler Notu')

    mold_fixture_creation = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Kalıp veya Fikstür Yapımı')
    mold_fixture_creation_note = fields.Char(string='Kalıp veya Fikstür Yapımı Notu')

    design_activities = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Tasarım Faaliyetleri')
    design_activities_note = fields.Char(string='Tasarım Faaliyetleri Notu')

    special_packaging_request = fields.Selection([
        ('yes', 'Evet'),
        ('no', 'Hayır')
    ], string='Özel Paketleme Talebi')
    special_packaging_request_note = fields.Char(string='Özel Paketleme Talebi Notu')
    document_numbers = fields.Char(string='Document Numbers', compute='_compute_document_numbers')
    transportation_codes = fields.Char(string="Transportation Codes", compute='_compute_transportation_codes')
    date_done_list = fields.Char(string="Effective Date", compute='_compute_date_done_list')


    def _compute_document_numbers(self):
        for order in self:
            pickings = self.env['stock.picking'].search([('sale_id', '=', order.id)])
            if pickings:
                document_numbers = [picking.document_number for picking in pickings if picking.document_number]
                document_numbers_str = ', '.join(document_numbers)
                order.document_numbers = document_numbers_str
            else:
                order.document_numbers = ''

    def _compute_transportation_codes(self):
        for order in self:
            pickings = self.env['stock.picking'].search([('sale_id', '=', order.id)])
            if pickings:
                unique_transportation_codes = {picking.transportation_code for picking in pickings if picking.transportation_code}
                transportation_codes_str = ', '.join(unique_transportation_codes)
                order.transportation_codes = transportation_codes_str
            else:
                order.transportation_codes = ''


    def _compute_date_done_list(self):
        for order in self:
            pickings = self.env['stock.picking'].search([('sale_id', '=', order.id)])
            if pickings:
                date_dones = [picking.date_done.strftime("%Y-%m-%d") for picking in pickings if picking.date_done]
                date_dones_str = ', '.join(date_dones)
                order.date_done_list = date_dones_str
            else:
                order.date_done_list = ''

    @api.model
    def create(self, vals):

        company_id = vals.get('company_id', False)
        if company_id == 1:
            return super().create(vals)

        # customer_reference'ın rfq_reference'a kopyalandığını kontrol edin.
        if 'customer_reference' in vals and vals['customer_reference']:
            vals['rfq_reference'] = vals['customer_reference']

        # rfq_date'i bugünün tarihi ile doldurun.
        vals['rfq_date'] = fields.Date.today()

        record = super().create(vals)

        if not record.customer_reference:
            return record

        # satış oluşturulduktan sonra bir proje oluştur.
        project_vals = {
            'name': record.name + '-' + record.customer_reference,
            'partner_id': record.partner_id.id,
            'company_id': 2,
        }
        project = self.env['project.project'].create(project_vals)

        # Proje oluşturulduktan sonra analitik hesap ID'yi al
        analytic_account_id = project.analytic_account_id.id if project.analytic_account_id else None

        # Son olarak, satışa analitik hesabı ve proje ID'yi ekleyin.
        record.write({
            'analytic_account_id': analytic_account_id,
            'project_sales': project.id,
            'company_id': 2,
        })

        return record

    def action_confirm(self):
        # C-Delivery Date kontrolü
        if not self.commitment_date:
            raise UserError('The C-Delivery Date is mandatory! Please add this date and try again.')
    
        # company_id 1 ise, standart onay işlemi yapılır ve özel işlemlerden kaçınılır
        if self.company_id.id == 1:
            return super(SaleOrder, self).action_confirm()
    
        # Diğer durumlarda, öncelikle standart onay işlemi yapılır
        res = super(SaleOrder, self).action_confirm()
    
        current_user = self.env.user  # Şu anki kullanıcıyı al
        incoterm = self.env['account.incoterms'].browse(10)
    
        for order in self:
            purchase_orders = self.env['purchase.order'].search([('origin', '=', order.name)])
            for purchase_order in purchase_orders:
                purchase_order.write({
                    'user_id': current_user.id,
                    'customer_reference': order.customer_reference,
                    'project_purchase': order.project_sales.id,
                    'incoterm_id': incoterm.id
                })
    
                # İlişkili tüm satın alma siparişi satırlarını sil
                purchase_order.order_line.unlink()
    
                # Yeni satın alma siparişi satırlarını oluştur
                for so_line in order.order_line:
                    new_price_unit = so_line.price_unit * 0.92  # Satış fiyatını 0.92 ile çarp
                    purchase_order.order_line.create({
                        'order_id': purchase_order.id,
                        'product_id': so_line.product_id.id,
                        'product_qty': so_line.product_uom_qty,
                        'product_uom': so_line.product_uom.id,
                        'price_unit': new_price_unit,
                        'name': so_line.name,
                        'date_planned': purchase_order.date_order,
                        'account_analytic_id': order.analytic_account_id.id,
                        'sale_order_id': so_line.order_id.id,
                    })
    
            # İlişkili tüm teslimat emirlerini bul
            delivery_orders = self.env['stock.picking'].search([('origin', '=', order.name)])
            # İlişkili tüm teslimat emirlerini güncelle
            for delivery_order in delivery_orders:
                delivery_order.write({
                    'project_transfer': [(6, 0, order.project_sales.ids)],
                })
    
        # Eğer customer_reference değiştiyse analitik hesap ve proje adını güncelle
        if self.rfq_reference != self.customer_reference:
            project = self.project_sales
            project.write({
                'name': self.name + '-' + self.customer_reference
            })
            analytic_account = self.analytic_account_id
            analytic_account.write({
                'name': project.name
            })
    
        return res

    def action_quotation_sent(self):
        res = super(SaleOrder, self).action_quotation_sent()

        # Quotation gönderildiğinde quo_date'i güncelle
        for record in self:
            record.write({
                'quo_date': fields.Date.today(),
            })

        return res

    @api.onchange('delivery_date')
    def _onchange_delivery_date(self):
        for line in self.order_line:
            line.product_delivery_date = self.delivery_date

    @api.depends('user_id')
    def _compute_is_current_user(self):
        for record in self:
            record.is_current_user = record.user_id == self.env.user

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.contact_id = False
        return {'domain': {'contact_id': [('parent_id', '=', self.partner_id.id), ('type', '=', 'contact')]}}

    def print_proposal_form(self):
        # id'si 2298 olan raporu indir
        return self.env.ref('__export__.ir_act_report_xml_2298_852ac486').report_action(self)

    class SaleOrderLine(models.Model):
        _inherit = 'sale.order.line'

        product_delivery_date = fields.Date(string="Product Delivery Date")


#Intercompany & autofill

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _inter_company_create_sale_order(self, dest_company):
        super(PurchaseOrder, self)._inter_company_create_sale_order(dest_company)

        # Satın almadan satışa aktarılacak verileri alın
        purchase_order = self.env['purchase.order'].browse(self.id)

        project = purchase_order.project_purchase
        if project and hasattr(project, 'analytic_account_id') and project.analytic_account_id:
            analytic_account_id = project.analytic_account_id.id
        else:
            analytic_account_id = False

        # Şirket ve partner koşulları
        if purchase_order.company_id.id == 2 and purchase_order.partner_id.id == 1:
            # Satış siparişi değerleri
            sale_order_vals = {
                'project_sales': project.id if project else False,
                'analytic_account_id': analytic_account_id,
                'customer_reference': purchase_order.customer_reference,
            }

            # Satış siparişini bulun
            sale_order = self.env['sale.order'].search([('auto_purchase_order_id', '=', self.id)], limit=1)
            sale_order.write(sale_order_vals)

            # Satın alma siparişi satırlarını döngüleyin ve satış siparişi satırlarını güncelleyin
            for po_line, so_line in zip(purchase_order.order_line, sale_order.order_line):
                sale_line_vals = {
                    'price_unit': po_line.price_unit,
                }
                so_line.write(sale_line_vals)
