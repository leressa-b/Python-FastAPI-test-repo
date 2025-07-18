import unittest
from unittest.mock import Mock
from payment import PaymentProcessor

class TestPaymentProcessor(unittest.TestCase):
    def test_successful_payment(self):
        gateway = Mock()
        ledger = Mock()
        logger = Mock()

        processor = PaymentProcessor(gateway, ledger, logger)
        user = Mock()
        user.is_suspended = False
        user.card = "123"

        result = processor.process_payment(user, 100)
        self.assertTrue(result)
        gateway.charge.assert_called_once_with("123", 100)
        ledger.record.assert_called_once_with(user.id, 100)

    def test_invalid_amount(self):
        gateway = Mock()
        ledger = Mock()
        logger = Mock()

        processor = PaymentProcessor(gateway, ledger, logger)
        user = Mock()
        user.is_suspended = False

        with self.assertRaises(ValueError):
            processor.process_payment(user, 0)