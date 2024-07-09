import base64

import os
import tempfile
from datetime import datetime, timedelta

import pandas as pd
from odoo import fields, models, api
from odoo.exceptions import ValidationError, RedirectWarning



class CustomNoti(models.TransientModel):
    _name = "custom_noti"
    _description = "Import thời khóa biểu"

    noti_html = fields.Char('Thông tin import', readonly=True)
