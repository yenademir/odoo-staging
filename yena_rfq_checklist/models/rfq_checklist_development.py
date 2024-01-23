from odoo import api, fields, models

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    
    project_docs = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Projenin talep ettiği sertifikasyon ve belgeler mevcut mu?')
    project_docs_note = fields.Char(string='Projenin talep ettiği sertifikasyon ve belgeler mevcut mu?')

    is_supllied = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Bu tedarikçi bu hammaddeyi tedarik edebilir mi? Temel proseslerde işlemeye uygun mu?')
    is_supllied_note = fields.Char(string='Bu tedarikçi bu hammaddeyi tedarik edebilir mi? Temel proseslerde işlemeye uygun mu?')

    drawing_activities = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Proje kapsamında yapılacak tasarım faaliyetleri var mı? Varsa termini açıklamaya ekleyiniz?')
    drawing_activities_note = fields.Char(string='Proje kapsamında yapılacak tasarım faaliyetleri var mı? Varsa termini açıklamaya ekleyiniz?')
    
    equipments_capability = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Tedarikçinin makine ekipmanları proje için yeterli mi?')
    equipments_capability_note = fields.Char(string='Tedarikçinin makine ekipmanları proje için yeterli mi?')
    
    external_outsource = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Tedarikçi dış kaynak kullanacak mı? Kullanılacak ise hangi operasyonlar için?')
    external_outsource_note = fields.Char(string='Tedarikçi dış kaynak kullanacak mı? Kullanılacak ise hangi operasyonlar için?')
    
    measurement_equipment_supplier = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Tedarikçinin ölçüm ekipmanları yeterli mi?')
    measurement_equipment_supplier_note = fields.Char(string='Tedarikçinin ölçüm ekipmanları yeterli mi?')
    
    measurement_equipment_yena = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Yena KK ekibinin ölçüm aletleri yeterli mi?', 
        help="(dwg or step may be requested if required)"
        )
    measurement_equipment_yena_note = fields.Char(string='Yena KK ekibinin ölçüm aletleri yeterli mi?')
    
    mold_or_fixture = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Kalıp veya fikstür yapılacak mı?')
    mold_or_fixture_note = fields.Char(string='Kalıp veya fikstür yapılacak mı?')
        
    before_project = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Proje öncesi YENA ya da tedarikçi tarafında herhangi bir operasyon adımı için eğitim ihtiyacı var mı?' )
    before_project_note = fields.Char(string='Proje öncesi YENA ya da tedarikçi tarafında herhangi bir operasyon adımı için eğitim ihtiyacı var mı?')
            
    transfer_condition = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Sevkiyat şartları ve ambalajlama yöntemi için müşteri ile teyitleşildi mi?' )
    transfer_condition_note = fields.Char(string='Sevkiyat şartları ve ambalajlama yöntemi için müşteri ile teyitleşildi mi?')
            
    wpqr_approval = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='WPQR (KAYNAK YÖNTEM ONAYI) yeterli mi?')
    wpqr_approval_note = fields.Char(string='WPQR (KAYNAK YÖNTEM ONAYI) yeterli mi?')
            
    welder_cert = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Kaynakçı sertifikası kapsamı yeterli ve süreleri proje sonuna kadar geçerli mi?')
    welder_cert_note = fields.Char(string='Kaynakçı sertifikası kapsamı yeterli ve süreleri proje sonuna kadar geçerli mi?')
            
    test_info = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Proje kapsamında tahribatlı veya tahribatsız test isteniyor mu?')
    test_info_note = fields.Char(string='Proje kapsamında tahribatlı veya tahribatsız test isteniyor mu?')
            
    ndt_information = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Dışarıdan NDT hizmeti ihtiyacı olacak mı?')
    ndt_information_note = fields.Char(string='Dışarıdan NDT hizmeti ihtiyacı olacak mı?')
            
    supplier_checklist = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Yapılacak faaliyetler için kalifiyeli personel var mı? İhtiyacı gerekli mi? (tedarikçi)')
    supplier_checklist_note = fields.Char(string='Yapılacak faaliyetler için kalifiyeli personel var mı? İhtiyacı gerekli mi? (tedarikçi)')
            
    yena_checklist = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Yapılacak faaliyetler için kalifiyeli personel var mı? İhtiyacı gerekli mi? (YENA)')
    yena_checklist_note = fields.Char(string='Yapılacak faaliyetler için kalifiyeli personel var mı? İhtiyacı gerekli mi? (YENA)')
                
    hole_information = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Kaplama prosesi varsa delik çapları yeri ve sayısı yeterli mi?')
    hole_information_note = fields.Char(string='Kaplama prosesi varsa delik çapları yeri ve sayısı yeterli mi?')
                
    is_info_shared = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Boya, kaplama öncesi keskin kenarların, lazer kesim izlerinin, kaynak çapaklarının giderilmesi; malzeme yüzeyinin yağlı kirli veya paslı olmaması gerektiği tedarikçi ile paylaşıldı mı?')
    is_info_shared_note = fields.Char(string='Boya, kaplama öncesi keskin kenarların, lazer kesim izlerinin, kaynak çapaklarının giderilmesi; malzeme yüzeyinin yağlı kirli veya paslı olmaması gerektiği tedarikçi ile paylaşıldı mı?')
                
    is_revision_actual = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Revizyonlar güncel mi?')
    is_revision_actual_note = fields.Char(string='Revizyonlar güncel mi?')
                
    potential_nonconformity = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Oluşabilecek uygunsuzluklar var mı? Varsa nedir ve nasıl önlem alınabilir?')
    potential_nonconformity_note = fields.Char(string='Oluşabilecek uygunsuzluklar var mı? Varsa nedir ve nasıl önlem alınabilir?')
                
    kickoff_meeting = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Has a Kick-Off Meeting with the customer been made?')
    kickoff_meeting_note = fields.Html(string='Has a Kick-Off Meeting with the customer been made?')
            
