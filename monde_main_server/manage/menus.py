# -*- encoding: utf-8 -*-

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from wpadmin.menu.menus import items, Menu
from wpadmin.utils import get_admin_site_name


class TitleMenuItem(items.MenuItem):
    def is_selected(self, request):
        return False


# Superadmin

class AdminTopMenu(Menu):

    def init_with_context(self, context):
        admin_site_name = get_admin_site_name(context)

        if 'django.contrib.sites' in settings.INSTALLED_APPS:
            from django.contrib.sites.models import Site
            site_name = Site.objects.get_current().name + ' 최고관리자'
        else:
            site_name = 'Site'

        self.children += [
            TitleMenuItem(
                title=site_name,
                url=reverse('%s:index' % admin_site_name),
                icon='fa-bullseye',
                css_styles='font-size: 1.5em;',
            ),
            items.UserTools(
                css_styles='float: right;',
                is_user_allowed=lambda user: user.is_staff,
            ),
        ]


class AdminLeftMenu(Menu):
    """
    Custom Menu for Monde admin site.
    """

    def is_user_allowed(self, user):
        """
        Only users that are staff are allowed to see this menu.
        """
        return user.is_superuser

    def init_with_context(self, context):

        if self.is_user_allowed(context.get('request').user):

            admin_site_name = get_admin_site_name(context)

            self.children += [
                items.MenuItem(
                    title='Dashboard',
                    icon='fa-tachometer',
                    url=reverse('%s:index' % admin_site_name),
                    description='Dashboard',
                ),
                items.AppList(
                    title='Applications',
                    description='Applications',
                    exclude=('django.contrib.*',),
                    icon='fa-tasks',
                ),
                items.AppList(
                    title='Administration',
                    description='Administration',
                    models=('django.contrib.*',),
                    icon='fa-cog',
                ),
            ]


# staff

class StaffTopMenu(Menu):

    def init_with_context(self, context):
        admin_site_name = get_admin_site_name(context)

        if 'django.contrib.sites' in settings.INSTALLED_APPS:
            from django.contrib.sites.models import Site
            site_name = Site.objects.get_current().name + ' 관리자'
        else:
            site_name = 'Site'

        self.children += [
            TitleMenuItem(
                title=site_name,
                url=reverse('%s:index' % admin_site_name),
                icon='fa-bullseye',
                css_styles='font-size: 1.5em;',
            ),
            items.UserTools(
                css_styles='float: right;',
                is_user_allowed=lambda user: user.is_staff,
            ),
        ]


class StaffLeftMenu(Menu):
    """
    Custom Menu for Monde admin site.
    """

    def is_user_allowed(self, user):
        """
        Only users that are staff are allowed to see this menu.
        """
        return user.is_staff

    def init_with_context(self, context):

        if self.is_user_allowed(context.get('request').user):

            admin_site_name = get_admin_site_name(context)

            self.children += [
                items.MenuItem(
                    title='Dashboard',
                    url=reverse('%s:index' % admin_site_name),
                    icon='fa-tachometer',
                ),
                items.ModelList(
                    title='회원 관리',
                    models=(
                        'accounts.admin.*',
                        'accounts.models.MondeUser',
                        'accounts.models.UserWithdrawalReason',
                        'accounts.models.DeleteUser',
                    ),
                    url=reverse('staff:accounts_user_changelist'),
                    icon='fa-users',
                ),
                items.ModelList(
                    title='일러스트 관리',
                    models=(
                        'cateiees.*',
                    ),
                    url=reverse('staff:categories_illust_changelist'),
                    icon='fa-question-circle',
                ),
                items.ModelList(
                    title='1:1 문의 관리',
                    models=(
                        'support.models.MondeSupport',),
                    url=reverse('staff:support_contact_changelist'),
                    icon='fa-envelope-o',
                ),
                items.ModelList(
                    title='운영',
                    models=(
                        'support.models.Official',
                        'notices.models.FAQ',
                        'support.models.Notice',),
                    url=reverse('staff:support_official_changelist'),
                    icon='fa-briefcase',
                ),
                items.ModelList(
                    title='데이터 관리',
                    models=(
                        'versions.models.Version',
                        ),
                    url=reverse('staff:versions_version_changelist'),
                    icon='fa-android',
                ),
                items.ModelList(
                    title='로그',
                    models=(
                        'logs.models.*',
                        ),
                    exclude=(
                        'logs.models.DBProductSyncLogs',
                    ),
                    url=reverse('staff:logs_userlog_changelist'),
                    icon='fa-file-text',
                ),
            ]
