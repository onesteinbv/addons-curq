import { WebClient } from "@web/webclient/webclient";
import { onMounted } from "@odoo/owl";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";



patch(WebClient.prototype, {
    setup() {
        super.setup();
        const actionService = useService("action");
        const orm = useService("orm");

        onMounted(async () => {
            const releaseNoteAction = await orm.call(
                "release.note.wizard", "action_open_release_notes"
            );

            if (!releaseNoteAction) {
                return;
            }

            actionService.doAction(releaseNoteAction, {
                onClose: async () => {
                    await orm.call("release.note.wizard", "mark_release_notes_as_read");
                    actionService.doAction({
                        type: "ir.actions.client", tag: "reload"
                    });
                }
            });
        });
    }
});
