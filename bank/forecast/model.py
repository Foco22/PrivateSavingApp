import pandas as pd
from os import listdir
from os.path import join, isfile
from dateutil.relativedelta import relativedelta
from bank import models as models_bank
from django.db import transaction
from datetime import datetime
from dateutil.relativedelta import relativedelta
import json
import requests
import re
from bank import constants
import openai
from sqlalchemy import create_engine, text
import base64