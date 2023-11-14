# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


# class SaleOrder(models.Model):
#     _inherit = "sale.order"
#
#     def action_create_rma(self):
#         res = super().action_create_rma()
#         Wizard = self.env['sale.order.rma.wizard']
#         line_vals = [
#             (0, 0, self._prepare_rma_wizard_line_vals(data))
#             for data in self.get_delivery_rma_data()]
#         wizard = Wizard.browse(res["res_id"]).location_id = self.env.ref(
#             "stock.stock_location_stock")
#         return res


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.multi
    def _compute_qty_delivered(self):
        super(SaleOrderLine, self)._compute_qty_delivered()
        lines = self.filtered(lambda sol: sol.qty_delivered_method == "on_demand")
        for line in lines:
            line.qty_delivered = sum([
                ln.qty_to_invoice
                for ln in self.env["rma"].search(
                    [("sale_line_id", "=", line.id)])])

    @api.multi
    def compute_qty_delivered(self):
        return self._compute_qty_delivered()
