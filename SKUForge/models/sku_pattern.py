from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SkuPattern(models.Model):
    _name = 'sku.pattern'
    _description = 'SKU Pattern'
    _order = 'sequence, id'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    is_default = fields.Boolean(string='Default Pattern', help='Use this pattern if no other match found.')
    sequence_id = fields.Many2one('ir.sequence', string='Sequence', help='Sequence used for auto-incrementing numbers.')
    component_ids = fields.One2many('sku.pattern.component', 'pattern_id', string='Pattern Components')
    example_sku = fields.Char(string='Example SKU', compute='_compute_example_sku')
    
    @api.constrains('is_default')
    def _check_default(self):
        if self.is_default:
            others = self.search([('is_default', '=', True), ('id', '!=', self.id)])
            if others:
                raise ValidationError(_("There can be only one default SKU pattern."))

    @api.depends('component_ids')
    def _compute_example_sku(self):
        for record in self:
            record.example_sku = record._generate_mock_sku()

    def _generate_mock_sku(self):
        """Generate a mock SKU for preview/example purposes."""
        from datetime import datetime
        
        # Use the same date format map as the mixin for consistency
        DATE_FORMAT_MAP = {
            'year': '%Y',
            'short_year': '%y',
            'year_month': '%Y%m',
            'short_year_month': '%y%m',
            'year_month_day': '%Y%m%d',
        }
        
        sku_parts = []
        for comp in self.component_ids.sorted('sequence'):
            val = ''
            
            if comp.component_type == 'fixed':
                val = comp.fixed_value or ''
            elif comp.component_type == 'name':
                name = "Product Name"
                length = comp.length or len(name)
                val = name[:length]
            elif comp.component_type == 'category':
                cat = "Category"
                length = comp.length or len(cat)
                val = cat[:length]
            elif comp.component_type == 'attribute':
                val = "Color"
            elif comp.component_type == 'date':
                fmt = DATE_FORMAT_MAP.get(comp.date_format, '%Y')
                val = datetime.now().strftime(fmt)
            elif comp.component_type == 'sequence':
                val = '0' * (comp.padding or 5)
            elif comp.component_type == 'company':
                val = 'CMP'
            
            # Apply case transformation
            if comp.case == 'upper':
                val = val.upper()
            elif comp.case == 'lower':
                val = val.lower()
            
            sku_parts.append(val)
            
            if comp.separator:
                sku_parts.append(comp.separator)
        
        return "".join(sku_parts)

class SkuPatternComponent(models.Model):
    _name = 'sku.pattern.component'
    _description = 'SKU Pattern Component'
    _order = 'sequence, id'

    pattern_id = fields.Many2one('sku.pattern', string='Pattern', required=True, ondelete='cascade')
    sequence = fields.Integer(string='Sequence', default=10)
    component_type = fields.Selection([
        ('fixed', 'Fixed Text'),
        ('name', 'Product Name'),
        ('category', 'Category'),
        ('attribute', 'Product Attribute'),
        ('date', 'Date'),
        ('sequence', 'Sequence Number'),
        ('company', 'Company Code'),
    ], string='Type', required=True, default='name')
    
    fixed_value = fields.Char(string='Fixed Text')
    length = fields.Integer(string='Length', help='Number of characters to extract. 0 for all.')
    case = fields.Selection([('no', 'No Change'), ('upper', 'Uppercase'), ('lower', 'Lowercase')], string='Letter Case', default='upper')
    date_format = fields.Selection([
        ('year', 'YYYY'),
        ('short_year', 'YY'),
        ('year_month', 'YYYYMM'),
        ('short_year_month', 'YYMM'),
        ('year_month_day', 'YYYYMMDD'),
    ], string='Date Format', default='year')
    padding = fields.Integer(string='Sequence Padding', default=5)
    attribute_id = fields.Many2one('product.attribute', string='Attribute')
    separator = fields.Char(string='Separator', help='Separator added after this component')
