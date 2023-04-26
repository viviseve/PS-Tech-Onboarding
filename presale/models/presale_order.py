from odoo import Command, api, fields, models


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
        max_id = len(self.env['presale.order'].search(domain=[]))
        for val in vals_List:
            str_id = str(max_id)
            str_id = '0' * max(0, 3 - len(str_id)) + str_id
            val['name'] = 'PS' + str_id
            max_id += 1
        return super().create(vals_List)

    def action_validate(self):
        self.state = 'confirmed'
        # Sales order creation
        for record in self:
            order_lines = []
            for item in record.order_line_ids:
                order_lines.append(Command.create({
                    'product_id': item.product_id.id,
                    'product_uom_qty': item.quantity,
                    'price_unit': item.price / item.quantity,
                }))
            order = {
                'name': record.name,
                'partner_id': record.customer_id.id,
                'order_line': order_lines,
                'state': 'sale',
                'presale_id': record.id,
            }
            record.sale_order_id = self.env["sale.order"].sudo().create(order)
        # Mail creation and delivery
        mail_values = {
            'subject': record.name,
            'email_to': record.customer_id.email,
            'body': f'Your presale order {record.name} has been validated',
            'body_html': f'Your presale order {record.name} has been validated',
            'res_id': record.id,
            'model': 'presale.order',
        }
        mail_id = self.env['mail.mail'].create(mail_values)
        mail_id.send()

        return True

    @api.model
    def archive_confirmed(self):
        presale_orders = self.env["presale.order"].search(
            domain=[('state', '=', 'confirmed')])
        presale_orders.active = False
