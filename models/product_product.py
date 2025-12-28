from odoo import models, api, fields
import logging

_logger = logging.getLogger(__name__)

class ProductProduct(models.Model):
    _inherit = 'product.product'

    auto_generated_sku = fields.Boolean(string='Auto Generated SKU', default=False)

    @api.model
    def create(self, vals):
        """Override create to auto-generate SKU if not provided."""
        product = super(ProductProduct, self).create(vals)
        
        # Auto-generate SKU only if default_code is not provided
        if not vals.get('default_code'):
            product.generate_sku()
        
        return product

    def generate_sku(self):
        """
        Generate SKU for this product variant.
        Handles uniqueness validation and logging.
        """
        self.ensure_one()
        pattern = self.env['sku.pattern'].search([('is_default', '=', True)], limit=1)
        
        if not pattern:
            _logger.warning("No default SKU pattern found for product variant %s", self.id)
            return
        
        new_sku = pattern.generate_sku_for_product(self)
        
        if not new_sku:
            _logger.warning("Empty SKU generated for product variant %s", self.id)
            return
        
        # Check uniqueness and assign
        if self._check_sku_uniqueness(new_sku):
            self.write({
                'default_code': new_sku,
                'auto_generated_sku': True
            })
        else:
            _logger.warning(
                "Duplicate SKU '%s' detected for product variant %s (%s). SKU not assigned.",
                new_sku, self.id, self.name
            )
    
    def _check_sku_uniqueness(self, sku):
        """
        Check if SKU is unique across all products and templates.
        
        :param sku: SKU string to check
        :return: True if unique, False otherwise
        """
        if not sku:
            return False
        
        domain = [('default_code', '=', sku), ('id', '!=', self.id)]
        
        # Check both product.product and product.template
        if (self.env['product.product'].search_count(domain) > 0 or
            self.env['product.template'].search_count(domain) > 0):
            return False
        
        return True
