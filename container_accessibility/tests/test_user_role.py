from odoo.addons.base.tests.common import BaseCommon


class TestUserRole(BaseCommon):
    def _new_group(self, name, xml_id):
        new_group = self.env["res.groups"].create(
            {
                "name": name,
            }
        )
        module, name = xml_id.split(".")
        data = self.env["ir.model.data"].create(
            {
                "name": name,
                "model": "res.groups",
                "res_id": new_group.id,
                "module": module,
            }
        )
        return new_group, data

    def test_implied_by_text(self):
        groups = self.env.ref("base.group_system") + self.env.ref(
            "container_accessibility.group_restricted"
        )
        group_xml_ids = "base.group_system\ncontainer_accessibility.group_restricted"
        role = self.env["res.users.role"].create(
            {"name": "testrole", "implied_by_text": group_xml_ids}
        )

        self.assertEqual(role.implied_ids, groups)

    def test_implied_by_text_with_non_existing_group(self):
        groups = self.env.ref("base.group_system") + self.env.ref(
            "container_accessibility.group_restricted"
        )
        group_xml_ids = "base.group_system\ncontainer_accessibility.group_restricted\ncontainer_accessibility.group_non_existing"
        role = self.env["res.users.role"].create(
            {"name": "testrole", "implied_by_text": group_xml_ids}
        )

        self.assertEqual(role.implied_ids, groups)

        role.invalidate_recordset()

        # Implied by text should still contain the non existing group
        self.assertEqual(role.implied_by_text, group_xml_ids)

    def test_new_group(self):
        group_xml_ids = "base.group_system\ncontainer_accessibility.group_restricted\ncontainer_accessibility.group_non_existing"
        role = self.env["res.users.role"].create(
            {"name": "testrole", "implied_by_text": group_xml_ids}
        )
        new_group, _ = self._new_group(
            "New Group", "container_accessibility.group_non_existing"
        )
        self.assertEqual(
            self.ref("container_accessibility.group_non_existing"), new_group.id
        )
        self.assertIn(new_group, role.implied_ids)

    def test_delete_data(self):
        new_group, data = self._new_group(
            "New Group", "container_accessibility.group_non_existing"
        )
        new_group_2, data_2 = self._new_group(
            "New Group", "container_accessibility.group_non_existing_2"
        )
        new_group_3, data_3 = self._new_group(
            "New Group", "container_accessibility.group_non_existing_3"
        )

        group_xml_ids = "base.group_system\ncontainer_accessibility.group_restricted\ncontainer_accessibility.group_non_existing\ncontainer_accessibility.group_non_existing_2\ncontainer_accessibility.group_non_existing_3"
        role = self.env["res.users.role"].create(
            {"name": "testrole", "implied_by_text": group_xml_ids}
        )
        self.assertIn(new_group, role.implied_ids)
        self.assertIn(new_group_2, role.implied_ids)
        self.assertIn(new_group_3, role.implied_ids)

        data.unlink()
        self.assertNotIn(new_group, role.implied_ids)
        self.assertIn(new_group_2, role.implied_ids)
        self.assertIn(new_group_3, role.implied_ids)

        (data_2 + data_3).unlink()
        self.assertNotIn(new_group_2, role.implied_ids)
        self.assertNotIn(new_group_3, role.implied_ids)

    def test_xml_id_changed(self):
        new_group, data = self._new_group(
            "New Group", "container_accessibility.group_non_existing"
        )
        group_xml_ids = "base.group_system\ncontainer_accessibility.group_restricted\ncontainer_accessibility.group_non_existing"
        role = self.env["res.users.role"].create(
            {"name": "testrole", "implied_by_text": group_xml_ids}
        )
        self.assertIn(new_group, role.implied_ids)

        data.name = "group_non_existing_renamed"
        self.assertNotIn(new_group, role.implied_ids)
