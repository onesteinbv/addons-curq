import { ViewButton } from '@web/views/view_button/view_button';
import { WebClient } from "@web/webclient/webclient";
import { onMounted } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";
import { user } from "@web/core/user";

patch(WebClient.prototype, {
    setup() {
        super.setup();
        const actionService = useService("action");

        onMounted(async () => {
            const hasOnboardingGroup = await user.hasGroup("base_onboarding.onboarding_group");
            if (hasOnboardingGroup) {
                actionService.doAction("base_onboarding.onboarding_wizard_action", {
                    onClose: () => {
                        actionService.doAction({
                            type: "ir.actions.client", tag: "reload"
                        });
                    }
                });
            }
        });
    }
});

patch(ViewButton.prototype,{
    setup() {
        super.setup();
        this.uiService = useService("ui");
    },
    onClick(ev) {
        if (this.props.className && this.props.className.includes("base_onboarding_instant_block")) {
            this.uiService.block();
        }
        super.onClick(ev);
    }
});
