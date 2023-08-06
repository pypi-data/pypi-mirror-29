from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView


@method_decorator(login_required, name='dispatch')
class IndexView(TemplateView):
    template_name = "index.html"