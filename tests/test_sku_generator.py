from odoo.tests import common, tagged

@tagged('post_install', '-at_install')
class TestSkuGenerator(common.TransactionCase):

    def setUp(self):
        super(TestSkuGenerator, self).setUp()
        self.SkuPattern = self.env['sku.pattern']
        self.ProductTemplate = self.env['product.template']
        self.ProductProduct = self.env['product.product']
        
        # Create a default pattern
        self.pattern = self.SkuPattern.create({
            'name': 'Test Pattern',
            'is_default': True,
            'component_ids': [
                (0, 0, {'component_type': 'fixed', 'fixed_value': 'TEST-', 'sequence': 1}),
                (0, 0, {'component_type': 'name', 'length': 3, 'case': 'upper', 'sequence': 2}),
                (0, 0, {'component_type': 'sequence', 'padding': 3, 'sequence': 3}),
            ]
        })

    def test_product_template_creation(self):
        """ Test SKU generation on product template creation """
        product = self.ProductTemplate.create({
            'name': 'Apple',
        })
        # Expecting: TEST-APP001 (assuming sequence starts at 1)
        # Note: Sequence depends on implementation. If global sequence, might be 1.
        self.assertTrue(product.default_code.startswith('TEST-APP'))
        self.assertTrue(len(product.default_code) >= 11)

    def test_manual_override(self):
        """ Test that manual SKU is not overwritten """
        product = self.ProductTemplate.create({
            'name': 'Banana',
            'default_code': 'MANUAL-SKU'
        })
        self.assertEqual(product.default_code, 'MANUAL-SKU')

    def test_bulk_generation(self):
        """ Test bulk wizard """
        product = self.ProductTemplate.create({
            'name': 'Cherry',
        })
        # Temporarily clear SKU to simulate bulk need (if it auto-generated, we clear it)
        product.default_code = False
        
        wizard = self.env['sku.generate.wizard'].with_context(active_ids=[product.id]).create({
            'target_model': 'product_template',
            'override_existing': False
        })
        wizard.action_generate()
        
        self.assertTrue(product.default_code)
        self.assertTrue(product.default_code.startswith('TEST-CHE'))

    def test_uniqueness(self):
        """ Test uniqueness check """
        # Create first product
        p1 = self.ProductTemplate.create({'name': 'Date'})
        sku1 = p1.default_code
        
        # Create second product with same name, should have different sequence
        p2 = self.ProductTemplate.create({'name': 'Date'})
        sku2 = p2.default_code
        
        self.assertNotEqual(sku1, sku2)
