ALTER TABLE `map_campaign`.`livetech_customers`
    ADD COLUMN `cm_cross_sell_k_protect` VARCHAR(100) AFTER `cm_cross_sell_direct`,
    ADD COLUMN `cm_cross_sell_win_back` VARCHAR(100) AFTER `cm_cross_sell_direct`;
