from requests import RequestException


class NetworkException(RequestException):
    def __init__(self, payment_id):
        self.payment_id = payment_id
        super().__init__('Network error. Payment id {}'.format(payment_id))


class ProcessingException(RequestException):
    def __init__(self, payment_id):
        self.payment_id = payment_id
        super().__init__('Bank error. Payment id {}'.format(payment_id))


class PaymentNotFoundException(Exception):
    def __init__(self):
        super().__init__('payment_id not found in DB')
