import os
import random
import string
from flask import Flask, request

app = Flask(__name__)

# Language-specific data
language_data = {
    "en": {
        "welcome": "CON Welcome to the Fiscal Stamp Service\nChoose language:\n1. English\n2. French",
        "stamp_types": {
            1: {"name": "Fiscal Stamps", "price": 2000},
            2: {"name": "Postal Stamps", "price": 5000},
            3: {"name": "Quittance Stamps", "price": 3000},
            4: {"name": "Judicial Stamps", "price": 4000},
            5: {"name": "Administrative Stamps", "price": 2500},
            6: {"name": "Local Stamps", "price": 1500},
            7: {"name": "Customs Stamps", "price": 3500},
        },
        "quantity_prompt": "CON How many {} do you want?\n",
        "total_amount": "CON Total amount to pay: {:.2f} FRS CFA\nSelect payment method:\n1. Orange Money\n2. MTN Mobile Money\n3. Bank Payment",
        "payment_success": "END Payment successful!\nPayment details:\nAmount: {:.2f} FRS CFA\nPayment Method: {}\nPayment Code: {}\n\nPresent this code at any distribution point to get your stamps.",
        "invalid_choice": "END Invalid choice. Please try again.",
    },
    "fr": {
        "welcome": "CON Bienvenue au Service des Timbres Fiscaux\nChoisissez la langue:\n1. Anglais\n2. Français",
        "stamp_types": {
            1: {"name": "Timbres Fiscaux", "price": 2000},
            2: {"name": "Timbres Postaux", "price": 5000},
            3: {"name": "Timbres de Quittance", "price": 3000},
            4: {"name": "Timbres Judiciaires", "price": 4000},
            5: {"name": "Timbres Administratifs", "price": 2500},
            6: {"name": "Timbres Locaux", "price": 1500},
            7: {"name": "Timbres Douaniers", "price": 3500},
        },
        "quantity_prompt": "CON Combien de {} voulez-vous?\n",
        "total_amount": "CON Montant total à payer: {:.2f} FRS CFA\nChoisissez le mode de paiement:\n1. Orange Money\n2. MTN Mobile Money\n3. Paiement Bancaire",
        "payment_success": "END Paiement réussi!\nDétails du paiement:\nMontant: {:.2f} FRS CFA\nMode de Paiement: {}\nCode de Paiement: {}\n\nPrésentez ce code à tout point de distribution pour obtenir vos timbres.",
        "invalid_choice": "END Choix invalide. Veuillez réessayer.",
    },
}

# Function to generate a 16-character alphanumeric code
def make_payment():
    characters = string.ascii_letters + string.digits  # A-Z, a-z, 0-9
    code = ''.join(random.choice(characters) for _ in range(16))
    return code

@app.route("/ussd", methods=['POST'])
def ussd():
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "")

    # Split the user input into a list
    user_input = text.split("*")

    if text == "":
        # First interaction: Ask for language
        response = language_data["en"]["welcome"]
    elif len(user_input) == 1:
        # User has selected a language
        language_choice = user_input[0]
        if language_choice == "1":
            language = "en"
        elif language_choice == "2":
            language = "fr"
        else:
            return language_data["en"]["invalid_choice"]

        # Display the main menu in the selected language
        response = f"CON {language_data[language]['welcome']}\n"
        for key, value in language_data[language]["stamp_types"].items():
            response += f"{key}. {value['name']}\n"
    elif len(user_input) == 2:
        # User has selected a stamp type
        language_choice = user_input[0]
        stamp_type = int(user_input[1])

        if language_choice == "1":
            language = "en"
        elif language_choice == "2":
            language = "fr"
        else:
            return language_data["en"]["invalid_choice"]

        if stamp_type in language_data[language]["stamp_types"]:
            stamp_name = language_data[language]["stamp_types"][stamp_type]["name"]
            response = language_data[language]["quantity_prompt"].format(stamp_name)
        else:
            response = language_data[language]["invalid_choice"]
    elif len(user_input) == 3:
        # User has entered the quantity
        language_choice = user_input[0]
        stamp_type = int(user_input[1])
        quantity = int(user_input[2])

        if language_choice == "1":
            language = "en"
        elif language_choice == "2":
            language = "fr"
        else:
            return language_data["en"]["invalid_choice"]

        if stamp_type in language_data[language]["stamp_types"]:
            total_amount = quantity * language_data[language]["stamp_types"][stamp_type]["price"]
            response = language_data[language]["total_amount"].format(total_amount)
        else:
            response = language_data[language]["invalid_choice"]
    elif len(user_input) == 4:
        # User has selected a payment method
        language_choice = user_input[0]
        stamp_type = int(user_input[1])
        quantity = int(user_input[2])
        payment_method = int(user_input[3])

        if language_choice == "1":
            language = "en"
        elif language_choice == "2":
            language = "fr"
        else:
            return language_data["en"]["invalid_choice"]

        if stamp_type in language_data[language]["stamp_types"] and payment_method in [1, 2, 3]:
            total_amount = quantity * language_data[language]["stamp_types"][stamp_type]["price"]
            payment_code = make_payment()
            response = language_data[language]["payment_success"].format(total_amount, payment_method, payment_code)
        else:
            response = language_data[language]["invalid_choice"]
    else:
        # Handle invalid input
        response = language_data["en"]["invalid_choice"]

    return response

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT'), debug=True)
