import datetime
from odoo import models, fields,api
from odoo.exceptions import ValidationError
from dateutil import relativedelta

class CancelAppointmentWizard(models.TransientModel):
    _name = "cancel.appointment.wizard"
    _description = "Cancel Appointment Wizard"

    @api.model
    def default_get(self, fields_list):
        res = super(CancelAppointmentWizard, self).default_get(fields_list)
        res['cancel_date'] = fields.Date.context_today(self)
        if self.env.context.get('active_id'):
            res['appointment_id'] = self.env.context.get('active_id')
        
        # Set default reason
        if self.env.context.get('default_reason'):
            res['reason'] = self.env.context.get('default_reason')
        else:
            res['reason'] = 'Cancel'
            
        return res

    appointment_id = fields.Many2one('hospital.appointment', string="Appointment", domain=[('state', '=', 'draft'),('priority', 'in', ('0','1',False))])
    reason = fields.Text(string="Reason", required=True)
    cancel_date = fields.Date(string="Cancel Date", default=fields.Date.context_today)

    def action_cancel(self):
        cancel_day = self.env['ir.config_parameter'].get_param('om_hospital.cancel_day')
        allowed_date = self.appointment_id.booking_date - relativedelta.relativedelta(days=int(cancel_day))
        if allowed_date < date.today():
            raise ValidationError(_('Sorry, cancellation is not allowed for this booking !'))
        self.appointment_id.state = 'cancel'
        return{
            'type': 'ir.actions.client',
            'tag': 'reload',
        }