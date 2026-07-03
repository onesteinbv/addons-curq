import {xml} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {apps_menu_preferences} from "@web_responsive/components/apps_menu/apps_menu_preferences.esm"; // eslint-disable-line no-unused-vars

// Until https://github.com/OCA/web/pull/3569 is merged, we need to it this way.
const AppsMenuPreferences = registry.category("systray").get("AppMenuTheme").Component;
AppsMenuPreferences.template = xml``;
