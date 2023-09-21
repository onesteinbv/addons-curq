# Copyright 2023 Onestein
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import json
from odoo import _, fields, models


class PontoInterface(models.AbstractModel):
    _inherit = "ponto.interface"

    def _get_request(self, access_data, url, params):
        res = super()._get_request(access_data, url, params)
        self._log_response_in_action(url, params, res)
        return res

    def _log_response_in_action(
        self, url, params, res
    ):
        # Serializing json
        params = json.dumps(params)
        res = json.dumps(res, indent=4)
        self.env["ponto.log"].create(
            {
                "url": url,
                "params": params,
                "res": res,
            }
        )
