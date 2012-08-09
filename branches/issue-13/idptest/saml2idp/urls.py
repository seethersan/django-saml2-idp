from django.conf.urls.defaults import *
from views import descriptor, login_begin, login_init, login_process, logout
from django.conf import settings

def _deeplink_patterns():
    """
    Returns new deeplink URLs based on 'links' from settings.SAML2IDP_REMOTES.
    """
    resources = []
    for key, sp_config in settings.SAML2IDP_REMOTES.items():
        for resource, pattern in sp_config.get('links', {}).items():
            if '/' not in resource:
                # It's a simple deeplink, which is handled by 'login_init' URL.
                continue
            resources.append(resource)

    resources.sort()
    resources.reverse()
    new_patterns = []
    for resource in resources:
        new_patterns += patterns('',
            url( r'^init/' + resource + r'/$',
                 login_init,
                 {
                    'resource': resource,
                 },
            )
        )
    return new_patterns

urlpatterns = patterns('',
    url( r'^login/$', login_begin, name="login_begin"),
    url( r'^login/process/$', login_process, name='login_process'),
    url( r'^logout/$', logout, name="logout"),
    (r'^metadata/xml/$', descriptor),
    # For "simple" deeplinks:
    url( r'^init/(?P<resource>\w+)/(?P<target>\w+)/$', login_init, name="login_init"),
)
# Issue 13 - Add new automagically-created URLs for deeplinks:
urlpatterns += _deeplink_patterns()
