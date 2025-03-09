from yookassa import Payment
import uuid


def create_yookassa_payload(price: int, tariff_name: str) -> Payment:
    payment_data = {
        "amount": {
            "value": f"{price}.00",
            "currency": "RUB"
        },
        "test": False,
        "capture": True,
        "confirmation": {
            "type": "redirect",
            "return_url": "https://t.me/JIX_develop_bot"
        },
        "description": f"{tariff_name}",
        "receipt": {
            "customer": {
                "full_name": "Алексей Алексеев",
                "email": "https://t.me/JIX_develop_bot",
                "phone": "+79991234567"
            },
            "items": [
                {
                    "description": f"{tariff_name}",
                    "quantity": "1.00",
                    "amount": {
                        "value": f"{price}.00",
                        "currency": "RUB"
                    },
                    "vat_code": "1",
                    "payment_subject": "commodity",
                    "payment_mode": "full_payment"
                }
            ]
        }
    }

    return Payment.create(payment_data, uuid.uuid4())
