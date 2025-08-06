from odoo import api, models


class AuditlogAutovacuum(models.TransientModel):
    _inherit = "auditlog.autovacuum"

    @api.model
    def autovacuum(self, days, chunk_size=None):
        return super(AuditlogAutovacuum, self.sudo()).autovacuum(
            days, chunk_size=chunk_size
        )
