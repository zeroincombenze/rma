# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class Rma(models.Model):
    _inherit = "rma"

    def _compute_qty_to_invoice(self):
        for rma in self:
            rma.qty_to_invoice = rma.product_uom_qty if rma.for_sale else 0.0

    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot',
    )
    original_order_not_sale = fields.Boolean(
        related="order_id.type_id.not_sale",
        string="Original order not for sale",
        store=True)
    qty_to_invoice = fields.Float(
        "Qty to Invoice",
        compute=_compute_qty_to_invoice)
    for_sale = fields.Boolean(
        related="operation_id.for_sale",
        string="RMA operation for sale",
        store=True)

    def _domain_location_id(self):
        res = super()._domain_location_id()
        if self.for_sale:
            return [("usage", "=", 'customer')]
        res.insert(0, "|")
        res.append(("id", "=", self.env.ref("stock.stock_location_stock").id))
        return res

    def _compute_can_be_refunded(self):
        super()._compute_can_be_refunded()
        for rma in self:
            if rma .original_order_not_sale:
                rma.can_be_refunded = False

    def _compute_can_be_returned(self):
        super()._compute_can_be_returned()
        for rma in self:
            if rma .original_order_not_sale:
                rma.can_be_returned = False

    def _compute_can_be_replaced(self):
        super()._compute_can_be_replaced()
        for rma in self:
            if rma .original_order_not_sale:
                rma.can_be_replaced = False

    def _compute_can_be_split(self):
        super()._compute_can_be_split()
        for rma in self:
            if rma .original_order_not_sale:
                rma.can_be_split = False

    @api.onchange('product_id')
    def _onchange_product_id_set_lot_domain(self):
        return {
            'domain': {'lot_id': [('product_id', '=', self.product_id.id)]}
        }

    def action_confirm(self):
        super().action_confirm()
        if self.sale_line_id.qty_delivered_method == "on_demand":
            self.sale_line_id._compute_qty_delivered()
