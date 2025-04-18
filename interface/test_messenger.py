
from messenger import Messenger

msg_handler = Messenger()

msg_handler.show_error("Test Show Error", "This is an error message.")

msg_handler.show_warning("Test Show Warning", "This is a warning message.")

msg_handler.show_info("Test Show Info", "This is an informational message.")

response1 = msg_handler.confirm_action("Test Confirm Action", "This is a confirmation message.")

if response1:
    msg_handler.show_info("Positive Confirmation", f"Received this response: {response1}")
else:
    msg_handler.show_info("Negative Confirmation", f"Received this response: {response1}")

response2 = msg_handler.confirm_action("Test Confirm Action", "This is a confirmation message.")

if response2:
    msg_handler.show_info("Positive Confirmation", f"Received this response: {response2}")
else:
    msg_handler.show_info("Negative Confirmation", f"Received this response: {response2}")