import {MessagingMenu} from "@mail/core/public_web/messaging_menu";
import {_t} from "@web/core/l10n/translation";
import {patch} from "@web/core/utils/patch";

patch(MessagingMenu.prototype, {
    get installationRequest() {
        return {
            ...super.installationRequest,
            displayName: _t("Install CURQ"),
        };
    },
});
