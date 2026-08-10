from odoo import models, fields, api, _
from datetime import date
from odoo.exceptions import ValidationError
from dateutil.relativedelta import relativedelta

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Hospital Patient'
    _order = "id desc"
    _inherit = ['mail.thread', 'mail.activity.mixin']


    name = fields.Char(string='Name', required=True, tracking=True, help="Masukkan nama lengkap dari pasien.")
    patient_code = fields.Char(string='Sequence', required=True, copy=False, readonly=True, default='New', tracking=True)
    photo = fields.Image(string='Photo')
    phone = fields.Char(string='Phone', tracking=True)
    address = fields.Text(string='Address')
    blood_type = fields.Selection([
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'AB'),
        ('O', 'O'),
    ], string='Blood Type')
    date_of_birth = fields.Date(string='Date of Birth', required=True, tracking=True, help="Pilih tanggal lahir pasien. Umur pasien akan dihitung secara otomatis berdasarkan tanggal ini.")
    age = fields.Integer(string='Age', compute='_compute_age', inverse='_inverse_compute_age', search='_search_age', store=True, help="Umur pasien yang dihitung secara otomatis dari tanggal lahir.")
    gender = fields.Selection( string='Gender',selection= [ ('male', 'Male'), ('female', 'Female')  ], default='female', tracking=True, help="Pilih jenis kelamin dari pasien." )
    active = fields.Boolean(string='Active', default=True, help="Tandai kotak ini jika pasien masih aktif, atau hilangkan centang untuk mengarsipkan.")
    ref = fields.Char(string='Reference', help="Masukkan nomor referensi atau nomor rekam medis pasien.")
    appointment_id = fields.One2many('hospital.appointment', 'patient_id', string="Appointment", help="Riwayat atau daftar jadwal pemeriksaan untuk pasien ini.")
    image = fields.Image(string='Image', help="Masukkan foto pasien")
    tag_ids = fields.Many2many('patient.tag', string='Tags', help="Masukkan tag yang terkait dengan pasien")
    appointment_ids = fields.One2many('hospital.appointment', 'patient_id', string="Appointment", help="Riwayat atau daftar jadwal pemeriksaan untuk pasien ini.")
    appointment_count = fields.Integer(string='Appointment Count', compute='_compute_appointment_count', help="Jumlah jadwal pemeriksaan yang dimiliki pasien.")
    parent = fields.Char(string='Parent')
    marital_status = fields.Selection([('single','Single'),('married','Married'),('divorced','Divorced'),('widowed','Widowed')], string='Marital Status',tracking=True)
    partner_name = fields.Char(string='Partner Name')
    is_birthday = fields.Boolean(string='Birthday ?', compute='_compute_is_birthday')
    phone = fields.Integer(string='Phone')
    email = fields.Integer(string='Email')
    website = fields.Integer(string='website')
    
    
    
    
    

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids)

    @api.constrains('date_of_birth')
    def _check_date_of_birth(self):
        for record in self:
            if record.date_of_birth and record.date_of_birth > fields.Date.context_today(self):
                raise ValidationError("Tanggal lahir pasien harus kurang dari tanggal hari ini")

    @api.ondelete(at_uninstall=False)
    def _check_appointment(self):
        for record in self:
            if record.appointment_ids:
                raise ValidationError("Pasien tidak dapat dihapus karena memiliki jadwal pemeriksaan")

    @api.model
    def create(self,vals):
        if vals.get('patient_code', 'New') == 'New':
            vals['patient_code'] = self.env['ir.sequence'].next_by_code('hospital.patient.code') or 'New'
        vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).create(vals)

    def write(self,vals):
        if not self.ref and not vals.get('ref'):
            vals['ref'] = self.env['ir.sequence'].next_by_code('hospital.patient')
        return super(HospitalPatient, self).write(vals)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = date.today()
        for record in self:
            record.age = 0
            if record.date_of_birth:
                record.age = today.year - record.date_of_birth.year

    @api.depends('age')            
    def _inverse_compute_age(self):
        for record in self:
            record.date_of_birth = fields.Date.today() - relativedelta(years=record.age)    

    def _search_age(self,operator,value):
        date_of_birth = date.today() - relativedelta(years=value)
        return [('date_of_birth', operator, date_of_birth)]

    def name_get(self):
        return [(record.id, f"[{record.ref}] {record.name}") for record in self]

    @api.depends('date_of_birth')
    def _compute_is_birthday(self):
        for rec in self:
            is_birthday = False
            if rec.date_of_birth:
                today = date.today()
                if today.day == rec.date_of_birth.day and today.month == rec.date_of_birth.month:
                    is_birthday = True
            rec.is_birthday = is_birthday

    def action_view_appointments(self):
        return {
            'name': _('Appointments'),
            'res_model': 'hospital.appointment',
            'view_mode': 'list,form,calendar,activity',
            'context': {'default_patient_id': self.id},
            'domain': [('patient_id', '=', self.id)],
            'target': 'current',
            'type': 'ir.actions.act_window',
        }



