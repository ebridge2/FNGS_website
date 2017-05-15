from django.views.generic import RedirectView
from django.core.urlresolvers import reverse
from django.views.static import serve
from django.conf import settings


DOCS_ROOT = getattr(settings, 'DOCS_ROOT', None)
print(DOCS_ROOT)

def serve_docs(request, path, **kwargs):
	print(path)
	kwargs['document_root'] = DOCS_ROOT
	return serve(request, path, **kwargs)

class DocsRootView(RedirectView):
    def get_redirect_url(self, **kwargs):
    	print(kwargs)
        return reverse('docs:docfiles', kwargs={'path': 'index.html'})
