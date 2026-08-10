
from odoo import models, fields, api


class ResGroups(models.Model):
    _inherit = 'res.groups'

    def get_application_groups(self, domain):
        excluded_group_ids = []

        for xmlid in (
            'project.group_project_task_dependencies',
            'stock.group_stock_picking_wave',
        ):
            try:
                excluded_group_ids.append(self.env.ref(xmlid).id)
            except ValueError:
                continue

        return super(ResGroups, self).get_application_groups(
            domain + [('id', 'not in', tuple(excluded_group_ids))]
        )