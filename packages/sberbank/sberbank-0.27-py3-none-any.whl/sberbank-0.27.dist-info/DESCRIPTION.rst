Sberbank
========

Installation
-----------

1. Add "sberbank" to your INSTALLED_APPS settings:
    ```python
        INSTALLED_APPS = [
            ...
            'sberbank',
        ]
    ```

2. Add merchants params to your settings:
    ```python
        MERCHANTS = {
            %merchant_id%: {
                'username': %merchant_username%,
                'password': %merchant_password%,
                'success_url': %default_success_url%
            }
        }
    ```

3. Add callback url to you urls.py:
    ```python
        urlpatterns = [
            ...
            url('/sberbank', include('sberbank.urls'))
        ]

    ```

Sberbank
========

Installation
-----------

1. Add "sberbank" to your INSTALLED_APPS settings:
    ```python
        INSTALLED_APPS = [
            ...
            'sberbank',
        ]
    ```

2. Add merchants params to your settings:
    ```python
        MERCHANTS = {
            %merchant_id%: {
                'username': %merchant_username%,
                'password': %merchant_password%,
                'success_url': %default_success_url%
            }
        }
    ```

3. Add callback url to you urls.py:
    ```python
        urlpatterns = [
            ...
            url('/sberbank', include('sberbank.urls'))
        ]

    ```

4. Run `python manage.py migrate` to create models.

Usage
-----------
* Pay

    ```python
        from sberbank.service import BankService

        instance = BankService(%merchant_id%)
        payment = instance.pay(amount=%amount%)
    ```
    Response:

  | name | type | example |
  |----- | ---- | ------- |
  | payment_id | UUID | UUID('8b7e1798-eb96-402d-ac0e-fa23042d05a7') |
  | redirest_url | string | https://3dsec.sberbank.ru/payment/merchants/upravdoma/payment_ru.html?mdOrder=c12f8fae-447c-7853-c12f-8fae0000302b |

* Check payment status:

    ```python
        from sberbank.service import BankService

        instance = BankService(%merchant_id%)
        status = instance.get_status(%payment_id%)
    ```
  Response:

  | name | type | example |
  |----- | ---- | ------- |
  | status | ENUM | <Status.CREATED: 0> |
  | amount | decimal | 190.82 |
  | created| datetime | datetime.datetime(2018, 1, 26, 9, 4, 1, 950122) |
  | updated| datetime | datetime.datetime(2018, 1, 26, 9, 4, 1, 950122) |



