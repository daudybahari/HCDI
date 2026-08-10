from odoo import models, fields, api



class Provinsi(models.Model):
    _name = 'provinsi'
    _description = 'Provinsi'

    kode = fields.Char(string='Kode Provinsi', required=True)
    name = fields.Char(string='Nama Provinsi', required=True)
    singkatan = fields.Char(string='Singkatan')
    description = fields.Char(string='Descripsi')

    kota_ids = fields.One2many(comodel_name='kota', inverse_name='provinsi_id', string='Kota')
    
   


class Kota(models.Model):
    _name = 'kota'
    _description = 'Kota'

    kode = fields.Char(string='Kode Kota', required=True)
    name = fields.Char(string='Nama Kota', required=True)
    singkatan = fields.Char(string='Singkatan')
    description = fields.Char(string='Descripsi')

    kecamatan_ids = fields.One2many(comodel_name='kecamatan', inverse_name='kota_id', string='Kecamatan')
    provinsi_id = fields.Many2one(comodel_name='provinsi', string='Provinsi')
    
    




class Kecamatan(models.Model):
    _name = 'kecamatan'
    _description = 'Kecamatan'

    kode = fields.Char(string='Kode Kecamatan', required=True)
    name = fields.Char(string='Nama Kecamatan', required=True)
    singkatan = fields.Char(string='Singkatan')
    description = fields.Char(string='Descripsi')

    desa_ids = fields.One2many(comodel_name='desa', inverse_name='kecamatan_id', string='Desa')
    kota_id = fields.Many2one(comodel_name='kota', string='Kota')
    
    
    


class Desa(models.Model):
    _name = 'desa'
    _description = 'Desa'

    kode = fields.Char(string='Kode Desa', required=True)
    name = fields.Char(string='Nama Desa', required=True)
    singkatan = fields.Char(string='Singkatan')
    description = fields.Char(string='Descripsi')

    kecamatan_id = fields.Many2one(comodel_name='kecamatan', string='Kecamatan')