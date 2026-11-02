/* Copyright 2026 INVITU (<https://www.invitu.com>)
 * License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl). */

import * as Chrome from "@point_of_sale/../tests/tours/utils/chrome_util";
import * as PosLoyalty from "@pos_loyalty/../tests/tours/utils/pos_loyalty_util";
import * as ProductScreen from "@point_of_sale/../tests/tours/utils/product_screen_util";
import {registry} from "@web/core/registry";

const addProduct = (name, times = 1) =>
    Array.from({length: times}, () => ProductScreen.clickDisplayedProduct(name)).flat();

registry.category("web_tour.tours").add("PosLoyaltyRewardUnitLimitMoreBottlesTour", {
    steps: () =>
        [
            Chrome.startPoS(),
            addProduct("Tea"),
            addProduct("Own Bottle", 4),
            ProductScreen.selectedOrderlineHas("Own Bottle", "4.00"),
            PosLoyalty.hasRewardLine("Bottle discount", "-50.00"),
            PosLoyalty.orderTotalIs("250.00"),
            PosLoyalty.isRewardButtonHighlighted(false, false),
            Chrome.endTour(),
        ].flat(),
});

registry.category("web_tour.tours").add("PosLoyaltyRewardUnitLimitPerDrinkTour", {
    steps: () =>
        [
            Chrome.startPoS(),
            addProduct("Tea", 2),
            addProduct("Own Bottle", 2),
            ProductScreen.selectedOrderlineHas("Own Bottle", "2.00"),
            PosLoyalty.orderTotalIs("500.00"),
            addProduct("Dessert"),
            addProduct("Own Bottle"),
            ProductScreen.selectedOrderlineHas("Own Bottle", "3.00"),
            PosLoyalty.orderTotalIs("700.00"),
            Chrome.endTour(),
        ].flat(),
});

registry.category("web_tour.tours").add("PosLoyaltyRewardUnitLimitPercentTour", {
    steps: () =>
        [
            Chrome.startPoS(),
            addProduct("Tea", 2),
            addProduct("Own Bottle"),
            ProductScreen.selectedOrderlineHas("Own Bottle", "1.00"),
            PosLoyalty.hasRewardLine("Bottle discount", "-150.00"),
            PosLoyalty.orderTotalIs("450.00"),
            Chrome.endTour(),
        ].flat(),
});
