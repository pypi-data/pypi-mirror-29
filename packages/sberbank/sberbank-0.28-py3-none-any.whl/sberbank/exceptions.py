from requests import RequestException


class NetworkException(RequestException):
    def __init__(self, payment_id):
        self.payment_id = payment_id
        super().__init__('Network error. Payment id {}'.format(payment_id))


class ProcessingException(RequestException):
    def __init__(self, payment_id, *args, **kwargs):
        self.payment_id = payment_id
        super().__init__(f'Bank error. Payment id {self.payment_id}'
                         f'Info: {args} {kwargs}')


class PaymentNotFoundException(Exception):
    def __init__(self):
        super().__init__('Payment_id not found in DB')
