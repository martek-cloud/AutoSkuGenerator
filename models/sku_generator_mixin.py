from odoo import models, api, _
from datetime import datetime
import logging

_logger = logging.getLogger(__name__)

class SkuPattern(models.Model):
    _inherit = 'sku.pattern'

    # Date format mapping - defined as class constant for reusability
    DATE_FORMAT_MAP = {
        'year': '%Y',
        'short_year': '%y',
        'year_month': '%Y%m',
        'short_year_month': '%y%m',
        'year_month_day': '%Y%m%d',
    }

    def generate_sku_for_product(self, product):
        """
        Generate SKU for a product (template or variant).
        
        :param product: product.template or product.product record
        :return: Generated SKU string
        """
        self.ensure_one()
        sku_parts = []
        is_variant = product._name == 'product.product'
        
        for comp in self.component_ids.sorted('sequence'):
            val = self._get_component_value(comp, product, is_variant)
            
            # Apply case transformation
            if comp.case == 'upper':
                val = val.upper()
            elif comp.case == 'lower':
                val = val.lower()
            
            sku_parts.append(val)
            
            # Add separator if specified
            if comp.separator:
                sku_parts.append(comp.separator)
        
        return "".join(sku_parts)

    def _get_component_value(self, comp, product, is_variant):
        """
        Get the value for a specific component.
        
        :param comp: sku.pattern.component record
        :param product: product.template or product.product record
        :param is_variant: Boolean indicating if product is a variant
        :return: Component value string
        """
        val = ''
        
        if comp.component_type == 'fixed':
            val = comp.fixed_value or ''
        
        elif comp.component_type == 'name':
            name = product.name or ''
            if comp.length and comp.length > 0:
                val = name[:comp.length]
            else:
                val = name
        
        elif comp.component_type == 'category':
            categ = product.categ_id
            if categ:
                val = categ.name or ''
                if comp.length and comp.length > 0:
                    val = val[:comp.length]
        
        elif comp.component_type == 'attribute':
            if is_variant and comp.attribute_id:
                ptavs = product.product_template_attribute_value_ids
                relevant_val = ptavs.filtered(lambda v: v.attribute_id == comp.attribute_id)
                if relevant_val:
                    val = "-".join(relevant_val.mapped('name'))
        
        elif comp.component_type == 'date':
            fmt = self.DATE_FORMAT_MAP.get(comp.date_format, '%Y')
            val = datetime.now().strftime(fmt)
        
        elif comp.component_type == 'sequence':
            val = self._get_sequence_value(comp)
        
        elif comp.component_type == 'company':
            if product.company_id:
                # Use company code if available, otherwise first 3 chars of name
                val = getattr(product.company_id, 'code', None) or product.company_id.name[:3]
        
        return val

    def _get_sequence_value(self, comp):
        """
        Get sequence value for the component.
        
        :param comp: sku.pattern.component record
        :return: Sequence value string
        """
        if self.sequence_id:
            try:
                return self.sequence_id.next_by_id()
            except Exception as e:
                _logger.warning("Failed to get sequence from pattern sequence_id: %s", e)
        
        # Fallback to default sequence (matching data file)
        try:
            return self.env['ir.sequence'].next_by_code('product.sku') or '00000'
        except Exception as e:
            _logger.warning("Failed to get sequence from default code: %s", e)
            return '00000'
