from random import randrange
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HospitalAppointment(models.Model):
    _name = 'hospital.appointment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Appointment'
    _rec_name = 'ref'
    _order = 'id desc'
    
    name = fields.Char(string='Sequence', default='New')
    patient_id = fields.Many2one('hospital.patient', string="Patient",ondelete='cascade' , help="Pilih data pasien yang akan melakukan jadwal pemeriksaan.")
    gender = fields.Selection( string='Gender',selection= [ ('male', 'Male'), ('female', 'Female')  ], related='patient_id.gender',readonly=False, help="Jenis kelamin pasien." )
    appointment_time = fields.Datetime(string="Appointment Time", default=fields.Datetime.now, help="Tentukan waktu pelaksanaan jadwal pemeriksaan pasien.")
    duration = fields.Float(string='Duration', default=1.0, help='Appointment duration in hours.')
    booking_date = fields.Date(string="Booking Date", default=fields.Date.context_today, help="Tanggal saat jadwal pemeriksaan ini dibuat.")
    ref = fields.Char(string='Reference', related='patient_id.ref', help="Referensi tambahan untuk pemeriksaan ini.")
    prescription = fields.Html(string='Prescription', help="Tuliskan detail resep obat atau catatan medis yang diberikan kepada pasien.")
    doctor_id = fields.Many2one('res.users', string="Doctor", tracking=True)
    appointment_pharmacy_lines_ids = fields.One2many('appointment.pharmacy.lines', 'appointment_id', string="Appointment Pharmacy Lines")
    hide_sales_price = fields.Boolean(string="Hide Sales Price", default=False)
    image = fields.Image(related='patient_id.image', string='Image')
    progress = fields.Integer(string='Progress', compute='_compute_progress')

    priority = fields.Selection(
        string='Priority',
        selection=[ 
            ('0', 'Normal'),
            ('1', 'Low'),
            ('2', 'High'),
            ('3', 'Very High'),
        ],
        help="Pilih tingkat prioritas penanganan untuk jadwal ini."
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_consultation', 'In Consultation'),
        ('done', 'Done'),
        ('cancel', 'Cancel'),
    ],default='draft',required=True, help="Status terkini dari jadwal pemeriksaan.")

    @api.model
    def create(self,vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hospital.appointment')
        return super(HospitalAppointment,self).create(vals)

    def unlink(self):
        for rec in self:
            if rec.state != 'done':
                raise ValidationError("You can not delete done state")
        return super(HospitalAppointment,self).unlink()

    
    @api.onchange('patient_id')
    def onchange_patient_id(self):
        if self.patient_id:
            self.gender = self.patient_id.gender


    def action_test(self):
        print("button clicked!")
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Proses Berhasil! Data telah tersimpan.',
                'type': 'rainbow_man',
            }
        }

    def action_in_consultation(self):
        for rec in self:
            rec.state = 'in_consultation'
            
    def action_done(self):
        for rec in self:
            rec.state = 'done'
            
    def action_cancel(self):
        action = self.env.ref('om_hospital.action_cancel_appointment_wizard').read()[0]
        action['res_id'] = self.id
        return action   

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    @api.depends('state')
    def _compute_progress(self):
        for rec in self:
            if rec.state == 'draft':
                rec.progress = randrange(0, 25)
            elif rec.state == 'in_consultation':
                rec.progress = randrange(26, 99)
            elif rec.state == 'done':
                rec.progress = 100
            elif rec.state == 'cancel':
                rec.progress = 0

class AppoinmentPharmacyLines(models.Model):
    _name = 'appointment.pharmacy.lines'
    _description = 'Appointment Pharmacy Lines'

    product_id = fields.Many2one('product.template', string="Product",required=True)
    qty = fields.Integer(string="Quantity",required=True, default=1)
    price_unit = fields.Float(string="Unit Price",readonly=True, related='product_id.list_price')
    total = fields.Float(string="Total",readonly=True, compute='_compute_total')

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment")
    
    @api.depends('qty', 'price_unit')
    def _compute_total(self):
        for rec in self:
            rec.total = rec.qty * rec.price_unit
            
    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.list_price


