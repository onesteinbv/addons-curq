{
    "name": "WMS Accounting",
    "author": "Onestein",
    "website": "https://onestein.nl",
    "category": "Hidden",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "depends": [
        "account_install",
        "stock_install",
        "account_move_line_stock_info",
        "account_move_line_purchase_info",
    ],
    "auto_install": ["account_install", "stock_install"],
    "bundle": True,
}
