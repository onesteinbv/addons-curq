from odoo.tests import tagged
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestIrActionsServer(TransactionCase):
    """Test suite for container_accessibility.IrActionsServer overrides.

    Covers all four methods:
      1. _get_groups_to_restrict_state_choices
      2. _get_state_choices_to_restrict
      3. _check_trigger_state_selection  (constrains)
      4. _get_state_selection_choices
      5. fields_get
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Restricted group
        cls.group_restricted = cls.env.ref(
            "container_accessibility.group_restricted"
        )

        # Create a restricted user (has group_restricted + group_system so he
        # can still write ir.actions.server records)
        cls.restricted_user = cls.env["res.users"].create(
            {
                "name": "Restricted Server Action Tester",
                "login": "restricted_tester_ias@test.local",
                "groups_id": [
                    (4, cls.env.ref("base.group_system").id),
                    (4, cls.group_restricted.id),
                ],
            }
        )

        # A plain admin (super-user; does NOT have group_restricted)
        cls.admin_user = cls.env.ref("base.user_admin")

        # Grab a model to use as the server-action model target
        cls.partner_model = cls.env.ref("base.model_res_partner")

    # ------------------------------------------------------------------ #
    # 1. _get_groups_to_restrict_state_choices                            #
    # ------------------------------------------------------------------ #

    @tagged("post_install", "-at_install")
    def test_get_groups_to_restrict_returns_list(self):
        """Return value must be a non-empty list."""
        result = self.env[
            "ir.actions.server"
        ]._get_groups_to_restrict_state_choices()
        self.assertIsInstance(result, list)
        self.assertTrue(result, "Expected at least one group xml_id in the list")

    @tagged("post_install", "-at_install")
    def test_get_groups_to_restrict_contains_expected_group(self):
        """The restricted group xml_id must be present in the list."""
        result = self.env[
            "ir.actions.server"
        ]._get_groups_to_restrict_state_choices()
        self.assertIn("container_accessibility.group_restricted", result)

    # ------------------------------------------------------------------ #
    # 2. _get_state_choices_to_restrict                                   #
    # ------------------------------------------------------------------ #

    @tagged("post_install", "-at_install")
    def test_get_state_choices_to_restrict_returns_list(self):
        """Return value must be a non-empty list."""
        result = self.env["ir.actions.server"]._get_state_choices_to_restrict()
        self.assertIsInstance(result, list)
        self.assertTrue(result)

    @tagged("post_install", "-at_install")
    def test_get_state_choices_to_restrict_expected_values(self):
        """'code' must be the restricted state choice."""
        result = self.env["ir.actions.server"]._get_state_choices_to_restrict()
        self.assertIn("code", result)

    # ------------------------------------------------------------------ #
    # 3. _check_trigger_state_selection (constrains)                      #
    # ------------------------------------------------------------------ #

    @tagged("post_install", "-at_install")
    def test_constrains_raises_for_restricted_user_with_code_state(self):
        """A restricted user must NOT be able to create a server action with state='code'."""
        env_restricted = self.env["ir.actions.server"].with_user(
            self.restricted_user
        )
        with self.assertRaises(AccessError):
            env_restricted.create(
                {
                    "name": "Bad Server Action (code)",
                    "model_id": self.partner_model.id,
                    "state": "code",
                }
            )

    @tagged("post_install", "-at_install")
    def test_constrains_passes_for_restricted_user_with_allowed_state(self):
        """A restricted user CAN create a server action with a non-restricted state,
        provided it is linked to a base.automation (required by restrict_mixin domain)."""
        # Create the server action as admin first so it exists without restriction
        server_action = self.env["ir.actions.server"].create(
            {
                "name": "Allowed Server Action (object_write)",
                "model_id": self.partner_model.id,
                "state": "object_write",
            }
        )
        # Link it to a base.automation so restrict_mixin domain
        # [("base_automation_id", "!=", False)] is satisfied
        self.env["base.automation"].create(
            {
                "name": "Automation for allowed state test",
                "model_id": self.partner_model.id,
                "trigger": "on_time",
                "action_server_ids": [(4, server_action.id)],
            }
        )
        # Now a restricted user can write to it (non-restricted state → no AccessError)
        env_restricted = server_action.with_user(self.restricted_user)
        env_restricted.write({"name": "Allowed Server Action (object_write) - updated"})
        self.assertTrue(server_action.exists())

    @tagged("post_install", "-at_install")
    def test_constrains_passes_for_admin_with_code_state(self):
        """An admin user (not in group_restricted) can use the 'code' state freely."""
        env_admin = self.env["ir.actions.server"].with_user(self.admin_user)
        record = env_admin.create(
            {
                "name": "Admin Server Action (code)",
                "model_id": self.partner_model.id,
                "state": "code",
                "code": "record.write({})",
            }
        )
        self.assertTrue(record.exists())

    @tagged("post_install", "-at_install")
    def test_constrains_raises_on_write_for_restricted_user(self):
        """Writing state='code' on an existing record as a restricted user must raise."""
        # Create with an allowed state as admin
        record = self.env["ir.actions.server"].create(
            {
                "name": "Server Action for write test",
                "model_id": self.partner_model.id,
                "state": "object_write",
            }
        )
        # Link to a base.automation so the restrict_mixin domain is satisfied
        # and the restricted user can reach the constrains check
        self.env["base.automation"].create(
            {
                "name": "Automation for write test",
                "model_id": self.partner_model.id,
                "trigger": "on_time",
                "action_server_ids": [(4, record.id)],
            }
        )
        env_restricted = record.with_user(self.restricted_user)
        with self.assertRaises(AccessError):
            env_restricted.write({"state": "code"})

    @tagged("post_install", "-at_install")
    def test_constrains_passes_on_write_with_allowed_state_for_restricted_user(self):
        """Writing an allowed (non-restricted) state on a linked record must succeed."""
        record = self.env["ir.actions.server"].create(
            {
                "name": "Server Action for allowed write test",
                "model_id": self.partner_model.id,
                "state": "object_write",
            }
        )
        # Link to a base.automation so the restrict_mixin domain is satisfied
        self.env["base.automation"].create(
            {
                "name": "Automation for allowed write test",
                "model_id": self.partner_model.id,
                "trigger": "on_time",
                "action_server_ids": [(4, record.id)],
            }
        )
        env_restricted = record.with_user(self.restricted_user)
        # Updating the name while staying on a non-restricted state must be fine
        env_restricted.write({"name": "Updated Server Action Name"})
        self.assertEqual(record.name, "Updated Server Action Name")

    @tagged("post_install", "-at_install")
    def test_constrains_error_message_contains_human_readable_state(self):
        """The AccessError message must mention the human-readable label of the state."""
        env_restricted = self.env["ir.actions.server"].with_user(
            self.restricted_user
        )
        try:
            env_restricted.create(
                {
                    "name": "Error Message Test",
                    "model_id": self.partner_model.id,
                    "state": "code",
                }
            )
            self.fail("AccessError was not raised")
        except AccessError as exc:
            self.assertIn(
                "restricted",
                str(exc).lower(),
                "Error message should mention restriction",
            )

    # ------------------------------------------------------------------ #
    # 4. _get_state_selection_choices                                     #
    # ------------------------------------------------------------------ #

    @tagged("post_install", "-at_install")
    def test_state_selection_choices_filtered_for_restricted_user(self):
        """Restricted user must not see the restricted state choices."""
        env_restricted = self.env["ir.actions.server"].with_user(
            self.restricted_user
        )
        choices = env_restricted._get_state_selection_choices()
        restricted_keys = env_restricted._get_state_choices_to_restrict()
        returned_keys = [c[0] for c in choices]
        for key in restricted_keys:
            with self.subTest(key=key):
                self.assertNotIn(key, returned_keys)

    @tagged("post_install", "-at_install")
    def test_state_selection_choices_not_filtered_for_admin(self):
        """Admin user must see the full (unfiltered) state choices list."""
        env_admin = self.env["ir.actions.server"].with_user(self.admin_user)
        all_choices = env_admin._fields["state"]._description_selection(
            env_admin.env
        )
        filtered_choices = env_admin._get_state_selection_choices()
        # Admin is not in group_restricted so both lists must be identical
        self.assertEqual(all_choices, filtered_choices)

    @tagged("post_install", "-at_install")
    def test_state_selection_choices_returns_list_of_tuples(self):
        """Each element of the returned choices must be a 2-tuple."""
        choices = self.env["ir.actions.server"]._get_state_selection_choices()
        self.assertIsInstance(choices, list)
        for item in choices:
            with self.subTest(item=item):
                self.assertIsInstance(item, tuple)
                self.assertEqual(len(item), 2)

    @tagged("post_install", "-at_install")
    def test_state_selection_choices_restricted_user_still_has_allowed_states(self):
        """Restricted user must still see states that are NOT restricted."""
        env_restricted = self.env["ir.actions.server"].with_user(
            self.restricted_user
        )
        choices = env_restricted._get_state_selection_choices()
        restricted_keys = set(env_restricted._get_state_choices_to_restrict())
        returned_keys = {c[0] for c in choices}
        allowed_keys = returned_keys - restricted_keys
        self.assertTrue(
            allowed_keys,
            "Restricted user should still have some non-restricted state options",
        )

    @tagged("post_install", "-at_install")
    def test_state_selection_choices_code_absent_for_restricted_user(self):
        """'code' state must specifically be absent for a restricted user."""
        env_restricted = self.env["ir.actions.server"].with_user(
            self.restricted_user
        )
        choices = env_restricted._get_state_selection_choices()
        returned_keys = [c[0] for c in choices]
        self.assertNotIn(
            "code",
            returned_keys,
            "Restricted user must not see 'code' in state selection choices",
        )

    @tagged("post_install", "-at_install")
    def test_state_selection_choices_code_present_for_admin(self):
        """'code' state must be present for an admin user."""
        env_admin = self.env["ir.actions.server"].with_user(self.admin_user)
        choices = env_admin._get_state_selection_choices()
        returned_keys = [c[0] for c in choices]
        self.assertIn(
            "code",
            returned_keys,
            "Admin must see 'code' in state selection choices",
        )

    # ------------------------------------------------------------------ #
    # 5. fields_get                                                        #
    # ------------------------------------------------------------------ #

    @tagged("post_install", "-at_install")
    def test_fields_get_state_selection_filtered_for_restricted_user(self):
        """fields_get must inject the filtered state selection for restricted users."""
        env_restricted = self.env["ir.actions.server"].with_user(
            self.restricted_user
        )
        result = env_restricted.fields_get(allfields=["state"])
        self.assertIn("state", result)
        selection_keys = [s[0] for s in result["state"]["selection"]]
        restricted_keys = env_restricted._get_state_choices_to_restrict()
        for key in restricted_keys:
            with self.subTest(key=key):
                self.assertNotIn(key, selection_keys)

    @tagged("post_install", "-at_install")
    def test_fields_get_state_selection_unfiltered_for_admin(self):
        """fields_get must return the full state selection for admin users."""
        env_admin = self.env["ir.actions.server"].with_user(self.admin_user)
        result = env_admin.fields_get(allfields=["state"])
        self.assertIn("state", result)
        all_choices = env_admin._fields["state"]._description_selection(
            env_admin.env
        )
        self.assertEqual(result["state"]["selection"], all_choices)

    @tagged("post_install", "-at_install")
    def test_fields_get_without_state_field_request(self):
        """fields_get must still work when 'state' is not requested."""
        env_admin = self.env["ir.actions.server"].with_user(self.admin_user)
        result = env_admin.fields_get(allfields=["name"])
        # 'state' not requested → it should not appear in the result
        self.assertNotIn("state", result)
        self.assertIn("name", result)

    @tagged("post_install", "-at_install")
    def test_fields_get_all_fields_does_not_break(self):
        """Calling fields_get with no field filter (all fields) must not raise."""
        env_restricted = self.env["ir.actions.server"].with_user(
            self.restricted_user
        )
        try:
            result = env_restricted.fields_get()
        except Exception as exc:  # noqa: BLE001
            self.fail(f"fields_get() raised unexpectedly: {exc}")
        self.assertIn("state", result)

    @tagged("post_install", "-at_install")
    def test_fields_get_state_selection_is_list_of_tuples(self):
        """The 'state' selection returned by fields_get must be a list of 2-tuples."""
        env_restricted = self.env["ir.actions.server"].with_user(
            self.restricted_user
        )
        result = env_restricted.fields_get(allfields=["state"])
        self.assertIn("state", result)
        selection = result["state"]["selection"]
        self.assertIsInstance(selection, list)
        for item in selection:
            with self.subTest(item=item):
                self.assertIsInstance(item, tuple)
                self.assertEqual(len(item), 2)

    @tagged("post_install", "-at_install")
    def test_fields_get_code_absent_in_state_selection_for_restricted_user(self):
        """fields_get must not include 'code' in the state selection for a restricted user."""
        env_restricted = self.env["ir.actions.server"].with_user(
            self.restricted_user
        )
        result = env_restricted.fields_get(allfields=["state"])
        selection_keys = [s[0] for s in result["state"]["selection"]]
        self.assertNotIn(
            "code",
            selection_keys,
            "fields_get must exclude 'code' state for restricted user",
        )

    @tagged("post_install", "-at_install")
    def test_fields_get_code_present_in_state_selection_for_admin(self):
        """fields_get must include 'code' in the state selection for an admin user."""
        env_admin = self.env["ir.actions.server"].with_user(self.admin_user)
        result = env_admin.fields_get(allfields=["state"])
        selection_keys = [s[0] for s in result["state"]["selection"]]
        self.assertIn(
            "code",
            selection_keys,
            "fields_get must include 'code' state for admin user",
        )
