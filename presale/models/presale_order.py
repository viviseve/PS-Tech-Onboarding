from odoo import Command, _, api, fields, models
from odoo.exceptions import UserError


class PresaleOrder(models.Model):
    _name = 'presale.order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Presales order class'

    name = fields.Char(readonly=True)
    customer_id = fields.Many2one('res.partner', required='True')
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('confirmed', 'Confirmed'),
        ],
        required=True,
        default='draft'
    )
    active = fields.Boolean(default=True)

    order_line_ids = fields.One2many(
        'presale.order.line', 'presale_id', required=True)
    sale_order_id = fields.Many2one('sale.order')

    @api.model_create_multi
    def create(self, vals_List):
        for vals in vals_List:
            next_val = self.env["ir.sequence"].next_by_code("presale.order.seq") or _("New")
            vals['name'] = next_val
        return super().create(vals_List)

    def action_validate(self):
        for presale_order in self:
            presale_order.state = 'confirmed'
            # Sales order creation
            order_lines = []
            if presale_order.order_line_ids == []:
                raise UserError(_('An empty order cannot be confirmed'))
            for presale_order_line in presale_order.order_line_ids:
                order_lines.append(Command.create({
                    'product_id': presale_order_line.product_id.id,
                    'product_uom_qty': presale_order_line.quantity,
                }))
            order = {
                'name': presale_order.name,
                'partner_id': presale_order.customer_id.id,
                'order_line': order_lines,
                'presale_id': presale_order.id,
            }
            presale_order.sale_order_id = self.env["sale.order"].create(order)
            # Mail creation and delivery
            mail_values = {
                'subject': presale_order.name,
                'email_to': presale_order.customer_id.email,
                'body': _(f'Your presale order {presale_order.name} has been validated'),
                'body_html': _(f'Your presale order {presale_order.name} has been validated'),
                'res_id': presale_order.id,
                'model': 'presale.order',
            }
            mail_id = self.env['mail.mail'].create(mail_values)
            mail_id.send()
        return True

    def archive_confirmed(self):
        presale_orders = self.env["presale.order"].search(
            domain=[('state', '=', 'confirmed')])
        presale_orders.active = False
