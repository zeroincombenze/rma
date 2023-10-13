# Copyright 2020 Tecnativa - Ernesto Tejeda
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Return Merchandise Authorization Management - Link with Sales",
    "version": "12.0.1.8.0",
    "category": "RMA",
    "summary": "Sale Order - Return Merchandise Authorization (RMA)",
    "author": "Tecnativa,SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/crm",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "rma",
        "sale_stock",
    ],
    "data": [
        "views/assets.xml",
        "views/report_rma.xml",
        "views/rma_views.xml",
        "views/sale_views.xml",
        "views/sale_portal_template.xml",
        "views/res_config_settings_views.xml",
        "wizard/sale_order_rma_wizard_views.xml",
    ],
    "maintainers": ["ernestotejeda"],
}
