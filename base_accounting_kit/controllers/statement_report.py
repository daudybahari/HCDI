# -*- coding: utf-8 -*-
###############################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#
#    Copyright (C) 2024-TODAY Cybrosys Technologies(<https://www.cybrosys.com>)
#    Author: Aysha Shalin (odoo@cybrosys.com)
#
#    You can modify it under the terms of the GNU LESSER
#    GENERAL PUBLIC LICENSE (LGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU LESSER GENERAL PUBLIC LICENSE (LGPL v3) for more details.
#
#    You should have received a copy of the GNU LESSER GENERAL PUBLIC
#    LICENSE (LGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import json
import inspect
from odoo import http
from odoo.http import content_disposition, request
from odoo.tools import html_escape


class XLSXReportController(http.Controller):
    """ Controller for xlsx report """

    @http.route(['/xlsx_report', '/xlsx_reports'], type='http', auth='user', methods=['POST', 'GET'],
                csrf=False)
    def get_report_xlsx(self, model=None, data=None, output_format='xlsx', report_name='Excel_Report',
                        report_action=None, **kw):
        """Generate an XLSX report based on the provided data and return it as a response."""
        uid = request.session.uid
        token = 'dummy-because-api-expects-one'

        # Extract arguments from kw or options if not passed directly
        if not model and 'model' in kw:
            model = kw.get('model')
        
        options = kw.get('options')
        if not data and options:
            try:
                data = json.loads(options)
            except Exception:
                data = options
        if not data and 'data' in kw:
            data = kw.get('data')

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception:
                pass

        if not report_name and 'report_name' in kw:
            report_name = kw.get('report_name')

        report_obj = request.env[model].with_user(uid) if model else None

        try:
            response = request.make_response(
                None,
                headers=[
                    ('Content-Type', 'application/vnd.ms-excel'),
                    ('Content-Disposition',
                     content_disposition((report_name or 'Report') + '.xlsx'))
                ]
            )
            if report_obj and hasattr(report_obj, 'get_xlsx_report'):
                sig = inspect.signature(report_obj.get_xlsx_report)
                param_count = len(sig.parameters)
                if param_count == 2:
                    report_obj.get_xlsx_report(data, response)
                else:
                    report_obj.get_xlsx_report(data, response, report_name, report_action)
            response.set_cookie('fileToken', token)
            return response
        except Exception as e:
            se = http.serialize_exception(e)
            error = {
                'code': 200,
                'message': 'Odoo Server Error',
                'data': se
            }
            return request.make_response(html_escape(json.dumps(error)))
