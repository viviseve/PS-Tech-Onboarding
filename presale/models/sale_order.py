from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    presale_id = fields.Many2one('presale.order')
