# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class SaleOrderRmaWizard(models.TransientModel):
    _inherit = "sale.order.rma.wizard"

    def _domain_location_id(self):
        rma_loc = self.env['stock.warehouse'].search([]).mapped('rma_loc_id')
        return [('id', 'child_of', rma_loc.ids)]

    location_id = fields.Many2one(
        comodel_name='stock.location',
        string='RMA location',
        domain=_domain_location_id,
        default=lambda self: self.env.ref("stock.stock_location_stock").id
    )
    for_sale = fields.Boolean("Product for sale")

    @api.onchange('for_sale')
    def onchange_for_sale(self):
        if self.for_sale:
            # self.location_id = self.env.ref('stock.picking_type_out')
            self.location_id = self.env.ref('stock.stock_location_customers')
            for line in self.line_ids:
                line.operation_id = line.env.ref(
                    "rma_consignment_evaluation.rma_operation_sale")
        else:
            self.location_id = self.env.ref("stock.stock_location_stock")
            for line in self.line_ids:
                line.operation_id = line.env.ref(
                    "rma_consignment_evaluation.rma_operation_return")


class SaleOrderLineRmaWizard(models.TransientModel):
    _inherit = "sale.order.line.rma.wizard"

    lot_id = fields.Many2one(
        'stock.production.lot', 'Lot',
        compute='_compute_lot_id')

    @api.onchange('operation_id')
    def onchange_operation_id(self):
        if self.wizard_id.for_sale != self.operation_id.for_sale:
            self.operation_id = False
            return {'warning': {
                'title': _('Warning!'),
                'message': _('Invalid operation for RMA')
            }}

    @api.depends('product_id')
    def _compute_lot_id(self):
        for record in self:
            if hasattr(self.env["sale.order.line"], "lot_id"):
                # This code requires *sale_order_lot_selection* installed
                record.lot_id = record.order_id.order_line.filtered(
                    lambda ln: (
                        ln == record.sale_line_id
                        and ln.product_id == record.product_id
                        and ln.order_id == record.order_id)).lot_id

    def _prepare_rma_values(self):
        res = super()._prepare_rma_values()
        res["lot_id"] = self.lot_id.id if self.lot_id else False
        res["qty_to_invoice"] = self.quantity if self.operation_id.for_sale else 0.0
        return res
