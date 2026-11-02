# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.exceptions import ValidationError
from odoo.fields import Command
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestLoyaltyRewardUnitLimit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.program = cls.env["loyalty.program"].create(
            {
                "name": "Own bottle",
                "program_type": "promotion",
                "reward_ids": [
                    Command.create(
                        {
                            "reward_type": "discount",
                            "discount": 50,
                            "discount_mode": "per_order",
                            "discount_applicability": "specific",
                            "discount_unit_limit": True,
                        }
                    )
                ],
            }
        )
        cls.reward = cls.program.reward_ids

    def test_only_specific_amount_or_percent(self):
        self.reward.discount_mode = "percent"
        for vals in (
            {"discount_applicability": "order"},
            {"discount_applicability": "cheapest"},
            {"discount_mode": "per_point"},
        ):
            with self.assertRaises(ValidationError), self.cr.savepoint():
                self.reward.write(vals)
            self.env.invalidate_all()
