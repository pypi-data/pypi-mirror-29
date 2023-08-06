# Realex SDK

Realex SDK for **auth**, **3ds\_verifiyenrolled** and **3ds\_verifysig** calls.

# Requirements

Python 2.7 or Python 3.6+

# Installation

```bash
pip install realex
```

# Usage

## Things you will need

At minimum, you'd need to have a Realex account (a test account will do). With the account you'll receive a **merchant id** which will be needed to authenticate yourself when making the calls. You also need to setup a **shared secret** with Realex, which will be used to sign your request.

Once you have these, you can setup your Realex config:

```python
from realex.realex import Realex

Realex.SHARED_SECRET = "Your shared secret"
Realex.MERCHANT_ID = "Your merchant id"

# Only needed for 3D secure calls
Realex.CALLBACK_URL = "http://callback.to.your.app.com/"
```

### Test mode

You can use the same URL, just use your test account details (merchant id and shared secret) to carry out the requests. The response message should indicate that it was served from a test system.

## Auth request

Auth requests are used to pay for something with your card. Alternatively they can be referred to as 'charges', 'orders' or 'transactions' in other processors' glossaries.

To create an auth request, you need the typical cardholder details (card holder name, card number, expiry, cvv) and the amount the customer is paying.

```python
# Create an auth request - i.e. charge a card with an amount
response = Realex.create_charge(
    amount=10.00,
    currency='EUR',
    card_holder_name='Ms Test Card',
    card_number='4111111111111111',
    cvv='123',
    expiry_month='12',
    expiry_year='25',
    card_type='VISA'
    )
```

The response object will be a dict, containing status code, realex result code and the message

```python
{
  'status_code': '00',
  'realex_result_code': '00',
  'message': 'SUCCESS'
}
```

## 3DS Verify Enrolled request

When you implement the 3D Secure flow (verified by visa, mastercard, etc.), first you need to check if the card is enrolled in the program. The verified enrolled API will tell you exactly that, indicating if you are free to carry out the call by redirecting to the bank verification page, or to carry on with an auth request as normal. For full details on the API, you can check [Realex's documentation](https://developer.realexpayments.com/#!/api/3d-secure/verify-enrolled).

```python
response = Realex.verify_enrolled(
    amount=10.00,
    currency='EUR',
    card_holder_name='Ms Test Card',
    card_number='4111111111111111',
    cvv='123',
    expiry_month='12',
    expiry_year='25',
    card_type='VISA'
    )
```

The response should have information about your next possible steps. It will also inform you about the card's validity, or if it failed on fraud checks.

```python
{
  'status_code': '00',
  'realex_result_code': '00',
  'message': 'Card enrolled',
  'pareq': 'P4R3q',
  'url': 'https://url.of.bank.com/',
  'enrolled': 'Y',
  'order_id': 'ORDER_ID',
  'sha1hash': 's0mesh4v4lu3'
}
```

If you got a positive response in `enrolled`, you need to call the `url` listed in the response with the `pareq`, your `termUrl` (i.e. the callback location the bank site will call after the verification finished) and an optional `md` (shorthand for merchant data).

## 3DS Verify Sig request

On return from the 3D secure site (the bank's page), you will get back a `pares` attribute (the effective result of the customer's verification, encoded) and the `md` (merchant data) you have initially submitted. Now you can use these to verify the verification (very meta) and then finally call the `auth` method, once you got a positive response back from this call.

```python
response = Realex.verify_signed(
    amount=10.00,
    currency='EUR',
    pares='p4r3s', # The result of the 3D secure verification
    sha1hash='sha1hash',
    order_id='ORDERID'
)
```

In the result, you'll get back - along with the usual fields like message and status_code - parameters that are required to pass on to the `auth` call. These are: `eci`, `xid` and `cavv`.

```python
{
  'status_code': '00',
  'cavv': 'AAABASY3QHgwUVdEBTdAAAAAAAA=',
  'eci': '5',
  'xid': 'crqAeMwkEL9r4POdxpByWJ1/wYg=',
  'message': 'authentication successful',
  'realex_result_code': '00',
  'status': 'Y'
}
```

See [Realex's docs](https://developer.realexpayments.com/#!/api/3d-secure/3ds-verifysig) for full information about the values and their format.
