from hearthstonearenastats.app.draft.models import DraftStatus


class DraftStatusData(object):
    """A mixin for views to provide 'draft_status' in their context data.
    """
    def get_context_data(self, **kwargs):
        context = super(DraftStatusData, self).get_context_data(**kwargs)
        draft_status, created = DraftStatus.objects.get_or_create(
            user=self.request.user
        )
        context['draft_status'] = draft_status
        return context
