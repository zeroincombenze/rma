# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "On Consignment and for Evaluation RMA",
    "version": "12.0.0.1.0",
    "category": "RMA",
    "summary": "Return Merchandise Authorization (RMA) from Consignent/Evaluation",
    "author": "SHS-AV s.r.l.",
    "website": "https://www.zeroincombenze.it/crm",
    "development_status": "Beta",
    "license": "AGPL-3",
    "depends": [
        "rma_sale",
        "sale_order_type_plus",
        "sale_stock",
        "l10n_it_ddt",
    ],
    "data": [
        "data/rma_operation_data.xml",
        "views/rma_views.xml",
        "wizard/sale_order_rma_wizard_views.xml",
    ],
    "maintainer": "Antonio M. Vigliotti <antoniomaria.vigliotti@gmail.com>",
}
