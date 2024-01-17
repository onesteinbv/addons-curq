# Copyright 2023 Onestein (<https://www.onestein.nl>)
# License OPL-1 (https://www.odoo.com/documentation/16.0/legal/licenses.html#odoo-apps).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class PontoLog(models.Model):
    _name = "ponto.log"
    _description = "Ponto Log"
    _rec_name = "url"
    _order = "id desc"

    url = fields.Char()
    params = fields.Char()
    res = fields.Text()
