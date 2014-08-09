# -*- coding: utf8 -*-
from django.shortcuts import render

import os
import re
import json
import time
import traceback
from django.utils.encoding import smart_str
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template.loader import render_to_string

def index(request):
    return render_to_response("index.html", {})

def get_list_by_id(node, with_root):
    dir_path = os.path.join(settings.DOCUMENT_DIR, node.lstrip('/'))
    ret = []

    if(with_root is True and node == '/'):
        ret.append({
                'text':     '/',
                'children': True,
                'id':       '/',
                'state':    {'opened': True},
                })
        return ret

    try:
        dir_path_list = os.listdir(dir_path)
        for item in dir_path_list:
            if(item is None or item.startswith('.')):
                continue
            cur_item_path = os.path.join(dir_path, item.lstrip('/'))
            if(os.path.isdir(cur_item_path)):
                ret.append({
                        'text':     item,
                        'children': True,
                        'id':       cur_item_path[len(settings.DOCUMENT_DIR):],
                        })
            else:
                cur_text = item
                if cur_text.endswith('.md'):
                    cur_text = cur_text[:-3]
                ret.append({
                        'text':     cur_text,
                        'children': False,
                        'id':       cur_item_path[len(settings.DOCUMENT_DIR):],
                        'type':     'file'
                        })
    except:
        print traceback.format_exc()
    return ret

def get_list(request):
    ret = []
    if not request.is_ajax() or request.method != 'GET':
        return HttpResponse(json.dumps(ret))
    
    req_id = request.GET.get('id')

    if req_id is not None:
        req_id = smart_str(req_id)
    
    node = req_id
    if node is None or node == '#':
        node = '/'

    with_root = False
    if req_id is not None and req_id == '#':
        with_root = True
    ret = get_list_by_id(node, with_root)
    return HttpResponse(json.dumps(ret))
