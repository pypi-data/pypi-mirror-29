#!/usr/local/bin/python3.5
# -*- coding: utf-8 -*-

__author__ = "YellowPush"
__copyright__ = "Copyright (C) YellowPush."

__revision__ = "$Id$"
__version__ = "0.0.1"

import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder
import urllib3

import datetime

urllib3.disable_warnings()

__all__ = ['Client']

# url account
account_url = 'https://api.identidadsms.net/rest/account'
# url tocken
url_token = 'https://api.identidadsms.net/rest/auth'
# url send sms
url_send_sms = 'https://api.identidadsms.net/rest/send_sms'
# url sms edr
url_sms_edr = 'https://api.identidadsms.net/rest/sms_edr'
# url bulk send sms
url_bulk_send_sms = 'https://api.identidadsms.net/rest/bulk_send_sms'


class Client():
    def __init__(self, user, password, account_id = None):
        """

        :param user:
        :param password:
        """
        self.user = user
        self.password = password
        self.token = None
        self.account_id = account_id

    def __response_message(self, content, status_code):
        """
        construye  el diccionario de respuesta
        """
        has_error = False
        error = ''

        if status_code != 200:
            has_error = True
            error = content

        rsp ={
            'Content': content,
            'StatusCode': status_code,
            'HasError': has_error,
            'Error' : error,
        }
        return rsp

    def __request_get(self, url, auth=None, data=None, token=None, parameters = None):
        """
        Realiza la solicitud http al servicio rest YellowPush
        """
        headers = {}

        if token:
            headers['Authorization'] = "Bearer {}".format(token)

        try:
            r = requests.get(url, auth=auth, headers=headers, data=data, params=parameters,verify=False)
            rsp = r.json()
        except requests.exceptions.RequestException as err:
            return self.__response_message(err, 0)

        return self.__response_message(rsp, r.status_code)

    def __request_post(self, url, content_type=None, auth=None, data=None, token=None, parameters = None):
        """
        Realiza la solicitud http al servicio rest YellowPush
        """
        headers = {}

        if token:
            headers['Authorization'] = "Bearer {}".format(token)
        if content_type:
            headers['Content-Type'] = content_type

        try:
            r = requests.post(url, auth=auth, headers=headers, data=data, params=parameters,verify=False)
            rsp = r.json()
        except requests.exceptions.RequestException as err:
            return self.__response_message(err, 0)

        return self.__response_message(rsp, r.status_code)


    def SendSMS(self, **kwargs):
        """
        Envia SMS
        mobileNumbers="+15558675309",
        from_="+15017250604",
        message="Hello from Python!"
        """
        mobileNumbers = kwargs['mobileNumbers']
        from_ = kwargs['from_']
        message = kwargs['message']
        auth = (self.user, self.password)

        # Verifica si no existe el account_id
        if not self.account_id:
            # Solicita la cuenta del usuario
            rsp = self.__request_get(account_url, auth, None)
            if rsp['HasError'] :
                return rsp

            self.account_id = str(rsp['Content'][0]['id'])

        # Solicita token del usuario
        rsp = self.__request_get(url_token, auth, None)
        if rsp['HasError']:
            return rsp

        self.token = rsp['Content']['token']


        # Datos form
        multipart_data = MultipartEncoder(
            fields={
                "acc_id": self.account_id,
                "from": from_,
                "message": message,
                "to": mobileNumbers
            }
        )
        data = multipart_data.to_string()

        # Envia SMS
        rsp = self.__request_post(url_send_sms, multipart_data.content_type, None, data, self.token)
        return rsp

    def GetMessageStatus(self, **kwargs):
        """
        Envia SMS
        messageId="5a5600d4-6cbd-b6e0-d221-cfe544e29d7f",
        sendDate="2018-03-05",
        endDate="2018-03-06"
        """
        messageId = kwargs['messageId']
        sendDate = kwargs['sendDate']
        auth = (self.user, self.password)

        delivery_date = datetime.datetime.strptime(sendDate, "%Y-%m-%d")
        before_date = delivery_date - datetime.timedelta(days=1)
        after_date = delivery_date + datetime.timedelta(days=1)

        str_before_date = before_date.strftime('%Y-%m-%d')
        str_after_date = after_date.strftime('%Y-%m-%d')

        # Verifica si no existe el account_id
        if not self.account_id:
            # Solicita la cuenta del usuario
            rsp = self.__request_get(account_url, auth, None)
            if rsp['HasError'] :
                return rsp

            self.account_id = str(rsp['Content'][0]['id'])

        # Solicita token del usuario
        rsp = self.__request_get(url_token, auth, None)
        if rsp['HasError']:
            return rsp

        self.token = rsp['Content']['token']

        # parametros url
        parameters = {
            "client_message_id": messageId,
            "end_date": str_after_date,
            "start_date": str_before_date
        }

        # Solicita token del usuario
        rsp = self.__request_get(url_sms_edr, None, None, self.token, parameters)
        return rsp



    def BulkSendSMS(self, **kwargs):
        """
        Envia SMS
        listMessages=[
            {
            "from":"893333",
            "to":"573103058946",
            "message": "hola333"
            },
            ]
        """
        listMessages = kwargs['listMessages']

        auth = (self.user, self.password)

        # Verifica si no existe el account_id
        if not self.account_id:
            # Solicita la cuenta del usuario
            rsp = self.__request_get(account_url, auth, None)
            if rsp['HasError'] :
                return rsp

            self.account_id = str(rsp['Content'][0]['id'])

        # Solicita token del usuario
        rsp = self.__request_get(url_token, auth, None)
        if rsp['HasError']:
            return rsp

        self.token = rsp['Content']['token']

        # parametros url
        parameters = {
            "acc_id": self.account_id,
            "show_details": 1
        }


        # Envia SMS
        rsp = self.__request_post(url_bulk_send_sms, "application/json", None, json.dumps(listMessages), self.token, parameters)
        return rsp
