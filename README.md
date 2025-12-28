# Auto SKU Generator for Odoo

**Technical Name**: `auto_sku_generator`  
**Compatibility**: Odoo 18, 19

## Overview
This module automatically generates unique, consistent, and meaningful SKU codes (Internal Reference) for products and product variants based on customizable patterns defined by the user.

## Features
- **Flexible Pattern Builder**: Define SKU structures using a drag-and-drop interface.
- **Pattern Components**:
    - **Product Name**: Extract first N characters (optional uppercase/lowercase).
    - **Category**: Use category name (first N chars).
    - **Attributes**: Include variant attributes (e.g., Color, Size).
    - **Date**: YYYY, YYMM, YYMMDD formats.
    - **Sequence**: Auto-incrementing number with padding.
    - **Company**: Company code or name.
    - **Fixed Text**: Custom prefixes, suffixes, or separators.
- **Automatic Generation**: SKUs are generated automatically when a product is created.
- **Bulk Generation**: Generate SKUs for existing products via a wizard.
- **Uniqueness Validation**: Ensures no duplicate SKUs are created.
- **Manual Override**: Respects manually entered SKUs unless explicitly overwritten.

## Installation
1.  Place the `auto_sku_generator` folder in your Odoo addons path.
2.  Update the App List.
3.  Install "Auto SKU Generator".

## Configuration
1.  Go to **Inventory > Configuration > SKU Configurations**.
2.  Create a new Pattern.
3.  Add components to the pattern list (e.g., Fixed Text "PROD-", Product Name (3 chars), Sequence).
4.  Set the pattern as **Default**.
5.  (Optional) Select or create a specific Sequence for auto-numbering.

## Usage
### New Products
- Create a product in Inventory.
- Leave the **Internal Reference** field empty.
- Save the product. The SKU will be generated automatically based on the default pattern.

### Existing Products (Bulk)
- Go to **Inventory > Products > Products**.
- Select multiple products in the list view.
- Click **Actions > Generate SKU**.
- Choose whether to override existing SKUs or only fill empty ones.
- Click **Generate**.

## Technical Details
- **Models**:
    - `sku.pattern`: Configuration for patterns.
    - `sku.pattern.component`: Individual parts of a pattern.
    - `product.template` & `product.product`: Inherited to add generation logic.
- **Security**: Access rules provided for standard users.
- **Tests**: Unit tests included in `tests/`.

## Support
For issues or feature requests, please contact the author.
