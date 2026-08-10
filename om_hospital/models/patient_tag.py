from odoo import models, fields,api

class PatientTag(models.Model):
    _name = "patient.tag"
    _description = "Patient Tag"
    _order = "name"

    name = fields.Char(string="Name",required=True)
    active = fields.Boolean(string="Active",default=True,copy=False)
    color = fields.Integer(string="Color")
    color_2 = fields.Char(string="Color 2")
    sequence = fields.Integer(string="Sequence")

    def copy(self,default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = f"Copy of {self.name}"
        default['sequence'] = 10
        return super(PatientTag, self).copy(default) 

    _sql_constraints = [
        ('unique_tag_name', 'unique(name,active)', 'The name must be unique'),
        ('check_sequence', 'check(sequence > 0)', 'The sequence must be greater than 0'),
    ]
    
    