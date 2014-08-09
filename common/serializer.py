# -*- coding:utf-8 -*-
'''
##############################################################
# File: serializer.py
# Time: 2014/5/2
# 
# Function: 用于Django中对象传递到前端时的序列化工作，Json的
#           序列化只能够操作QuerySet实例，封装的MoodelEncoder
#           类根据传入的类型来进行封装，可以操作单个的
#           对象、QuerySet和日期类型的对象
##############################################################
'''

import json
from django.db import models
from django.core.serializers import serialize, deserialize
from django.db.models.query import QuerySet


class ModelEncoder(json.JSONEncoder):
    '''
    ModelEncoder类用于Django中对象数据的序列化
    '''
    def default(self, obj):
        if isinstance(obj, QuerySet):
            '''
            QuerySet实例直接使用Django内置的序列化工具
            如果直接返回serialize('json', obj),则在simplejson
            序列化时候会被当成字符串处理，会多出前后的双引号，
            因此这里先获得序列化后的对象，然后再用simplejson反
            序列化依次，得到一个标准的字典(dict)对象
            '''
            return json.loads(serialize('json', obj))

        if isinstance(obj, models.Model):
            '''
            如果传入的时单个对象，区别于QuerySet的就是Django不支持
            序列化单个对象，因此首先用单个对象来构造一个只有一个对
            象的数组，然后可以看做时是QuerySet对象。由于序列化QuerySet
            会被'[]'所包围，使用string[1:-1]来取出由于序列化QuerySet
            而带入的'[]'
            '''
            return json.loads(serialize('json', [obj])[1:-1])

        if hasattr(obj, 'isoformat'):
            #处理日期类型
            return obj.isoformat()

        return json.JSONEncoder.default(self, obj)
    
    def json_back(self, json_data):
        '''
        进行Json字符串的反序列化一般来说，从网络得回的POST（或者GET）
        参数中所包含json数据,例如，用POST传过来的参数中有一个key value键值对为
        request.POST['update']= "[{pk:1,name:'changename'},{pk:2,name:'changename2'}]"
        要将这个value进行反序列化,则可以使用Django内置的序列化与反序列化,但是问题在于
        传回的有可能是代表单个对象的json字符串如：
        request.POST['update'] = "{pk:1,name:'changename'}"
        这是，由于Django无法处理单个对象,因此要做适当的处理
        将其模拟成一个数组，也就是用'[]'进行包围,再进行反序列化
        '''
        if json_data[0] == '[':
            return deserialize('json', json_data)
        else:
            return deserialize('json', '['+json_data+']')


def get_json(**args):
    '''
    使用ModelEncoder这个自定义的规则类来序列化对象
    '''
    result = dict(args)
    return json.dumps(result, cls=ModelEncoder)
