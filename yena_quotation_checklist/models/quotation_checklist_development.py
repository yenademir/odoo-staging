from odoo import api, fields, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    customer_log = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Have customer notes been entered as Log Notes?')

    requested_received = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Were order quantities (first order and annual), target prices, photos of the product in use or in its finished state, and packaging photos requested/received?')
    requested_received_note = fields.Char(string='Were order quantities (first order and annual), target prices, photos of the product in use or in its finished state, and packaging photos requested/received?')

    material_list = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Has the Material List been issued/created?')
    material_list_note = fields.Char(string='Has the Material List been issued/created?')
    
    surface_treatment = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Is the surface treatment specified?')
    surface_treatment_note = fields.Char(string='Is the surface treatment specified?')
    
    weights_clear = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Are the weights clear?')
    weights_clear_note = fields.Char(string='Are the weights clear?')
    
    manufacturing_processes = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Are the manufacturing processes clear?')
    manufacturing_processes_note = fields.Char(string='Are the manufacturing processes clear?')
    
    drawing_sufficient = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Are the drawings sufficient?', 
        help="(dwg or step may be requested if required)"
        )
    drawing_sufficient_note = fields.Char(string='Are the drawings sufficient?')
    
    drawing_information = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')
    ], string='Are there materials, measurement information, welding information and tolerances in the drawings of all parts?')
    drawing_information_note = fields.Char(string='Are there materials, measurement information, welding information and tolerances in the drawings of all parts?')
        
    important_notes = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Is there an important detail in the notes on the drawing?' )
    important_notes_note = fields.Char(string='Is there an important detail in the notes on the drawing?')
            
    raw_material_supplied = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Can raw materials be supplied? Is it suitable for processing in basic processes?' )
    raw_material_supplied_note = fields.Char(string='Can raw materials be supplied? Is it suitable for processing in basic processes?')
            
    surface_treatment_information = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Is there surface treatment information? Coating type, thickness (micron value) etc. clear? If hot-dip galvanized, are there galvanization holes?')
    surface_treatment_information_note = fields.Char(string='Is there surface treatment information? Coating type, thickness (micron value) etc. clear? If hot-dip galvanized, are there galvanization holes?')
            
    bolts_nuts_nonsteel = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='If there are bolts and nuts or non-steel parts, will these be within the scope of YENA?')
    bolts_nuts_nonsteel_note = fields.Char(string='If there are bolts and nuts or non-steel parts, will these be within the scope of YENA?')
            
    assembly_notes = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='If there is pre-assembly or on-site assembly, will it be within the scope of YENA?')
    assembly_notes_note = fields.Char(string='If there is pre-assembly or on-site assembly, will it be within the scope of YENA?')
            
    ndt_information = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Is there a request for NDT?')
    ndt_information_note = fields.Char(string='Is there a request for NDT?')
            
    certification_documents = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Are the certifications and documents requested by the customer available?')
    certification_documents_note = fields.Char(string='Are the certifications and documents requested by the customer available?')
            
    dies_fixtures = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Will dies or fixtures be made?', 
        )
    dies_fixtures_note = fields.Char(string='Will dies or fixtures be made?')
                
    kickoff_meeting = fields.Selection([
        ('yes', 'Yes'),
        ('no', 'No')], 
        string='Has a Kick-Off Meeting with the customer been made?', 
        )
    kickoff_meeting_note = fields.Html(string='Has a Kick-Off Meeting with the customer been made?')
            
