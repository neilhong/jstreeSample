# -*- coding:utf-8 -*-
import os, sys
from django.conf import settings
from django.core import urlresolvers
from django.core.exceptions import ImproperlyConfigured
from django.template import TemplateDoesNotExist, Origin
from django.template.loader import BaseLoader
from django.utils.importlib import import_module
import jinja2


class Template(jinja2.Template):
    '''
    Template类用于在Django中集成Jinja2模板
    '''
    def render(self, context):
        context_dict = {}
        for d in context.dicts:
            context_dict.update(d)

        if settings.TEMPLATE_DEBUG:
            from django.test import signals
            self.origin = Origin(self.filename)
            signals.template_rendered.send(
                    sender = self,
                    template = self,
                    context = context
                    )
        return super(Template, self).render(context_dict)


fs_encoding = sys.getfilesystemencoding() or sys.getdefaultencoding()
app_template_dirs = []
for app in settings.INSTALLED_APPS:
    try:
        mod = import_module(app)
    except ImportError, e:
        raise ImproperlyConfigured('ImportError %s: %s' %(app, e.args[0]))
    template_dir = os.path.join(os.path.dirname(mod.__file__), 'templates')
    if os.path.isdir(template_dir):
        app_template_dirs.append(template_dir.decode(fs_encoding))

class Loader(BaseLoader):
    '''
    用于初始化Jinja2模板
    '''
    #whether the loader can be used in this python installation
    is_usable = True

    #setup the jinja env and load any extension you may have
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(app_template_dirs))
    env.template_class = Template

    # These are available to all templates

    env.globals['BASE_DIR'] = settings.BASE_DIR
#    env.globals['BASE_URL'] = settings.BASE_URL
    env.globals['STATIC_URL'] = settings.STATIC_URL

    def load_template(self, template_name, template_dirs=None):
        try:
            template = self.env.get_template(template_name)
            return template, template.filename
        except jinja2.TemplateNotFound:
            raise TemplateDoesNotExist(template_name)

    def render_to_string(self, template_name, context={}):
        return self.env.get_template(template_name).render(**context)
