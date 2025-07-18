from payment import PaymentProcessor

class DummyGateway:
    def charge(self, card, amount):
        """
        Simulate charging a payment card for a specified amount and return a fixed transaction ID.
        
        Parameters:
        	card (str): The payment card identifier.
        	amount (float): The amount to charge.
        
        Returns:
        	str: A fixed transaction ID string.
        """
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