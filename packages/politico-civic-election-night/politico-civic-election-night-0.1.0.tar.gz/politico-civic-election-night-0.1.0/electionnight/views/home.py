from django.views.generic import TemplateView


class DevHome(TemplateView):
    template_name = "electionnight/preview.html"
