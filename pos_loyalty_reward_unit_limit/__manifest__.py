# Copyright 2026 INVITU (<https://www.invitu.com>)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "POS Loyalty Reward Unit Limit",
    "summary": "Apply discount rewards at most once per eligible unit in the PoS",
    "version": "18.0.1.0.0",
    "development_status": "Alpha",
    "category": "Point of Sale",
    "website": "https://github.com/OCA/sale-promotion",
    "author": "INVITU, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": ["pos_loyalty", "loyalty_reward_unit_limit"],
    "assets": {
        "point_of_sale._assets_pos": [
            "pos_loyalty_reward_unit_limit/static/src/**/*.js",
        ],
        "web.assets_tests": [
            "pos_loyalty_reward_unit_limit/static/tests/tours/**/*",
        ],
    },
}
