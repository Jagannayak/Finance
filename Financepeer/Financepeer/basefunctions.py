from bson.objectid import ObjectId
from .settings import dbcursor
from datetime import datetime
from time import strftime, strptime

from django.http import HttpResponse, response, JsonResponse
from django.views import View
from bson.json_util import loads,dumps
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from django.template.loader import get_template 
from threading import Thread
from smtplib import SMTP
from datetime import datetime,timedelta
import gzip
import tempfile
# from datetime import timedelta
import string
import random
import time
import os
from .settings import *
from hashlib import sha256
from uuid import uuid4
from django.shortcuts import render, redirect
import pandas as pd
import json

from django.views import View
def hash_password(password):
	return sha256(password.encode()).hexdigest()

def verifyToken(token, response):
	checkData = loads(dumps(dbcursor.users.find_one({"token":token})))
	response.update({"message":"Data not found"})
	if checkData:
		response.update({"message":"token Verified", "code":200, "status":"success"})
	return response
