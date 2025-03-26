import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--server")
@click.option("--user")
@click.option("--password")
@click.option("--confirm", is_flag=True, default=False)
def main(env, server, user, password, confirm):
    click.echo("Setup Incoming mail (IMAP)...")
    module_container_accessibility = env.ref("base.module_container_accessibility")
    if module_container_accessibility.state != "installed":
        return click.echo(
            "Module `container_accessibility` must be installed for this script to work",
            err=True,
        )

    module_fetchmail_notify_error_to_sender = env.ref(
        "base.module_fetchmail_notify_error_to_sender"
    )
    if module_fetchmail_notify_error_to_sender.state != "installed":
        return click.echo(
            "Module `fetchmail_notify_error_to_sender` must be installed for this script to work",
            err=True,
        )
    fetchmail_server_model = env["fetchmail.server"]
    fetchmail_server = fetchmail_server_model.search([("private", "=", True)])
    values = {
        "name": "Default Incoming Mail Server",
        "server_type": "imap",
        "server": server,
        "port": 993,
        "is_ssl": True,
        "priority": 9999999,
        "user": user,
        "password": password,
        "private": True,
        "error_notice_template_id": env.ref(
            "fetchmail_notify_error_to_sender.email_template_error_notice"
        ).id,
    }
    if fetchmail_server:
        fetchmail_server.write(values)
    else:
        fetchmail_server = fetchmail_server_model.create(values)
        if confirm:
            fetchmail_server.button_confirm_login()

    config_parameter = env["ir.config_parameter"]
    config_parameter.set_param("base_setup.default_external_email_server", "True")
    mail_domain = user.split("@")[1]
    config_parameter.set_param("mail.catchall.domain", mail_domain)
    config_parameter.set_param("mass_mailing_force_dedicated_server.enabled", "True")


if __name__ == "__main__":
    main()
