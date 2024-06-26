"""
Duo Security Auth API reference client implementation.

<http://www.duosecurity.com/docs/authapi>
"""
from . import client

class Auth(client.Client):
    def ping(self):
        """
        Determine if the Duo service is up and responding.

        Returns information about the Duo service state: {
            'time': <int:UNIX timestamp>,
        }
        """
        return self.json_api_call('GET', '/auth/v2/ping', {})

    def check(self):
        """
        Determine if the integration key, secret key, and signature
        generation are valid.

        Returns information about the Duo service state: {
            'time': <int:UNIX timestamp>,
        }
        """
        return self.json_api_call('GET', '/auth/v2/check', {})

    def logo(self):
        """
        Retrieve the user-supplied logo.

        Returns the logo on success, raises RuntimeError on failure.
        """
        response, data = self.api_call('GET', '/auth/v2/logo', {})
        content_type = response.getheader('Content-Type')
        if content_type and content_type.startswith('image/'):
            return data
        else:
            return self.parse_json_response(response, data)

    def enroll(self, username=None, valid_secs=None, bypass_codes=None):
        """
        Create a new user and associated numberless phone.

        Returns activation information: {
            'activation_barcode': <str:url>,
            'activation_code': <str:actcode>,
            'bypass_codes': <list[str:autogenerated]:optional>,
            'user_id': <str:autogenerated>,
            'username': <str:provided or autogenerated>,
            'valid_secs': <int:seconds>,
        }
        """
        params = {}
        if username is not None:
            params['username'] = username
        if valid_secs is not None:
            valid_secs = str(int(valid_secs))
            params['valid_secs'] = valid_secs
        if bypass_codes is not None:
            bypass_codes = str(int(bypass_codes))
            params['bypass_codes'] = bypass_codes
        return self.json_api_call('POST',
                                  '/auth/v2/enroll',
                                  params)

    def enroll_status(self, user_id, activation_code):
        """
        Check if a user has been enrolled yet.

        Returns a string constant indicating whether the user has been
        enrolled or the code remains unclaimed.
        """
        params = {
            'user_id': user_id,
            'activation_code': activation_code,
        }
        response = self.json_api_call('POST',
                                      '/auth/v2/enroll_status',
                                      params)
        return response

    def preauth(self,
                username=None,
                user_id=None,
                ipaddr=None,
                client_supports_verified_push=None,
                trusted_device_token=None):
        """
        Determine if and with what factors a user may authenticate or enroll.

        See the adminapi docs for parameter and response information.
        """
        params = {}
        if username is not None:
            params['username'] = username
        if user_id is not None:
            params['user_id'] = user_id
        if ipaddr is not None:
            params['ipaddr'] = ipaddr
        if client_supports_verified_push is not None:
            params['client_supports_verified_push'] = client_supports_verified_push
        if trusted_device_token is not None:
            params['trusted_device_token'] = trusted_device_token
        response = self.json_api_call('POST',
                                      '/auth/v2/preauth',
                                      params)
        return response

    def auth(self,
             factor,
             username=None,
             user_id=None,
             ipaddr=None,
             async_txn=False,
             type=None,
             display_username=None,
             pushinfo=None,
             device=None,
             passcode=None,
             txid=None):
        """
        Perform second-factor authentication for a user.

        If async_txn is True, returns: {
            'txid': <str: transaction ID for use with auth_status>,
        }

        Otherwise, returns: {
            'result': <str:allow|deny>,
            'status': <str:machine-parsable>,
            'status_msg': <str:human-readable>,
        }

        If Trusted Devices is enabled, async_txn is not True, and status is
        'allow', another item is returned:

        * trusted_device_token: <str: device token for use with preauth>
        """
        params = {
            'factor': factor,
            'async': str(int(async_txn)),
        }
        if username is not None:
            params['username'] = username
        if user_id is not None:
            params['user_id'] = user_id
        if ipaddr is not None:
            params['ipaddr'] = ipaddr
        if type is not None:
            params['type'] = type
        if display_username is not None:
            params['display_username'] = display_username
        if pushinfo is not None:
            params['pushinfo'] = pushinfo
        if device is not None:
            params['device'] = device
        if passcode is not None:
            params['passcode'] = passcode
        if txid is not None:
            params['txid'] = txid
        response = self.json_api_call('POST',
                                      '/auth/v2/auth',
                                      params)
        return response

    def auth_status(self, txid):
        """
        Longpoll for the status of an asynchronous authentication call.

        Returns a dict with four items:

        * waiting: True if the authentication attempt is still in progress
          and the caller can continue to poll, else False.

        * success: True if the authentication request has completed and
          was a success, else False.

        * status: String constant identifying the request's state.

        * status_msg: Human-readable string describing the request state.

        If Trusted Devices is enabled, another item is returned when success
        is True:

        * trusted_device_token: String token to bypass second-factor
          authentication for this user during an admin-defined period.
        """
        params = {
            'txid': txid,
        }
        status = self.json_api_call('GET',
                                    '/auth/v2/auth_status',
                                    params)
        response = {
            'waiting': (status.get('result') == 'waiting'),
            'success': (status.get('result') == 'allow'),
            'status': status.get('status', ''),
            'status_msg': status.get('status_msg', ''),
        }

        if 'trusted_device_token' in status:
            response['trusted_device_token'] = status['trusted_device_token']

        return response
