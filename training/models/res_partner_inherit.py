from odoo import models, fields, api



class ResPartner(models.Model):
    _inherit = 'res.partner'

    provinsi_id = fields.Many2one(comodel_name='provinsi', string='Provinsi')
    kota_id = fields.Many2one(comodel_name='kota', string='Kota')
    kecamatan_id = fields.Many2one(comodel_name='kecamatan', string='Kecamatan')
    desa_id = fields.Many2one(comodel_name='desa', string='Desa')
    jenis_kelamin = fields.Selection([('laki-laki', 'Laki-laki'), ('perempuan', 'Perempuan')], string='Jenis Kelamin')

