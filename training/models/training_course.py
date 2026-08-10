from odoo import models, fields, api

class TrainingCourse(models.Model):
    _name           = 'training.course'
    _description    = 'Training Course'

    name            = fields.Char(string='Course Name', required=True)
    description     = fields.Text(string='Description')
    user_id         = fields.Many2one(comodel_name='res.users', string='Penanggung Jawab')
    session_line    = fields.One2many(comodel_name='training.session', inverse_name='course_id', string='Sessions')

    
class TrainingSession(models.Model):
    _name           = 'training.session'
    _description    = 'Training Session'
    _inherit        = ['mail.thread', 'mail.activity.mixin']

    name            = fields.Char(string='Session Name',required=True)
    course_id       = fields.Many2one(comodel_name='training.course',string='Course Name',ondelete='cascade',required=True)
    start_date      = fields.Date(string='Start Date',required=True)
    duration        = fields.Float(string='Duration',required=True)
    seats           = fields.Integer(string='Seat',required=True)
    instruktur_id   = fields.Many2one(comodel_name='instruktur',string='Instruktur')
    peserta_ids     = fields.Many2many(comodel_name='peserta',string='Peserta')
    no_hp           = fields.Char(string='No Hp',related='instruktur_id.mobile',readonly=True)
    email           = fields.Char(string='Email',related='instruktur_id.email',readonly=True)
    jenis_kelamin   = fields.Selection(related='instruktur_id.jenis_kelamin',string='Jenis Kelamin',readonly=True)
    jml_peserta     = fields.Integer(string='Jumlah Peserta',compute='_compute_jml_peserta' )

    state = fields.Selection([('draft', 'Draft'),('confirm', 'Confirm'),('done', 'Done'),],string='Status',default='draft')

    @api.depends('peserta_ids')
    def _compute_jml_peserta(self):
        for rec in self:
            rec.jml_peserta = len(rec.peserta_ids)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirm'

    def action_done(self):
        for rec in self:
            rec.state = 'done'

    def action_draft(self):
        for rec in self:
            rec.state = 'draft'

    
    

    