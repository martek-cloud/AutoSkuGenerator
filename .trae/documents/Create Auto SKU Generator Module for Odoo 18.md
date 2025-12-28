I will create a new Odoo 18 module named `auto_sku_generator` to automatically generate the Internal Reference (SKU) for products.

The module will include the following components:

1.  **Module Structure**:
    -   Standard Odoo module structure with `__manifest__.py`, `__init__.py`, `models/`, `data/`, and `views/`.

2.  **Sequence Definition (`data/ir_sequence_data.xml`)**:
    -   Define an `ir.sequence` record to handle the auto-incrementing numbers (e.g., prefix 'SKU', padding 5 digits).

3.  **Model Extension (`models/product_template.py`)**:
    -   Inherit `product.template`.
    -   Override the `create` method (or use a default value/compute) to assign a generated SKU from the sequence if the "Internal Reference" (`default_code`) is not provided by the user.

4.  **Manifest (`__manifest__.py`)**:
    -   Define module dependencies (depends on `product`).

This approach ensures that every new product gets a unique SKU automatically.

**Step-by-step Implementation Plan:**
1.  Create the directory structure.
2.  Create `__manifest__.py` and `__init__.py`.
3.  Create `data/ir_sequence_data.xml` to define the sequence.
4.  Create `models/product_template.py` to implement the logic.
5.  Create `models/__init__.py` to expose the model.
