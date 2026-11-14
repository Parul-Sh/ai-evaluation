
def search_order(order_id):
    """Search for an order using its ID."""

    orders = {
        "ORD101": {
            "status": "Shipped",
            "delivery": "Expected in 2 days"
        },
        "ORD102": {
            "status": "Processing",
            "delivery": "Expected in 5 days"
        }
    }

    return orders.get(order_id, "Order not found")


def check_refund_eligibility(order_id):
    """Check whether an order is eligible for a refund."""

    eligible_orders = ["ORD101"]

    return {
        "order_id": order_id,
        "eligible": order_id in eligible_orders
    }


def create_support_ticket(customer_id, issue):
    """Create a customer support ticket."""

    return {
        "ticket_id": "TICKET001",
        "customer_id": customer_id,
        "issue": issue,
        "status": "Created"
    }
