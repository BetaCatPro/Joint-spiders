# -*- coding: utf-8 -*-
import redis
def inserintota(str,type):
    try:
        r = redis.Redis(host='127.0.0.1', port=6379, db=0)
    except:
        print ('connect redis fail')
    else:
        if type == 2:
            r.lpush('ke:requests', str)