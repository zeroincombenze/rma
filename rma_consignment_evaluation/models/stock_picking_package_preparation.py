from odoo import models, api


class StockPickingPackagePreparation(models.Model):
    _inherit = 'stock.picking.package.preparation'

    @api.multi
    def create_td_grouped_invoices(self):
        Invoice = self.env['account.invoice']
        grouped_invoices, references = super().create_td_grouped_invoices()
        for ddt in self:
            for line in ddt.line_ids:
                if (
                        not line.sale_line_id
                        or line.sale_line_id.qty_delivered_method != "on_demand"
                ):
                    continue

            group_key = ddt.get_td_group_key()
            if group_key not in grouped_invoices:
                inv_data = ddt._prepare_invoice()
                grouped_invoices[group_key] = Invoice.create(inv_data)

            invoice = grouped_invoices.get(group_key)
            ddt.invoice_id = invoice.id

            if invoice not in references:
                references[invoice] = ddt
            else:
                references[invoice] |= ddt

            origin = invoice.origin
            if origin and ddt.ddt_number not in origin.split(', '):
                invoice.update({
                    'origin': origin + ', ' + ddt.ddt_number
                })

            for line in ddt.line_ids:
                if (
                        line.product_uom_qty > 0
                        and line.sale_line_id
                        and line.sale_line_id.qty_delivered_method == "on_demand"
                ):
                    qty_to_invoice = (line.sale_line_id.qty_delivered
                                      - line.sale_line_id.qty_invoiced)
                    if qty_to_invoice:
                        line.invoice_line_create(
                            invoice.id,
                            qty_to_invoice)
            # Allow additional operations from ddt
            ddt.other_operations_on_ddt(invoice)
        return grouped_invoices, references
