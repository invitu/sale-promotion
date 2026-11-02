# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.point_of_sale.tests.test_frontend import TestPointOfSaleHttpCommon


@tagged("post_install", "-at_install")
class TestUi(TestPointOfSaleHttpCommon):
    def _start_bottle_tour(self, tour, discount, discount_mode):
        self.env["loyalty.program"].search([]).write({"active": False})
        products = self.env["product.product"].create(
            [
                {
                    "name": name,
                    "list_price": price,
                    "taxes_id": False,
                    "available_in_pos": True,
                }
                for name, price in (
                    ("Tea", 300),
                    ("Dessert", 200),
                    ("Own Bottle", 0),
                )
            ]
        )
        tea, bottle = products[0], products[2]
        self.env["loyalty.program"].create(
            {
                "name": "Own Bottle",
                "program_type": "promotion",
                "trigger": "auto",
                "applies_on": "current",
                "rule_ids": [
                    Command.create(
                        {
                            "product_ids": [Command.set(bottle.ids)],
                            "reward_point_mode": "unit",
                            "reward_point_amount": 1,
                        }
                    )
                ],
                "reward_ids": [
                    Command.create(
                        {
                            "reward_type": "discount",
                            "discount": discount,
                            "discount_mode": discount_mode,
                            "discount_applicability": "specific",
                            "discount_product_ids": [Command.set(tea.ids)],
                            "discount_unit_limit": True,
                            "required_points": 1,
                            "description": "Bottle discount",
                        }
                    )
                ],
            }
        )
        self.main_pos_config.write(
            {"tax_regime_selection": False, "use_pricelist": False}
        )
        self.main_pos_config.with_user(self.pos_user).open_ui()
        self.main_pos_config.current_session_id.set_opening_control(0, "")
        self.start_tour(
            f"/pos/ui?config_id={self.main_pos_config.id}", tour, login="pos_user"
        )

    def test_more_bottles_than_drinks(self):
        self._start_bottle_tour(
            "PosLoyaltyRewardUnitLimitMoreBottlesTour", 50, "per_order"
        )

    def test_one_discount_per_drink(self):
        self._start_bottle_tour(
            "PosLoyaltyRewardUnitLimitPerDrinkTour", 50, "per_order"
        )

    def test_percent_on_one_unit(self):
        self._start_bottle_tour("PosLoyaltyRewardUnitLimitPercentTour", 50, "percent")
