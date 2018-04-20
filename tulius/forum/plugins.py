from django import urls
from django.utils.decorators import classonlymethod
from django.views.generic import TemplateView
from django.template import RequestContext, loader
from django.core.exceptions import PermissionDenied
from django.contrib.auth.views import redirect_to_login


class ForumPlugin(object):
    site = None
    core = None
    templates = None
    urlizer = None
    signals = None
    
    def __init__(self, site):
        self.site = site
        self.site_id = site.site_id
        self.models = site.core.models
        self.core = {}
        self.templates = {}
        self.urlizer = {}
        self.signals = {}
        self.init_core()
        
    def check_dependencies(self, plugins):
        pass
    
    def init_core(self):
        pass
    
    def post_init(self):
        pass
    
    def get_urls(self):
        return []
    
    def reverse(self, viewname, *args, **kwargs):
        return urls.reverse(
            self.site.name + ':' + viewname, args=args, kwargs=kwargs)

    
class BasePluginView(TemplateView):
    plugin = None
    require_user = False
    
    def __init__(self, **kwargs):
        super(BasePluginView, self).__init__(**kwargs)
        self.site = self.plugin.site
        self.core = self.site.core

    @classonlymethod
    def as_view(self, plugin, **initkwargs):
        initkwargs['plugin'] = plugin
        return super(BasePluginView, self).as_view(**initkwargs)
    
    def get_context_data(self, **kwargs):
        if self.require_user and self.request.user.is_anonymous:
            raise PermissionDenied()
        return {'forum_site': self.site, 'core': self.core}
    
    def render_to_response(self, context, **response_kwargs):
        return super(BasePluginView, self).render_to_response(
            context, current_app=self.site.app_name, **response_kwargs)
    
    def get_template_names(self):
        return [self.site.templates[self.template_name]]
    
    def render(self, context_data=None, **kwargs):
        if context_data is None:
            context_data = self.get_context_data(**kwargs)
        context = RequestContext(
            self.request, context_data, current_app=self.site.app_name)
        template = self.get_template_names()
        if isinstance(template, (list, tuple)):
            t = loader.select_template(template)
        elif isinstance(template, str):
            t = loader.get_template(template)
        return t.render(context)

    def dispatch(self, request, *args, **kwargs):
        if self.require_user and (not request.user.is_authenticated):
            return redirect_to_login(request.build_absolute_uri())
        try:
            return super(BasePluginView, self).dispatch(
                request, *args, **kwargs)
        except PermissionDenied:
            if not request.user.is_authenticated:
                return redirect_to_login(request.build_absolute_uri())
            else:
                raise
