from odoo import Command
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


# The CI will run these tests after all the modules are installed,
# not right after installing the one defining it.


@tagged('post_install', '-at_install')
class PresaleTestCase(TransactionCase):

    @classmethod
    def setUpClass(cls):
        # add env on cls and many other things
        super(PresaleTestCase, cls).setUpClass()

        # create the data for each tests. By doing it in the setUpClass instead
        # of in a setUp or in each test case, we reduce the testing time and
        # the duplication of code.
        cls.presales_orders = cls.env['presale.order'].create([
            {'customer_id': 12, 'order_line_ids':
                [Command.create({
                    'product_id': 3,
                    'quantity': 2,
                })
                ],
             },
            {'customer_id': 4, 'order_line_ids':
                [Command.create({
                    'product_id': 6,
                    'quantity': 5,
                })
                ],
             },
        ])
        cls.wrong_presale_order = cls.env['presale.order'].create([
            {'customer_id': 12, },
        ])

    def test_confirm_order(self):
        """Test the confirmation of orders"""
        self.presales_orders.action_validate()
        self.assertRecordValues(self.presales_orders, [
            {'state': 'confirmed', },
            {'state': 'confirmed', },
        ])
