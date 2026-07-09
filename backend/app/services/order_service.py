from app.database.orders import orders

def verify_order(customer: str, platform: str):

    for order in orders:
        if customer is None or platform is None:
            return None
        elif (
            order["customer"].lower() == customer.lower()
            and order["platform"].lower() == platform.lower()
        ):
            return order

    return None