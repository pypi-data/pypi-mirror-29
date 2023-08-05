import requests
import imghdr

from urllib.parse import urlencode, quote_plus
from io import BytesIO
from .extrahdr import what


class Response:
    def __init__(self, status_code):
        self.status_code = status_code


class ScanResponse(Response):
    def __init__(self, json, status_code):
        super().__init__(status_code)
        if status_code == 200:
            self.detections = json
        else:
            self.error_message = 'Unable to scan document'


class MatchResponse(Response):
    def __init__(self, json, status_code):
        super().__init__(status_code)
        if status_code == 200:
            self.matched_transactions = json['matchedTransactions']
            self.unmatched_transactions = json['unmatchedTransactions']
        else:
            self.error_message = json['errorMessage']


class Client:
    def __init__(self, api_key, base_endpoint='https://api.lucidtech.ai', stage='v0'):
        self.api_key = api_key
        self.base_endpoint = base_endpoint
        self.stage = stage

    def scan_receipt(self, receipt):
        receipt_id = self._upload_receipt(receipt)

        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }

        params = {'receiptId': receipt_id}
        querystring = urlencode(params, quote_via=quote_plus)
        endpoint = '/'.join([self.base_endpoint, self.stage, 'receipts?' + querystring])
        response = requests.post(endpoint, headers=headers)
        return ScanResponse(response.json(), response.status_code)

    def scan_invoice(self, invoice):
        receipt_id = self._upload_receipt(invoice)

        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }

        params = {'receiptId': receipt_id}
        querystring = urlencode(params, quote_via=quote_plus)
        endpoint = '/'.join([self.base_endpoint, self.stage, 'invoices?' + querystring])
        response = requests.post(endpoint, headers=headers)
        return ScanResponse(response.json(), response.status_code)

    def match_receipts(self, transactions, receipts, matching_fields, matching_strategy=None):
        matching_strategy = matching_strategy or {
            'total': {
                'maximumDeviation': 0.0
            },
            'date': {
                'maximumDeviation': 0
            }
        }

        body = {
            'receipts': {k: self._upload_receipt(r) for k, r in receipts.items()},
            'transactions': transactions,
            'matchingFields': matching_fields,
            'matchingStrategy': matching_strategy
        }

        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }

        endpoint = '/'.join([self.base_endpoint, self.stage, 'receipts', 'match'])
        response = requests.post(endpoint, json=body, headers=headers)
        return MatchResponse(response.json(), response.status_code)

    def _upload_receipt(self, receipt):
        supported_formats = {'jpeg', 'png', 'bmp', 'gif', 'pdf'}
        fp = BytesIO(receipt.content)
        fmt = imghdr.what(fp) or what(fp)

        if fmt in supported_formats:
            headers = {
                'x-api-key': self.api_key
            }

            endpoint = '/'.join([self.base_endpoint, self.stage, 'receipts/upload'])
            response = requests.get(endpoint, headers=headers).json()
            upload_url = response['uploadUrl']
            receipt_id = response['receiptId']
            response = requests.put(upload_url, data=receipt.content)
            if response.status_code == 200:
                return receipt_id
        elif fmt:
            raise Exception('File format {} not supported'.format(fmt))
        else:
            raise Exception('File format not recognized')
