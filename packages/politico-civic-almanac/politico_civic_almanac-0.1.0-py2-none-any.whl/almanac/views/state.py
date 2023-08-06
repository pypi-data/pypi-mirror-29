from almanac.conf import settings as app_settings
from almanac.utils.auth import secure
from django.shortcuts import render
from django.views.generic import TemplateView

from geography.models import Division


@secure
class State(TemplateView):
    template_name = "almanac/state.live.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        context['state'] = Division.objects.get(
            slug=kwargs['state']
        )
        context['statics_path'] = '../../schedule'
        context['data'] = './data.json'
        context['ad_tag'] = ''
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['secret'] = app_settings.SECRET_KEY
        return context
