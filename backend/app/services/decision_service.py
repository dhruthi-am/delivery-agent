def decide_delivery_action(order):

    # Order not verified
    if order is None:
        return {
            "status": "Order Not Verified",
            "instruction": (
                "The order could not be verified. "
                "Please contact the customer or revisit after 7 PM."
            )
        }

    # Verified order
    return {
        "status": "Verified",
        "instruction": order["instruction"]
    }