from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class SkuGenerateWizard(models.TransientModel):
    _name = 'sku.generate.wizard'
    _description = 'Bulk SKU Generation Wizard'

    target_model = fields.Selection([
        ('product_template', 'Product Templates'),
        ('product_product', 'Product Variants')
    ], string='Target', default='product_template', required=True)
    
    override_existing = fields.Boolean(
        string='Override Existing SKU',
        default=False,
        help="If checked, existing Internal References will be overwritten."
    )
    
    def action_generate(self):
        """
        Generate SKUs for selected records.
        Uses active_ids from context to determine which records to process.
        """
        active_ids = self.env.context.get('active_ids', [])
        if not active_ids:
            raise UserError(_("No records selected. Please select products to generate SKUs for."))
        
        model_name = 'product.template' if self.target_model == 'product_template' else 'product.product'
        records = self.env[model_name].browse(active_ids)
        
        # Get default pattern
        pattern = self.env['sku.pattern'].search([('is_default', '=', True)], limit=1)
        if not pattern:
            raise UserError(_("No default SKU pattern found. Please create and set a default pattern first."))
        
        # Track results
        generated_count = 0
        skipped_count = 0
        duplicate_count = 0
        
        for record in records:
            # Skip if has SKU and override is not enabled
            if not self.override_existing and record.default_code:
                skipped_count += 1
                continue
            
            # Generate SKU
            new_sku = pattern.generate_sku_for_product(record)
            
            if not new_sku:
                _logger.warning("Empty SKU generated for %s (ID: %s)", record._name, record.id)
                continue
            
            # Check uniqueness using the record's method
            if record._check_sku_uniqueness(new_sku):
                record.write({
                    'default_code': new_sku,
                    'auto_generated_sku': True
                })
                generated_count += 1
            else:
                duplicate_count += 1
                _logger.warning(
                    "Duplicate SKU '%s' detected for %s (ID: %s). SKU not assigned.",
                    new_sku, record._name, record.id
                )
        
        # Log summary
        _logger.info(
            "SKU Generation Complete: %d generated, %d skipped (has SKU), %d skipped (duplicate)",
            generated_count, skipped_count, duplicate_count
        )
        
        # Show user-friendly message
        message_parts = []
        if generated_count > 0:
            message_parts.append(_("%d SKU(s) generated successfully.") % generated_count)
        if skipped_count > 0:
            message_parts.append(_("%d record(s) skipped (already have SKU).") % skipped_count)
        if duplicate_count > 0:
            message_parts.append(_("%d record(s) skipped (duplicate SKU detected).") % duplicate_count)
        
        if message_parts:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': _('SKU Generation Complete'),
                    'message': '\n'.join(message_parts),
                    'type': 'success',
                    'sticky': False,
                }
            }
        
        return {'type': 'ir.actions.act_window_close'}
