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
        "static/description/banner.png",
        "static/description/New SKU Patern.png",
        "static/description/Configure Pattern.png",
        "static/description/Generate SKU.png"
    ],

    "installable": True,
    "application": False,
    "auto_install": False,

    "description": "<h2>SKUFORGE – Advanced SKU Generator</h2><p>Advanced SKU generation tool designed to automatically create unique, consistent, and meaningful SKU codes for products and product variants using configurable patterns and business rules.</p><h3>Key Features:</h3><ul><li><strong>SKU Pattern Builder</strong> with configurable components</li><li>Supports product names, categories, attributes, dates, sequences, companies, and fixed text</li><li>Automatic SKU generation on product creation or bulk updates</li><li>Dedicated handling for product variants</li><li>Manual SKU override support</li><li>SKU uniqueness validation across all products</li></ul><h3>Configuration:</h3><p>Go to <strong>Inventory → Configuration → SKU Configurations</strong> to set up your SKU patterns.</p><h3>How It Works:</h3><ol><li>Create a SKU pattern with customizable components</li><li>Set it as the default pattern</li><li>SKUs are automatically generated when products are created</li><li>Use the bulk generation wizard for existing products</li></ol>",
}
