# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class LoyaltyReward(models.Model):
    _inherit = "loyalty.reward"

    discount_unit_limit = fields.Boolean(
        string="Limit to Eligible Units",
        help="Each claim discounts one unit of the eligible products, at most "
        "once per unit.",
    )

    @api.constrains("discount_unit_limit", "discount_applicability", "discount_mode")
    def _check_discount_unit_limit(self):
        for reward in self:
            if reward.discount_unit_limit and (
                reward.discount_applicability != "specific"
                or reward.discount_mode == "per_point"
            ):
                raise ValidationError(
                    self.env._(
                        "The limit to eligible units only applies to discounts "
                        "on specific products, not per point."
                    )
                )
