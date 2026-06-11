from pathlib import Path

from django.conf import settings
from django.test import TestCase
from django.urls import resolve, reverse

from .models import CelestialBody, MiningSpot, System


class ActionPanelRenderTests(TestCase):
	def setUp(self):
		self.system = System.objects.create(name="Sol")
		self.body = CelestialBody.objects.create(name="Jupiter", system=self.system)
		self.spot = MiningSpot.objects.create(name="Ring Sector 3", body=self.body)

	def test_action_panel_partial_is_present_on_system_and_body_detail_pages(self):
		system_response = self.client.get(reverse("system_detail", args=[self.system.pk]))
		body_response = self.client.get(reverse("body_detail", args=[self.body.pk]))

		self.assertContains(system_response, 'class="action-toggle"')
		self.assertContains(system_response, 'class="action-panel"')
		self.assertContains(body_response, 'class="action-toggle"')
		self.assertContains(body_response, 'class="action-panel"')

	def test_body_detail_renders_action_panel_hooks_and_add_items(self):
		response = self.client.get(reverse("body_detail", args=[self.body.pk]))

		self.assertContains(response, 'class="action-toggle"')
		self.assertContains(response, 'class="toggle-arrow"')
		self.assertContains(response, 'class="action-panel"')
		self.assertContains(response, 'class="add-menu"')
		self.assertContains(response, 'class="add-button"')
		self.assertContains(response, 'class="add-dropdown"')

		self.assertContains(response, "Edit Body")
		self.assertContains(response, "Delete Body")
		self.assertContains(response, "Add Moon")
		self.assertContains(response, "Add Mining Spot")

	def test_base_template_keeps_dropdown_visible_when_panel_is_open(self):
		base_template = Path(settings.BASE_DIR) / "templates" / "base.html"
		css = base_template.read_text(encoding="utf-8")

		self.assertIn(".action-panel.open", css)
		self.assertIn("overflow: visible;", css)
		self.assertIn(".add-dropdown.open", css)

	def test_reversed_urls_resolve_to_expected_view_names(self):
		url_map = {
			reverse("home"): "home",
			reverse("system_list"): "system_list",
			reverse("system_create"): "system_create",
			reverse("system_detail", args=[self.system.pk]): "system_detail",
			reverse("system_edit", args=[self.system.pk]): "system_edit",
			reverse("system_delete", args=[self.system.pk]): "system_delete",
			reverse("body_detail", args=[self.body.pk]): "body_detail",
			reverse("body_edit", args=[self.body.pk]): "body_edit",
			reverse("body_delete", args=[self.body.pk]): "body_delete",
			reverse("body_create_for_system", args=[self.system.pk]): "body_create_for_system",
			reverse("body_create_child", args=[self.body.pk]): "body_create_child",
			reverse("mining_spot_create_for_body", args=[self.body.pk]): "mining_spot_create_for_body",
			reverse("mining_spot_create_for_child", args=[self.body.pk]): "mining_spot_create_for_child",
			reverse("mining_spot_detail", args=[self.spot.pk]): "mining_spot_detail",
		}

		for url, view_name in url_map.items():
			self.assertEqual(resolve(url).view_name, view_name)

	def test_post_create_body_for_system_redirects_to_new_body_detail(self):
		response = self.client.post(
			reverse("body_create_for_system", args=[self.system.pk]),
			{
				"name": "Neptune",
				"system": self.system.pk,
				"notes": "Ice giant",
			},
		)

		new_body = CelestialBody.objects.get(name="Neptune")
		self.assertRedirects(response, reverse("body_detail", args=[new_body.pk]))
