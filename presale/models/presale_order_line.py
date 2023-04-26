from odoo import api, fields, models


class PresaleOrderLine(models.Model):
    _name = 'presale.order.line'
    _description = 'Presales order line class'

    product_id = fields.Many2one('product.product', required=True)
    quantity = fields.Integer(default=0)
    price = fields.Float(compute="_compute_price", default=0, readonly=False)

    presale_id = fields.Many2one('presale.order')

    @api.depends('product_id', 'quantity')
    def _compute_price(self):
        for record in self:
            record.price = record.product_id['standard_price'] * record.quantity
