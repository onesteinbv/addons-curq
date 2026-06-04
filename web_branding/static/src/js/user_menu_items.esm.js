import { patch } from "@web/core/utils/patch";
import {registry} from "@web/core/registry";
import {browser} from "@web/core/browser/browser";
import {_t} from "@web/core/l10n/translation";

import {tourService} from "@web_tour/tour_service/tour_service";

const menuItemRegistry = registry.category("user_menuitems");


function documentationItem() {
    const documentationURL = "https://docs.curq.nl";
    return {
        type: "item",
        id: "curq_documentation",
        description: _t("Documentation"),
        href: documentationURL,
        callback: () => {
            browser.open(documentationURL, "_blank");
        },
        sequence: 10,
    };
}


function supportItem() {
    const url = "https://curq.nl/support";
    return {
        type: "item",
        id: "curq_support",
        description: _t("Support"),
        href: url,
        callback: () => {
            browser.open(url, "_blank");
        },
        sequence: 20,
    };
}

patch(tourService, {
    async start(env, deps) {
        const res = await super.start(env, deps);
        menuItemRegistry.remove("web_tour.tour_enabled");
        return res;
    },
});

menuItemRegistry.add("curq_documentation", documentationItem);
menuItemRegistry.add("curq_support", supportItem);
