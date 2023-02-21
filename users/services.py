import time

import requests
from django.conf import settings

NIKITA_MOBILE_URL = settings.NIKITA_MOBILE_URL
NIKITA_MOBILE_USERNAME = settings.NIKITA_MOBILE_USERNAME
NIKITA_MOBILE_PASSWORD = settings.NIKITA_MOBILE_PASSWORD


def send_otp_code(text, generated_code, phone_number):
    try:
        requests.post(NIKITA_MOBILE_URL,
                      auth=(NIKITA_MOBILE_USERNAME, NIKITA_MOBILE_PASSWORD),
                      json={"messages": [{"recipient": f"{phone_number}",
                                          "sms": {
                                              "originator": "Canapea.am",
                                              "content": {
                                                  "text": f"{text}{generated_code}"
                                              }
                                          },
                                          "message-id": f"{(int(time.time()))}"}]
                            })

        return True
    except Exception as e:
        return False
