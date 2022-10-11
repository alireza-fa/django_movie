import requests
import json


ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"


def send_request(**kwargs):
    req_data = {
        "merchant_id": kwargs['merchant'],
        "amount": kwargs['amount'] * 10,  # convert toman to rial
        "callback_url": kwargs['callback_url'],
        "description": kwargs['description'],
        "metadata": {"mobile": kwargs['mobile'], "email": kwargs['email']}
    }

    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=kwargs['api_request'], data=json.dumps(
        req_data), headers=req_header)

    authority = req.json()['data']['authority']

    if len(req.json()['errors']) == 0:
        url = ZP_API_STARTPAY.format(authority=authority)
        return 100, {"url": url, "authority": authority}

    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        error_code, error_message = e_code, e_message
        return 200, {"error_code": error_code, "error_message": error_message}


def verify(**kwargs):

    if kwargs['request'].GET.get('Status') == 'OK':
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": kwargs['merchant'],
            "amount": kwargs['amount'] * 10,  # convert toman to rial,
            "authority": kwargs['authority']
        }

        req = requests.post(url=kwargs['api_verify'], data=json.dumps(req_data), headers=req_header)

        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                return 100, {"ref_id": req.json()['data']['ref_id']}
            elif t_status == 101:
                return 101, {"message": req.json()['data']['message']}
            else:
                return -100, {"message": req.json()['data']['message']}
    else:
        return None, None
