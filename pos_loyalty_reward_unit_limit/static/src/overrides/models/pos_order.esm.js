/* Copyright 2026 INVITU (<https://www.invitu.com>)
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import {PosOrder} from "@point_of_sale/app/models/pos_order";
import {patch} from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    _isLineValidForUnitLimit(line, productIds) {
        return Boolean(
            line.get_quantity() > 0 &&
                line.isDiscountable() &&
                !line.is_reward_line &&
                !line.combo_parent_id &&
                !line.combo_line_ids?.length &&
                productIds.has(line.get_product().id)
        );
    },
    _getUnitLimitUnits(reward) {
        const productIds = new Set(reward.all_discount_product_ids.map((p) => p.id));
        const units = [];
        for (const line of this.get_orderlines()) {
            if (!this._isLineValidForUnitLimit(line, productIds)) {
                continue;
            }
            for (let i = 0; i < Math.floor(line.get_quantity()); i++) {
                units.push(line);
            }
        }
        const unitPrice = (line) => line.get_price_with_tax() / line.get_quantity();
        return units.sort((a, b) => unitPrice(b) - unitPrice(a));
    },
    _getUnitLimitClaimCount(reward) {
        // One claim creates one line per tax group, sharing its identifier code.
        return new Set(
            this.get_orderlines()
                .filter(
                    (line) => line.is_reward_line && line.reward_id?.id === reward.id
                )
                .map((line) => line.reward_identifier_code)
        ).size;
    },
    _getDiscountableOnSpecific(reward) {
        if (!reward.discount_unit_limit) {
            return super._getDiscountableOnSpecific(...arguments);
        }
        const line =
            this._getUnitLimitUnits(reward)[this._getUnitLimitClaimCount(reward)];
        if (!line) {
            return {discountable: 0, discountablePerTax: {}};
        }
        const taxKey = line.tax_ids
            .filter((t) => t.amount_type !== "fixed")
            .map((t) => t.id);
        return {
            discountable: line.get_price_with_tax() / line.get_quantity(),
            discountablePerTax: {[taxKey]: line.get_base_price() / line.get_quantity()},
        };
    },
    getClaimableRewards() {
        return super
            .getClaimableRewards(...arguments)
            .filter(
                ({reward}) =>
                    !reward.discount_unit_limit ||
                    this._getUnitLimitUnits(reward).length >
                        this._getUnitLimitClaimCount(reward)
            );
    },
});
