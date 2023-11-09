from odoo import fields, models


class RmaOperation(models.Model):
    _inherit = "rma.operation"

    for_sale = fields.Boolean("Operation for sale")
