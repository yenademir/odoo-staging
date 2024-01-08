from odoo import models, fields, api
import requests
import base64
import logging
_logger = logging.getLogger(__name__)

class DocumentUploadWizard(models.Model):
    _name = 'document.upload.wizard'
    _description = 'Document Upload Wizard'
 
    certificate_line_ids = fields.One2many(
        'document.upload.wizard.line', 'wizard_id', string='Certificate Lines'
    )

    measurement_report_ids = fields.One2many(
        'document.upload.wizard.measurement.report', 'wizard_id', string='Measurement Reports'
    )

    galvanize_ids = fields.One2many(
        'document.upload.wizard.galvanize', 'wizard_id', string='Galvanize'
    )

    packaging_ids = fields.One2many(
        'document.upload.wizard.packaging', 'wizard_id', string='Packaging'
    )

    purchase_name = fields.Char('Purchase Name')

class DocumentUploadWizardLine(models.Model):
    _name = 'document.upload.wizard.line'
    _description = 'Document Upload Wizard Line'

    wizard_id = fields.Many2one('document.upload.wizard', string='Wizard')
    required_document = fields.Char(string='Required Document')
    uploaded_document = fields.Char(string='Uploaded Document')
    material_thickness = fields.Char(string="Thickness")
    material_width = fields.Char(string="Width")
    material_length = fields.Char(string="Length")
    is_uploaded = fields.Boolean(string='Yüklemeden Devam Et')
    upload_document = fields.Binary(string='Upload Document')

    material_certificate_id = fields.Many2one(
        'material.certificate', string='Material Certificate'
    )

    @api.onchange('upload_document')
    def onchange_upload_document(self):
        if self.upload_document:
            # Dosya yükleme işlemi
            success = self.upload_to_cdn()
            if success:
                # Yükleme başarılıysa 'upload_document' alanını boşalt
                self.upload_document = False


    def upload_to_cdn(self):
        file_data = self.upload_document
        if file_data:
            api_url = "https://portal-test.yenaengineering.nl/api/qualitydocuments"
            file_name = self.required_document if self.required_document else "certificate_file"

            files = {
                'quality_documents': (file_name, base64.b64decode(file_data), 'application/octet-stream')
            }
            data = {'purchase': self.wizard_id.purchase_name}

            response = requests.post(api_url, files=files, data=data)
            if response.status_code == 201:
                result = response.json()
                certificate_url = result['data']['certificate_url']

                # Google Drive viewer URL'si ile birleştir
                viewer_url = "https://drive.google.com/viewerng/viewer?embedded=true&url=" + certificate_url
                self.uploaded_document = viewer_url

                return True  # Başarı durumunu belirt
            return False  # Başarısızlık durumunu belirt
        
class DocumentUploadWizardMeasurementReport(models.Model):
    _name = 'document.upload.wizard.measurement.report'
    _description = 'Document Upload Wizard Measurement Report'

    wizard_id = fields.Many2one('document.upload.wizard', string='Wizard')
    name = fields.Char(string='Name')
    upload_document = fields.Binary(string='Upload Document')
    is_uploaded = fields.Boolean(string='Yüklemeden Devam Et')
    uploaded_document = fields.Char(string='Uploaded Document')

    def filename_extract_from_binary_field(self):
        if self.upload_document:
            # Odoo, binary alanlarda dosya adını 'filename;' önekini kullanarak saklar
            file_info = self.upload_document.decode().split(';')[0]
            file_name = file_info.split('=')[-1] if '=' in file_info else 'unknown_file'
            return file_name
        return 'unknown_file'

    @api.onchange('upload_document')
    def onchange_upload_document(self):
        if self.upload_document:
            # Dosya yükleme işlemi
            success = self.upload_to_cdn()
            if success:
                # Yükleme başarılıysa 'upload_document' alanını boşalt
                self.upload_document = False

    def upload_to_cdn(self):
        file_data = self.upload_document
        if file_data:
            api_url = "https://portal-test.yenaengineering.nl/api/qualitydocuments"
            
            # Dosya adını al
            file_name = self.filename_extract_from_binary_field()

            files = {
                'quality_documents': (file_name, base64.b64decode(file_data), 'application/octet-stream')
            }
            data = {'purchase': self.wizard_id.purchase_name}

            response = requests.post(api_url, files=files, data=data)
            if response.status_code == 201:
                result = response.json()
                certificate_url = result['data']['certificate_url']

                # Google Drive viewer URL'si ile birleştir
                viewer_url = "https://drive.google.com/viewerng/viewer?embedded=true&url=" + certificate_url
                self.uploaded_document = viewer_url

                return True  # Başarı durumunu belirt
            return False  # Başarısızlık durumunu belirt
        
class DocumentUploadWizardGalvanize(models.Model):
    _name = 'document.upload.wizard.galvanize'
    _description = 'Document Upload Wizard Galvanize'

    wizard_id = fields.Many2one('document.upload.wizard', string='Wizard')
    name = fields.Char(string='Name')
    upload_document = fields.Binary(string='Upload Document')
    is_uploaded = fields.Boolean(string='Yüklemeden Devam Et')
    uploaded_document = fields.Char(string='Uploaded Document')

    def filename_extract_from_binary_field(self):
        if self.upload_document:
            # Odoo, binary alanlarda dosya adını 'filename;' önekini kullanarak saklar
            file_info = self.upload_document.decode().split(';')[0]
            file_name = file_info.split('=')[-1] if '=' in file_info else 'unknown_file'
            return file_name
        return 'unknown_file'

    @api.onchange('upload_document')
    def onchange_upload_document(self):
        if self.upload_document:
            # Dosya yükleme işlemi
            success = self.upload_to_cdn()
            if success:
                # Yükleme başarılıysa 'upload_document' alanını boşalt
                self.upload_document = False

    def upload_to_cdn(self):
        file_data = self.upload_document
        if file_data:
            api_url = "https://portal-test.yenaengineering.nl/api/qualitydocuments"
            
            # Dosya adını al
            file_name = self.filename_extract_from_binary_field()

            files = {
                'quality_documents': (file_name, base64.b64decode(file_data), 'application/octet-stream')
            }
            data = {'purchase': self.wizard_id.purchase_name}

            response = requests.post(api_url, files=files, data=data)
            if response.status_code == 201:
                result = response.json()
                certificate_url = result['data']['certificate_url']

                # Google Drive viewer URL'si ile birleştir
                viewer_url = "https://drive.google.com/viewerng/viewer?embedded=true&url=" + certificate_url
                self.uploaded_document = viewer_url

                return True  # Başarı durumunu belirt
            return False  # Başarısızlık durumunu belirt

class DocumentUploadWizardGalvanize(models.Model):
    _name = 'document.upload.wizard.packaging'
    _description = 'Document Upload Wizard Packaging'

    wizard_id = fields.Many2one('document.upload.wizard', string='Wizard')
    name = fields.Char(string='Name')
    upload_document = fields.Binary(string='Upload Document')
    is_uploaded = fields.Boolean(string='Yüklemeden Devam Et')
    uploaded_document = fields.Char(string='Uploaded Document')

    def filename_extract_from_binary_field(self):
        if self.upload_document:
            # Odoo, binary alanlarda dosya adını 'filename;' önekini kullanarak saklar
            file_info = self.upload_document.decode().split(';')[0]
            file_name = file_info.split('=')[-1] if '=' in file_info else 'unknown_file'
            return file_name
        return 'unknown_file'

    @api.onchange('upload_document')
    def onchange_upload_document(self):
        if self.upload_document:
            # Dosya yükleme işlemi
            success = self.upload_to_cdn()
            if success:
                # Yükleme başarılıysa 'upload_document' alanını boşalt
                self.upload_document = False

    def upload_to_cdn(self):
        file_data = self.upload_document
        if file_data:
            api_url = "https://portal-test.yenaengineering.nl/api/qualitydocuments"
            
            # Dosya adını al
            file_name = self.filename_extract_from_binary_field()

            files = {
                'quality_documents': (file_name, base64.b64decode(file_data), 'application/octet-stream')
            }
            data = {'purchase': self.wizard_id.purchase_name}

            response = requests.post(api_url, files=files, data=data)
            if response.status_code == 201:
                result = response.json()
                certificate_url = result['data']['certificate_url']

                # Google Drive viewer URL'si ile birleştir
                viewer_url = "https://drive.google.com/viewerng/viewer?embedded=true&url=" + certificate_url
                self.uploaded_document = viewer_url

                return True  # Başarı durumunu belirt
            return False  # Başarısızlık durumunu belirt
