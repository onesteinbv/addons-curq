#!/bin/bash

USER_EMAIL=${USER_EMAIL:-$COMPANY_EMAIL}

# TODO: Removed '-c "$ODOO_RC"', they are not necessary as Odoo will automatically use the ODOO_RC env variable

python /odoo/scripts/set_base_url.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error --domain "$DOMAIN"

# TODO: Remove this in favor for the update_user.py script, kept for backward compatibility but should be removed in the future
if [[ -n "$ADMIN_USER_PWD" && "$CHANGE_ADMIN_USER_PWD" == "true" ]]; then
  python /odoo/scripts/change_password.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error --login admin --password "$ADMIN_USER_PWD"
fi

if [[ "$UPDATE_ADMIN_USER" == "true" ]]; then
  python /odoo/scripts/update_user.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error --xml-id "base.user_admin" --login "$ADMIN_USER_LOGIN" --password "$ADMIN_USER_PASSWORD"
fi

if [[ -n "$SMTP_HOST" && "$SETUP_SMTP" == "true" ]]; then
  python /odoo/scripts/setup_smtp.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error \
    --host "$SMTP_HOST" \
    --user "$SMTP_USER" \
    --password "$SMTP_PASSWORD" \
    --encryption "$SMTP_ENCRYPTION" \
    --port "$SMTP_PORT"
fi

if [[ -n "$INCOMING_MAIL_SERVER" && "$SETUP_INCOMING_MAIL" == "true" ]]; then
  flags=()
  if [[ "$INCOMING_MAIL_CONFIRM" == "true" ]]; then
    flags+=(--confirm)
  fi
  if [[ -n "$INCOMING_MAIL_PORT" ]]; then
    flags+=(--port "$INCOMING_MAIL_PORT")
  fi
  if [[ -n "$INCOMING_MAIL_SERVER_TYPE" ]]; then
    flags+=(--server-type "$INCOMING_MAIL_SERVER_TYPE")
  fi
  if [[ "$INCOMING_MAIL_SSL" == "true" ]]; then
    flags+=(--ssl)
  else
    flags+=(--no-ssl)
  fi

  python /odoo/scripts/setup_incoming_mail.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error --server "$INCOMING_MAIL_SERVER" --user "$INCOMING_MAIL_USER" --password "$INCOMING_MAIL_PASSWORD" "${flags[@]}"
fi

python /odoo/scripts/localize.py

# TODO: Remove capitalized True/False check, it's kept for backward compatibility but should be removed in favor of lowercase in the future
if [[ -n "$UNINSTALL_MODULES" && ( "$UNINSTALL_MODULES" == "True" || "$UNINSTALL_MODULES" == "true" ) ]]; then
  python /odoo/scripts/apply_modules.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error
else
  python /odoo/scripts/apply_modules.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error --dry-run
fi

python /odoo/scripts/uninstall_auto_install_modules.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error

python /odoo/scripts/remove_odoo_oauth_provider.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error

if [[ -n "$KEYCLOAK_URL" ]]; then
  python /odoo/scripts/setup_oauth.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error \
    --url "$KEYCLOAK_URL" --realm "$KEYCLOAK_REALM" \
    --client-id "$KEYCLOAK_CLIENT_ID" --client-secret "$KEYCLOAK_CLIENT_SECRET" \
    --xml-id="__export__.__oauth_provider_onestein" \
    --body="Support Login" \
    --template-user-id="base.user_admin"

  if [[ "${KEYCLOAK_RESELLER_REALM:-false}" != "false" ]]; then
    python /odoo/scripts/setup_oauth.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error \
      --url "$KEYCLOAK_URL" --realm "$KEYCLOAK_RESELLER_REALM" \
      --client-id "$KEYCLOAK_CLIENT_ID" --client-secret "$KEYCLOAK_RESELLER_CLIENT_SECRET" \
      --xml-id="__export__.__oauth_provider_reseller" \
      --body="${KEYCLOAK_RESELLER_BUTTON:-Reseller Login}" \
      --template-user-id="base.user_admin" \
      --group-id="container_accessibility.group_restricted"
  fi
fi

if [[ "$UPDATE_COMPANY" == "true" ]]; then
  python /odoo/scripts/update_company.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error --name "$COMPANY_NAME" --email "$COMPANY_EMAIL" --coc "$COMPANY_COC" --city "$COMPANY_CITY" --zip "$COMPANY_ZIP" --street "$COMPANY_STREET"
fi

if [[ "$PREPARE_CUSTOMER_USER" == "true" ]]; then
  python /odoo/scripts/prepare_customer_user.py -c "$ODOO_RC" -d "$DB_NAME" --log-level=error --email "$USER_EMAIL" --group-file /odoo/scripts/groups.txt
fi
