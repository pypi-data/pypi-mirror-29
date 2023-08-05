


"""
    created 2017 by Jens Diemer <ya-publisher@jensdiemer.de>


"""


import datetime
import logging

from django.contrib.auth import get_user_model
from django.utils import timezone, translation
from django.utils.translation import ugettext_lazy as _

from cms.models import CMSPlugin

# https://github.com/jedie/django-cms-tools
from django_cms_tools.fixtures.pages import CmsPageCreator

from publisher.models import PublisherStateModel
from publisher_test_project.constants import REPORTER_USER
from publisher_test_project.publisher_list_app import constants
from publisher_test_project.publisher_list_app.models import PublisherItem

log = logging.getLogger(__name__)


class PublisherItemPageCreator(CmsPageCreator):
    """
    note:

    application_namespace == apphook_namespace == Application instance name
    """
    apphook = constants.LIST_APPHOOK
    apphook_namespace = constants.LIST_APPHOOK_NAMESPACE

    placeholder_slots = () # create a empty page, without dummy content

    def get_title(self, language_code, lang_name):
        return _("PublisherItems")



def list_item_fixtures():
    CMSPlugin.objects.filter(plugin_type=constants.LIST_APPHOOK).delete()

    log.info("Create %r CMS-Plugin...", constants.LIST_APPHOOK)
    PublisherItemPageCreator().create()

    User = get_user_model()
    ask_permission_user = User.objects.get(username=REPORTER_USER)

    language_code = "en"
    with translation.override(language_code):
        qs = PublisherItem.objects.all()
        log.info("Delete %i existing PublisherItems...", qs.count())
        qs.delete()

        list_items_queryset = PublisherItem.objects.visible()
        list_items_queryset = list_items_queryset.language(language_code=language_code)

        now = timezone.now()

        for no in range(1, 8):
            publication_start_date = None
            publication_end_date = None

            if no == 1:
                text = "Not published Item"
            elif no == 2:
                text = "Published Item"
            elif no == 3:
                text = "hidden by start date"
                publication_start_date = now + datetime.timedelta(days=1)
            elif no == 4:
                text = "hidden by end date"
                publication_end_date = now - datetime.timedelta(days=1)
            elif no == 5:
                text = "dirty"
            elif no == 6:
                text = "pending publish request"
            elif no == 7:
                text = "pending unpublish request"
            else:
                raise RuntimeError

            instance, created = list_items_queryset.get_or_create(
                translations__language_code=language_code,
                translations__text=text,
                defaults={
                    "text": text,
                    "publication_start_date": publication_start_date,
                    "publication_end_date": publication_end_date,
                },
            )

            if no not in (1, 6):
                instance.publish()

            if no == 6:
                PublisherStateModel.objects.request_publishing(
                    user=ask_permission_user,
                    publisher_instance=instance,
                )
            elif no == 7:
                PublisherStateModel.objects.request_unpublishing(
                    user=ask_permission_user,
                    publisher_instance=instance,
                )

            if text == "dirty":
                draft = instance.get_draft_object()
                draft.text = "This is dirty!"
                draft.save()

            if created:
                print("PublisherItem created:", instance)
            else:
                print("Existing PublisherItem:", instance)
