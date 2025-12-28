from odoo import models, api, fields, _
from odoo.exceptions import ValidationError
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    auto_generated_sku = fields.Boolean(string='Auto Generated SKU', default=False)

    @api.model
    def create(self, vals):
        """Override create to auto-generate SKU if not provided."""
        template = super(ProductTemplate, self).create(vals)
        
        # Auto-generate SKU only if default_code is not provided
        # Respects manually entered SKUs
        if not vals.get('default_code'):
            template.generate_sku()
        
        return template

    def generate_sku(self):
        """
        Generate SKU for this product template and its variants.
        Handles uniqueness validation and logging.
        """
        self.ensure_one()
        pattern = self.env['sku.pattern'].search([('is_default', '=', True)], limit=1)
        
        if not pattern:
            _logger.warning("No default SKU pattern found for product template %s", self.id)
            return
        
        # Generate SKU for template
        new_sku = pattern.generate_sku_for_product(self)
        
        if not new_sku:
            _logger.warning("Empty SKU generated for product template %s", self.id)
            return
        
        # Check uniqueness and assign
        if self._check_sku_uniqueness(new_sku):
            self.write({
                'default_code': new_sku,
                'auto_generated_sku': True
            })
        else:
            _logger.warning(
                "Duplicate SKU '%s' detected for product template %s (%s). SKU not assigned.",
                new_sku, self.id, self.name
            )
        
        # Generate SKU for variants that don't have one
        for variant in self.product_variant_ids:
            if not variant.default_code:
                variant.generate_sku()

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

    def action_generate_sku(self):
        """Action method to regenerate SKU for selected records."""
        for record in self:
            record.generate_sku()
    
    def action_open_sku_generate_wizard(self):
        """Open the SKU generation wizard for selected products."""
        self.ensure_one()
        return {
            'name': _('Generate SKU'),
            'type': 'ir.actions.act_window',
            'res_model': 'sku.generate.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_target_model': 'product_template',
                'active_ids': self.ids,
                'active_model': 'product.template',
            },
        }