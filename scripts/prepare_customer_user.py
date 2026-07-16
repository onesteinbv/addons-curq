import click
import click_odoo


@click.command()
@click_odoo.env_options(default_log_level="error")
@click.option("--login", default="")
def main(env, login):
    click.echo("Update customer user...")
    customer_user = env.ref(
        "base_customer_user.user_customer", raise_if_not_found=False
    )
    if not customer_user:
        return click.echo("Customer user doesn't exists", err=True)

    if customer_user.login == "customer_user":
        customer_user.write({"login": login, "lang": "nl_NL"})
        # Use the login as email to ensure the user can receive the reset password email
        customer_user.partner_id.write({"email": login})

    customer_user.role_id = env.ref("container_accessibility.role_manager")
    if customer_user.state == "new":
        customer_user.groups_id += env.ref("base_onboarding.onboarding_group")
        try:
            customer_user.action_reset_password()
        except Exception as e:
            click.echo(click.style(str(e), fg="red"))


if __name__ == "__main__":
    main()
