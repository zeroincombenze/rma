from odoo import fields, models


class ReturnPicking(models.TransientModel):
    _inherit = "stock.return.picking"

    def _create_returns(self):
        # Standard 'return wizard' returns new_picking.id and picking_type_id
        res = super()._create_returns()

        picking_returned = self.env["stock.picking"].browse(res[0])
        move_line_ids_to_update = picking_returned.move_line_ids.ids
        moves_with_lot = self.product_return_moves.mapped(
            "move_id.move_line_ids"
        ).filtered(lambda ln: ln.lot_id)

        for line in moves_with_lot:
            move_line = fields.first(
                picking_returned.move_line_ids.filtered(
                    lambda ln: ln.product_id == line.product_id
                    and ln.id in move_line_ids_to_update
                )
            )
            # Here quantity test is not important because RMA has just 1 product
            if (
                    move_line and not move_line.lot_id
                    # and (move_line.product_uom_qty == line.qty_done)
            ):
                move_line.lot_id = line.lot_id
                move_line.qty_done = min(move_line.product_uom_qty,
                                         line.lot_id.product_qty)
            move_line_ids_to_update.remove(move_line.id)

        return res
