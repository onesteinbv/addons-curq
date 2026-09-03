def pre_init_hook(env):
    crm_team_member_admin_sales = env.ref(
        "sales_team.crm_team_member_admin_sales", raise_if_not_found=False
    )
    if crm_team_member_admin_sales:
        crm_team_member_admin_sales.unlink()
