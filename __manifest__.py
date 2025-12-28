{
    'name': 'SKUFORGE',
    'version': '18.0.1.0.0',
    'summary': 'Automatically generate unique, consistent, and meaningful SKU codes for products and variants.',
    'category': 'Inventory/Inventory',
    'author': 'Trae AI',
    'website': 'https://www.odoo.com',
    'license': 'LGPL-3',
    'depends': ['product', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/sku_pattern_views.xml',
        'views/product_views.xml',
        'wizard/sku_generate_wizard_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/banner.png'],
    'description': """
SKUFORGE
========
Powerful SKU generation tool that automatically creates unique, consistent, and meaningful SKU codes for products and product variants based on customizable patterns and business rules.

Features:
- **SKU Pattern Builder UI**: Drag & drop pattern components with intuitive interface.
- **Pattern Components**: Product Name, Category, Attributes, Date, Sequence, Company, Fixed Text.
- **Automatic Generation**: On creation or bulk update.
- **Variant Handling**: Specific logic for variants.
- **Manual Override**: Respects manually entered SKUs.
- **Validation**: Ensures uniqueness across all products.

Configuration:
Go to Inventory > Configuration > SKU Configurations (or Settings > Technical > SKU Configurations).
    """,
}
