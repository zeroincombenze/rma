from odoo import models, api


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    def action_done(self):
        res = super().action_done()
        rmas = self.env["rma"].search(
            [("reception_move_id.picking_id", "in", [pick.id for pick in self]),
             ("for_sale", "=", True)])
        if not rmas:
            # Current picking(s) are not from RMA
            return res
        # Now search for all RMA on current line id to recalculate qty for sale
        for rma in rmas:
            all_rmas = self.env["rma"].search(
                [("sale_line_id", "=", rma.sale_line_id.id),
                 ("operation_id", "=", rma.operation_id.id),
                 ("state", "in", ["confirmed", "received"])])
            rma.sale_line_id.qty_delivered = sum(r.product_uom_qty for r in all_rmas)
        return res
