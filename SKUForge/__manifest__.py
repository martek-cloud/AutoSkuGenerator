{
    "name": "SKUFORGE – Advanced SKU Generator",
    "version": "18.0.1.0.0",
    "summary": "Generate structured, unique, and meaningful SKU codes for products and variants.",
    "category": "Inventory",
    "author": "Trae AI",
    "website": "https://www.odoo.com",
    "license": "OPL-1",

    "price": 21.35,
    "currency": "EUR",

    "depends": [
        "product",
        "stock"
    ],

    "data": [
        "security/ir.model.access.csv",
        "data/ir_sequence_data.xml",
        "views/sku_pattern_views.xml",
        "views/product_views.xml",
        "wizard/sku_generate_wizard_views.xml",
    ],

    "images": [
        "static/description/banner.png"
    ],

    "installable": True,
    "application": False,
    "auto_install": False,

    "description": """
SKUFORGE
========
Advanced SKU generation tool designed to automatically create unique, consistent,
and meaningful SKU codes for products and product variants using configurable
patterns and business rules.

Key Features:
- SKU Pattern Builder with configurable components
- Supports product names, categories, attributes, dates, sequences, companies, and fixed text
- Automatic SKU generation on product creation or bulk updates
- Dedicated handling for product variants
- Manual SKU override support
- SKU uniqueness validation across all products

Configuration:
Inventory → Configuration → SKU Configurations
    """,
}
