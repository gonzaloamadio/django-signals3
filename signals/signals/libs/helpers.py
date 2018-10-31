# -*- coding: utf-8 -*-
import string
import random
from datetime import datetime, timedelta, date
from random import choice, randint
import logging
import hashlib

#logging.basicConfig(level=logging.DEBUG,
#                     format='%(asctime)s %(levelname)-8s %(message)s',
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='log_back_emedido.log',
#                     filemode='a')
#log = logging.getLogger('back_emedido')


def to_epoch(date, miliseconds=True):
    """
        The Unix epoch (or Unix time or POSIX time or Unix timestamp) is the number of seconds that have elapsed since January 1, 1970
    """
    seconds = int((date - datetime(1970,1,1)).total_seconds())
    if miliseconds:
        ret = seconds * 1000
    else:
        ret = seconds
    return ret

def this_year():
      return int(datetime.now().year)

def weekday_to_str(num):
    data = {
        '0' : 'mon',
        '1' : 'tue',
        '2' : 'wed',
        '3' : 'thu',
        '4' : 'fri',
        '5' : 'sat',
        '6' : 'sun'
    }

    return data.get(str(num))

def gen_secret_key(numero):
    return ''.join(random.choice(string.ascii_lowercase + string.ascii_uppercase + string.digits) for _ in range(numero))

def gen_random_num_of_length(n):
    """
        Gen random number of n cyphers.
    """
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

# ####################
# FORMAT DICTIONARIES

# "data": [
# {
   # "cost_price": 10,
   # "id": 1,
   # "valid": true
   # .....
# }
# ],

#  FORMATED TO:

# "data": {
# "1" : {
   # "cost_price": 10,
   # "id": 1,
   # "valid": true
   # .....
# }
# },

def list_to_dict(lista):
    """
        Argument: list of objects.
        Output: Dict where key is the ID, and value the hole object.
    """
    ret = {}
    try:
        for obj in lista:
            clave = obj.get('id')
            if clave:
                ret[clave] = obj
        return ret
    except Exception as e:
#        return ret
        raise Exception("[list_to_dict] Error prcessing data.")

# ----------------------------------------------------------------------------
#                    OBTENCION DE PARAMETROS
# ----------------------------------------------------------------------------

def get_setting_param(key):
    try:
        par = Parameter.objects.get(key=key)
        if par.typeof == "Char":
            return Parameter.objects.get(key=key).value
        elif par.typeof == "Int":
            return int(Parameter.objects.get(key=key).value)
        elif par.typeof == "Float":
            return float(Parameter.objects.get(key=key).value)
        else:
            raise Exception("Parameter type not recognised.")
    except Parameter.DoesNotExist:
        raise Exception("Parameter not existent.")

