from odoo import http
from odoo.http import request

class ChartController(http.Controller):
    @http.route('/chart', type='http', auth='user')
    def chart(self, **kw):
        return request.render('your_module.chart_template')
