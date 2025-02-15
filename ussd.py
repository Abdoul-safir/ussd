import os
from flask import Flask, request
from serverless_wsgi import handle_request

app = Flask(__name__)

# Updated data for stamp types and their prices
stamp_types = {
    1: {"name": "Timbres Fiscaux", "price": 2000},
    2: {"name": "Timbres Postaux", "price": 5000},
    3: {"name": "Timbres de Quittance", "price": 3000},
    4: {"name": "Timbres Judiciaires", "price": 4000},
    5: {"name": "Timbres Administratifs", "price": 2500},
    6: {"name": "Timbres Locaux", "price": 1500},
    7: {"name": "Timbres Douaniers", "price": 3500},
    # Add other stamp types as needed
}

# Updated function to simulate payment and generate a 10-figure code
def make_payment():
    # Replace this with actual logic to process the payment
    # For simplicity, generate a random 10-figure code as a placeholder
    import random
    return str(random.randint(1000000000, 9999999999))

@app.route("/ussd", methods=['POST'])
def ussd():
    # Read the variables sent via POST from our API
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    if text == '':
        # Display the main menu
        response = "CON Welcome to the Fiscal Stamp Service\n"
        for key, value in stamp_types.items():
            response += f"{key}. {value['name']}\n"
    elif text.isdigit() and int(text) in stamp_types:
        # Get user input for the number of stamps
        selected_type = int(text)
        response = f"CON How many {stamp_types[selected_type]['name']} do you want?\n"
    elif '*' in text and text.split('*')[0].isdigit() and text.split('*')[1].isdigit():
        # Process the user input for the number of stamps
        stamp_type, quantity = map(int, text.split('*'))
        if stamp_type in stamp_types:
            total_amount = quantity * stamp_types[stamp_type]["price"]
            response = f"CON Total amount to pay: {total_amount:.2f} FRS CFA\nSelect payment method:\n1. Orange Money\n2. MTN Mobile Money\n3. Bank Payment"
    elif text.isdigit() and int(text) in [1, 2, 3]:
        # Process the user input for payment method
        payment_method = int(text)
        if payment_method in [1, 2, 3]:
            # Simulate payment and generate a 10-figure code
            payment_code = make_payment()
            response = f"END Payment successful!\nPayment details:\nAmount: {total_amount:.2f} FRS CFA\nPayment Method: {payment_method}\nPayment Code: {payment_code}\n\nPresent this code at any distribution point to get your stamps."
        else:
            response = "END Invalid payment method. Please try again."
    else:
        # Handle invalid input
        response = "END Invalid choice. Please try again."

    return response

def handler(event, context):
    return handle_request(app, event, context)
