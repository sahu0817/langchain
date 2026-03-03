# mcp_backend.py
from typing import Dict, Any
import json

# Pretend this is backed by a Lightning Table / DB / API
ORDERS = {
    "ORD-1001": {"orderId": "ORD-1001", "customer": "Alice", "total": 42.5},
    "ORD-1002": {"orderId": "ORD-1002", "customer": "Bob", "total": 13.37},
}

def lookup_order(table: str, key: str) -> str:
    """
    Lookup an order by primary key and return JSON.
    `table` is unused here but included to mirror a generic pattern.
    """
    if table != "orders":
        raise ValueError(f"Unknown table: {table}")

    order = ORDERS.get(key)
    if not order:
        raise KeyError(f"Order {key} not found")

    return json.dumps(order, indent=2)
