from payment import PaymentProcessor

class DummyGateway:
    def charge(self, card, amount):
        return "txn123" 

def test_charge_success():
    user = type("User", (), {"account_suspended": False, "card": "1234"})
    processor = PaymentProcessor(DummyGateway())
    result = processor.charge_user(user, 100)
    assert result["status"] == "success"

def test_charge_invalid_amount():
    user = type("User", (), {"account_suspended": False, "card": "1234"})
    processor = PaymentProcessor(DummyGateway())
    result = processor.charge_user(user, 0)
    assert result["status"] == "failed"