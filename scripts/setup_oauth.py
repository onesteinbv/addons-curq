import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--url")
@click.option("--realm")
@click.option("--client-id")
@click.option("--client-secret")
@click.option("--xml-id")
@click.option("--body")
@click.option("--role-id")
def main(env, url, realm, client_id, client_secret, xml_id, body, role_id):
    click.echo("Setup Keycloak... (%s)" % xml_id)
    module_container_accessibility = env.ref("base.module_container_accessibility")
    if module_container_accessibility.state != "installed":
        return click.echo(
            "Module `container_accessibility` must be installed for this script to work",
            err=True,
        )

    oauth_provider = env.ref(xml_id, raise_if_not_found=False)
    values = {
        "name": "Keycloak Onestein",
        "flow": "id_token_code",
        "token_map": "preferred_username:user_id",
        "client_id": client_id,
        "client_secret": client_secret,
        "enabled": True,
        "body": body,
        "css_class": "fa fa-fw fa-support text-primary",
        "auth_endpoint": "%s/realms/%s/protocol/openid-connect/auth" % (url, realm),
        "scope": "openid email",
        "token_endpoint": "%s/realms/%s/protocol/openid-connect/token" % (url, realm),
        "jwks_uri": "%s/realms/%s/protocol/openid-connect/certs" % (url, realm),
        "private": True,
        "role_id": env.ref(role_id).id,
    }

    if oauth_provider:
        oauth_provider.write(values)
    else:
        module, name = xml_id.split(".")
        new_provider = env["auth.oauth.provider"].create(values)
        env["ir.model.data"].create(
            {
                "module": module,
                "name": name,
                "model": "auth.oauth.provider",
                "res_id": new_provider.id,
            }
        )


if __name__ == "__main__":
    main()
