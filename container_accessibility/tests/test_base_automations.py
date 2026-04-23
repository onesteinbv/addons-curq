from unittest.mock import patch
from odoo.tests import tagged
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestBaseAutomation(TransactionCase):
    """Test suite for container_accessibility.BaseAutomation overrides.

    Covers all five methods:
      1. _get_groups_to_restrict_trigger_choices
      2. _get_trigger_choices_to_restrict
      3. _check_trigger_choice_selection  (constrains)
      4. _get_trigger_selection_choices
      5. fields_get
      6. _update_cron
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Grab a partner model to use as the base-automation model target
        cls.partner_model = cls.env.ref("base.model_res_partner")

        # Restricted group
        cls.group_restricted = cls.env.ref(
            "container_accessibility.group_restricted"
        )

        # Create a restricted user (has group_restricted + group_system so he
        # can still write base.automation records)
        cls.restricted_user = cls.env["res.users"].create(
            {
                "name": "Restricted Tester",
                "login": "restricted_tester_ba@test.local",
                "groups_id": [
                    (4, cls.env.ref("base.group_system").id),
                    (4, cls.group_restricted.id),
                ],
            }
        )

        # A plain admin (super-user; does NOT have group_restricted)
        cls.admin_user = cls.env.ref("base.user_admin")

        # Minimal automation record created as admin – trigger "on_time" is
        # never restricted, so it always passes the constrains check.
        cls.automation = cls.env["base.automation"].create(
            {
                "name": "Test Automation",
                "model_id": cls.partner_model.id,
                "trigger": "on_time",
            }
        )

    # ------------------------------------------------------------------ #
    # 1. _get_groups_to_restrict_trigger_choices                           #
    # ------------------------------------------------------------------ #

    @tagged('post_install','-at_install')
    def test_get_groups_to_restrict_returns_list(self):
        """Return value must be a non-empty list."""
        result = self.env["base.automation"]._get_groups_to_restrict_trigger_choices()
        self.assertIsInstance(result, list)
        self.assertTrue(result, "Expected at least one group xml_id in the list")

    @tagged('post_install','-at_install')
    def test_get_groups_to_restrict_contains_expected_group(self):
        """The restricted group xml_id must be present."""
        result = self.env["base.automation"]._get_groups_to_restrict_trigger_choices()
        self.assertIn("container_accessibility.group_restricted", result)

    # ------------------------------------------------------------------ #
    # 2. _get_trigger_choices_to_restrict                                  #
    # ------------------------------------------------------------------ #
    @tagged('post_install','-at_install')
    def test_get_trigger_choices_to_restrict_returns_list(self):
        result = self.env["base.automation"]._get_trigger_choices_to_restrict()
        self.assertIsInstance(result, list)
        self.assertTrue(result)

    @tagged('post_install','-at_install')
    def test_get_trigger_choices_to_restrict_expected_values(self):
        expected = {"on_create_or_write", "on_unlink", "on_change", "on_webhook"}
        result = set(self.env["base.automation"]._get_trigger_choices_to_restrict())
        self.assertEqual(result, expected)

    # ------------------------------------------------------------------ #
    # 3. _check_trigger_choice_selection (constrains)                      #
    # ------------------------------------------------------------------ #

    @tagged('post_install','-at_install')
    def test_constrains_raises_for_restricted_user_with_restricted_trigger(self):
        """A restricted user must NOT be able to set a restricted trigger."""
        env_restricted = self.env["base.automation"].with_user(self.restricted_user)
        for trigger in ["on_create_or_write", "on_unlink", "on_change", "on_webhook"]:
            with self.subTest(trigger=trigger):
                with self.assertRaises(AccessError):
                    env_restricted.create(
                        {
                            "name": f"Bad Automation ({trigger})",
                            "model_id": self.partner_model.id,
                            "trigger": trigger,
                        }
                    )

    
    @tagged('post_install','-at_install')
    def test_constrains_passes_for_restricted_user_with_allowed_trigger(self):
        """A restricted user CAN set a trigger that is not in the restricted list."""
        env_restricted = self.env["base.automation"].with_user(self.restricted_user)
        # "on_time" is not in the restricted set
        record = env_restricted.create(
            {
                "name": "Allowed Automation (on_time)",
                "model_id": self.partner_model.id,
                "trigger": "on_time",
            }
        )
        self.assertTrue(record.exists())

    @tagged('post_install','-at_install')
    def test_constrains_passes_for_admin_with_restricted_trigger(self):
        """An admin user (not in group_restricted) can use any trigger freely."""
        env_admin = self.env["base.automation"].with_user(self.admin_user)
        record = env_admin.create(
            {
                "name": "Admin Automation (on_create_or_write)",
                "model_id": self.partner_model.id,
                "trigger": "on_create_or_write",
            }
        )
        self.assertTrue(record.exists())

    @tagged('post_install','-at_install')
    def test_constrains_raises_on_write_for_restricted_user(self):
        """Writing a restricted trigger on an existing record should also raise."""
        # Create with an allowed trigger as admin first
        record = self.env["base.automation"].create(
            {
                "name": "Automation for write test",
                "model_id": self.partner_model.id,
                "trigger": "on_time",
            }
        )
        env_restricted = record.with_user(self.restricted_user)
        with self.assertRaises(AccessError):
            env_restricted.write({"trigger": "on_unlink"})

    @tagged('post_install','-at_install')
    def test_constrains_passes_on_write_with_allowed_trigger_for_restricted_user(self):
        """Writing an allowed trigger on an existing record must succeed."""
        record = self.env["base.automation"].create(
            {
                "name": "Automation for allowed write test",
                "model_id": self.partner_model.id,
                "trigger": "on_time",
            }
        )
        env_restricted = record.with_user(self.restricted_user)
        # "on_time" is not restricted – staying on it (or updating name) must be fine
        env_restricted.write({"name": "Updated Name"})
        self.assertEqual(record.name, "Updated Name")

    # ------------------------------------------------------------------ #
    # 4. _get_trigger_selection_choices                                    #
    # ------------------------------------------------------------------ #

    @tagged('post_install','-at_install')
    def test_selection_choices_filtered_for_restricted_user(self):
        """Restricted user must not see the restricted trigger choices."""
        env_restricted = self.env["base.automation"].with_user(self.restricted_user)
        choices = env_restricted._get_trigger_selection_choices()
        restricted_keys = env_restricted._get_trigger_choices_to_restrict()
        returned_keys = [c[0] for c in choices]
        for key in restricted_keys:
            with self.subTest(key=key):
                self.assertNotIn(key, returned_keys)

    @tagged('post_install','-at_install')
    def test_selection_choices_not_filtered_for_admin(self):
        """Admin user must see the full (unfiltered) trigger choices list."""
        env_admin = self.env["base.automation"].with_user(self.admin_user)
        all_choices = env_admin._fields["trigger"]._description_selection(env_admin.env)
        filtered_choices = env_admin._get_trigger_selection_choices()
        # Admin is not in group_restricted so both lists must be identical
        self.assertEqual(all_choices, filtered_choices)

    @tagged('post_install','-at_install')
    def test_selection_choices_returns_list_of_tuples(self):
        """Each element of the returned choices must be a 2-tuple."""
        choices = self.env["base.automation"]._get_trigger_selection_choices()
        self.assertIsInstance(choices, list)
        for item in choices:
            with self.subTest(item=item):
                self.assertIsInstance(item, tuple)
                self.assertEqual(len(item), 2)

    @tagged('post_install','-at_install')
    def test_selection_choices_restricted_user_still_has_allowed_triggers(self):
        """Restricted user must still see triggers that are NOT restricted."""
        env_restricted = self.env["base.automation"].with_user(self.restricted_user)
        choices = env_restricted._get_trigger_selection_choices()
        restricted_keys = set(env_restricted._get_trigger_choices_to_restrict())
        returned_keys = {c[0] for c in choices}
        allowed_keys = returned_keys - restricted_keys
        # There should be at least some allowed triggers remaining
        self.assertTrue(
            allowed_keys,
            "Restricted user should still have some non-restricted trigger options",
        )

    # ------------------------------------------------------------------ #
    # 5. fields_get                                                        #
    # ------------------------------------------------------------------ #

    @tagged('post_install','-at_install')
    def test_fields_get_trigger_selection_filtered_for_restricted_user(self):
        """fields_get must inject the filtered trigger selection for restricted users."""
        env_restricted = self.env["base.automation"].with_user(self.restricted_user)
        result = env_restricted.fields_get(allfields=["trigger"])
        self.assertIn("trigger", result)
        selection_keys = [s[0] for s in result["trigger"]["selection"]]
        restricted_keys = env_restricted._get_trigger_choices_to_restrict()
        for key in restricted_keys:
            with self.subTest(key=key):
                self.assertNotIn(key, selection_keys)

    @tagged('post_install','-at_install')
    def test_fields_get_trigger_selection_unfiltered_for_admin(self):
        """fields_get must return the full trigger selection for admin users."""
        env_admin = self.env["base.automation"].with_user(self.admin_user)
        result = env_admin.fields_get(allfields=["trigger"])
        self.assertIn("trigger", result)
        # All trigger values should be present (nothing removed for admin)
        all_choices = env_admin._fields["trigger"]._description_selection(env_admin.env)
        self.assertEqual(result["trigger"]["selection"], all_choices)

    @tagged('post_install','-at_install')
    def test_fields_get_without_trigger_field_request(self):
        """fields_get must still work when 'trigger' is not requested."""
        env_admin = self.env["base.automation"].with_user(self.admin_user)
        result = env_admin.fields_get(allfields=["name"])
        # 'trigger' not requested → it should not appear in the result
        self.assertNotIn("trigger", result)
        self.assertIn("name", result)

    @tagged('post_install','-at_install')
    def test_fields_get_all_fields_does_not_break(self):
        """Calling fields_get with no field filter (all fields) must not raise."""
        env_restricted = self.env["base.automation"].with_user(self.restricted_user)
        try:
            result = env_restricted.fields_get()
        except Exception as exc:  # noqa: BLE001
            self.fail(f"fields_get() raised unexpectedly: {exc}")
        self.assertIn("trigger", result)

    # ------------------------------------------------------------------ #
    # 6. _update_cron                                                      #
    # ------------------------------------------------------------------ #

    @classmethod
    def _find_parent_update_cron_class(cls, record):
        """Traverse the registry MRO to find the first ancestor class that defines
        _update_cron, skipping container_accessibility's own override.
        Returns (parent_class, original_method) or (None, None)."""
        our_module = "odoo.addons.container_accessibility.models.base_automation"
        for klass in type(record).__mro__:
            if klass.__module__ != our_module and "_update_cron" in klass.__dict__:
                return klass, klass.__dict__["_update_cron"]
        return None, None

    @tagged('post_install', '-at_install')
    def test_update_cron_uses_sudo_for_restricted_system_user(self):
        """_update_cron must forward to super() with a sudo() self when the
        current user is both restricted (group_restricted) and a system admin."""
        record = self.env["base.automation"].create(
            {
                "name": "Cron Automation",
                "model_id": self.partner_model.id,
                "trigger": "on_time",
            }
        )
        env_restricted = record.with_user(self.restricted_user)

        parent_class, _ = self._find_parent_update_cron_class(env_restricted)
        if parent_class is None:
            self.skipTest("Could not locate parent _update_cron in the MRO")

        calls = []

        # Patch the actual parent class in the registry MRO so that super()
        # dispatch inside our override routes to our spy correctly.
        with patch.object(parent_class, "_update_cron", lambda self_arg: calls.append(self_arg)):
            env_restricted._update_cron()

        self.assertTrue(calls, "_update_cron was never forwarded to the parent class")
        called_self = calls[0]
        # sudo() sets env.su = True on the recordset it returns.
        self.assertTrue(
            called_self.env.su,
            "Expected env.su=True (sudo context) when a restricted+system user "
            "calls _update_cron",
        )

    @tagged('post_install', '-at_install')
    def test_update_cron_does_not_sudo_for_plain_admin(self):
        """_update_cron must NOT elevate to sudo for a plain admin (not restricted)."""
        record = self.env["base.automation"].create(
            {
                "name": "Cron Automation Admin",
                "model_id": self.partner_model.id,
                "trigger": "on_time",
            }
        )
        env_admin = record.with_user(self.admin_user)

        parent_class, _ = self._find_parent_update_cron_class(env_admin)
        if parent_class is None:
            self.skipTest("Could not locate parent _update_cron in the MRO")

        calls = []

        with patch.object(parent_class, "_update_cron", lambda self_arg: calls.append(self_arg)):
            env_admin._update_cron()

        self.assertTrue(calls)
        called_self = calls[0]
        # Admin is not restricted → sudo() must NOT have been called.
        self.assertFalse(
            called_self.env.su,
            "Plain admin should not be escalated to sudo in _update_cron",
        )

    @tagged('post_install', '-at_install')
    def test_update_cron_does_not_sudo_for_restricted_user_without_system_group(self):
        """A restricted user WITHOUT group_system must not have cron calls elevated."""
        restricted_only_user = self.env["res.users"].create(
            {
                "name": "Restricted No System",
                "login": "restricted_no_sys@test.local",
                "groups_id": [
                    (4, self.env.ref("base.group_user").id),
                    (4, self.group_restricted.id),
                ],
            }
        )
        record = self.env["base.automation"].create(
            {
                "name": "Cron Automation Restricted Only",
                "model_id": self.partner_model.id,
                "trigger": "on_time",
            }
        )
        env_restricted_only = record.with_user(restricted_only_user)

        parent_class, _ = self._find_parent_update_cron_class(env_restricted_only)
        if parent_class is None:
            self.skipTest("Could not locate parent _update_cron in the MRO")

        calls = []

        with patch.object(parent_class, "_update_cron", lambda self_arg: calls.append(self_arg)):
            env_restricted_only._update_cron()

        self.assertTrue(calls)
        called_self = calls[0]
        # Restricted without group_system → condition is False → no sudo.
        self.assertFalse(
            called_self.env.su,
            "Restricted user without group_system should not be escalated in _update_cron",
        )
