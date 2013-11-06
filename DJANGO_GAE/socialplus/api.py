import json
import httplib2
import logging
import sys
import os

from django.core.cache import cache

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials
from oauth2client.client import AccessTokenRefreshError

API_ACCESS_DATA = {
    "DOMAIN": {
        "SERVICE_ACCOUNT_EMAIL": "xxx@developer.gserviceaccount.com",
        "ADMIN_EMAIL": "socialplus@yourdomain.com",
        "SERVICE_ACCOUNT_PEM_FILE_PATH": "privatekey.pem",
        "DOMAIN_NAME": "yourdomain.com",
        "CUSTOMER_ID": "xxx",
        "DIRECTORY_SCOPES": [
            "https://www.googleapis.com/auth/admin.directory.user.readonly",
            "https://www.googleapis.com/auth/admin.directory.orgunit.readonly",
        ]
    }
}

CURRENT_DOMAIN = "DOMAIN"

current_plus_service = {"user_email" : "--", "service" : None}

def create_plus_service(user_email):

    if current_plus_service["user_email"] == user_email and current_plus_service["service"]:
        return current_plus_service["service"]
    else:
        print("NEW AUTHENTICATION NECESSARY: current email is " + current_plus_service["user_email"] + " and new email is " + user_email)

    f = file(API_ACCESS_DATA[CURRENT_DOMAIN]["SERVICE_ACCOUNT_PEM_FILE_PATH"], 'rb')
    key = f.read()
    f.close()

    http = httplib2.Http()
    cached_http = cache.get('plus_http_' + user_email)
    if not cached_http == None:
        http = cached_http
        logging.debug("CACHE HIT")
    else:
        credentials = SignedJwtAssertionCredentials(API_ACCESS_DATA[CURRENT_DOMAIN]["SERVICE_ACCOUNT_EMAIL"], key, scope=[
            "https://www.googleapis.com/auth/plus.circles.read",
            "https://www.googleapis.com/auth/plus.circles.write",
            "https://www.googleapis.com/auth/plus.profiles.read",
            "https://www.googleapis.com/auth/plus.stream.read",
            "https://www.googleapis.com/auth/plus.stream.write"
        ], sub=user_email)
        http = credentials.authorize(http)
        cache.set('plus_http_' + user_email, http, 30)
        logging.debug("CACHE MISS")

    service = build("plus", "v1domains", http=http)

    # save for current session
    current_plus_service["user_email"] = user_email
    current_plus_service["service"] = service

    return service

def create_directory_service():
    f = file(API_ACCESS_DATA[CURRENT_DOMAIN]["SERVICE_ACCOUNT_PEM_FILE_PATH"], 'rb')
    key = f.read()
    f.close()

    credentials = SignedJwtAssertionCredentials(API_ACCESS_DATA[CURRENT_DOMAIN]["SERVICE_ACCOUNT_EMAIL"], key, scope=API_ACCESS_DATA[CURRENT_DOMAIN]["DIRECTORY_SCOPES"], sub=API_ACCESS_DATA[CURRENT_DOMAIN]["ADMIN_EMAIL"])
    http = httplib2.Http()
    http = credentials.authorize(http)
  
    # Construct a service from the local documents
    service = build("admin", "directory_v1", http=http)
    return service