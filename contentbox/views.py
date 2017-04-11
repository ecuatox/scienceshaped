from django.views.generic import UpdateView

from .models import ContentBox


class ContentBoxEdit(UpdateView):
    model = ContentBox
    fields = ['title', 'content', 'light']

    template_name = 'contentbox/contentbox.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return ContentBox.get(self.kwargs['title'])
