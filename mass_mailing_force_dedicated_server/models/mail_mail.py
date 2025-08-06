import logging

from odoo import models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class MailMail(models.Model):
    _inherit = "mail.mail"

    def _send(
        self,
        auto_commit=False,
        raise_exception=False,
        smtp_session=None,
        alias_domain_id=False,
        mail_server=False,
        post_send_callback=None,
    ):
        if self.mailing_id:
            try:
                self.mailing_id._force_dedicated_server()
            except UserError as e:
                if raise_exception:
                    raise e
                failure_reason = str(e)
                # We don't care to log if exception will be raised
                _logger.info("Refused to send mailing %s", failure_reason)
                self.write({"state": "exception", "failure_reason": failure_reason})
        return super()._send(
            auto_commit,
            raise_exception,
            smtp_session,
            alias_domain_id,
            mail_server,
            post_send_callback,
        )
