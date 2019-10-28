# -*- encoding: utf-8 -*-
import pytz
from django.conf.urls import url
from django.contrib import admin, messages
from django.contrib.admin.options import IS_POPUP_VAR
from django.contrib.admin.utils import unquote
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.core.exceptions import PermissionDenied
from django.http import Http404, HttpResponseRedirect
from django.template.response import TemplateResponse
from django.urls import reverse
from django.utils.encoding import force_text
from django.utils.html import escape
from django.utils.translation import ugettext_lazy as _
from accounts.models import MondeUser, DeleteUser
from logs.models import BannedUserLog
from manage.sites import staff_panel
from manage.tools import export_as_csv

# Proxy model
from manage.pagination import FixedCountAdminPaginator


class User(MondeUser):
    class Meta:
        verbose_name_plural = '회원'
        proxy = True


# Django 기본 UserAdmin을 따라해서 만듬.
# ref : https://github.com/django/django/blob/1.9.5/django/contrib/auth/admin.py

def get_timezone_string(input_date, format_string='%Y.%m.%d %H:%M:%S'):
    return input_date.astimezone(pytz.timezone('Asia/Seoul')).strftime(format_string)


class AbstractUserAdmin(admin.ModelAdmin):
    list_per_page = 100

    list_filter = ['groups__name', ]
    actions = ['set_banned', 'unset_banned', export_as_csv(), ]

    search_fields = ['age', 'uid']

    fieldsets = (
        (None, {'fields': ('email', 'uid')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff',)}),
        (_('Important dates'), {'fields': ('_last_login', '_created_at',)}),
        (_('Password'), {'fields': ('change_password_link', 'change_temporary_password_link',)}),
    )

    readonly_fields = ['_created_at', '_last_login', 'change_password_link', 'change_temporary_password_link']

    def nickname(self, user):
        if user.is_active:
            return user.nickname
        return '[탈퇴] %s' % user.nickname

    nickname.short_description = u'닉네임'

    def _last_login(self, user):
        if user.last_login is not None:
            return get_timezone_string(user.last_login)
        return u''

    _last_login.short_description = u'마지막 로그인'

    def _created_at(self, user):
        return get_timezone_string(user.created_at)

    _created_at.short_description = u'회원가입일'

    def is_member(self, user):
        if user.groups.filter(name='members').exists():
            return u'O'
        return u'X'

    is_member.short_description = '멤버'

    # actions
    # def set_member(self, request, queryset):
    #     group = Group.objects.get(name='members')
    #     rows_updated = queryset.count()
    #     for user in queryset.all():
    #         user.groups.add(group)
    #     self.message_user(request, '%d개의 아이디를 members로 설정했습니다.' % rows_updated)
    #
    # set_member.short_description = 'members 설정'
    #
    # def unset_member(self, request, queryset):
    #     group = Group.objects.get(name='members')
    #     rows_updated = queryset.count()
    #     for user in queryset.all():
    #         user.groups.remove(group)
    #     self.message_user(request, '%d개의 아이디를 members에서 해제했습니다.' % rows_updated)
    #
    # unset_member.short_description = 'members 해제'

    def set_banned(self, request, queryset):
        rows_updated = queryset.count()
        for user in queryset.all():
            user.is_banned = True
            user.save()
            BannedUserLog.objects.create(user=user, reason="Banned by staff")
        self.message_user(request, '%d개의 아이디를 제재했습니다. (BannedUserLog 사유를 기록해주세요)' % rows_updated)

    set_banned.short_description = '아이디 제재'

    def unset_banned(self, request, queryset):
        rows_updated = queryset.count()
        for user in queryset.all():
            user.is_banned = False
            user.save()
            BannedUserLog.objects.create(user=user, reason="Unbanned by staff")
        self.message_user(request, '%d개의 아이디를 해제했습니다.' % rows_updated)

    unset_banned.short_description = '아이디 제재 해제'

    # 비밀번호 변경 form
    # ref : https://github.com/django/django/blob/1.9.5/django/contrib/auth/admin.py
    change_password_form = AdminPasswordChangeForm

    def change_password_link(self, user):
        return '<a href="password/">click</a>'

    change_password_link.allow_tags = True
    change_password_link.short_description = '비밀번호 변경'

    def change_temporary_password_link(self, user):
        return '<a href="temporary_password/">click</a>'

    change_temporary_password_link.allow_tags = True
    change_temporary_password_link.short_description = '임시 비밀번호 변경 (원본 비밀번호는 유지됩니다)'

    def get_urls(self):
        return [
                   url(
                       r'^(.+)/change/password/$',
                       self.admin_site.admin_view(self.user_change_password),
                       name='auth_user_password_change',
                   ),
                   url(
                       r'^(.+)/change/temporary_password/$',
                       self.admin_site.admin_view(self.user_change_temporary_password),
                       name='auth_user_temporary_password_change',
                   ),
               ] + super(AbstractUserAdmin, self).get_urls()

    def user_change_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = self.get_object(request, unquote(id))
        if user is None:
            raise Http404('%(name)s object with primary key %(key)r does not exist.' % {
                'name': force_text(self.model._meta.verbose_name),
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                form.save()
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = 'Password changed successfully.'
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': 'Change password: %s' % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        context.update(self.admin_site.each_context(request))

        request.current_app = self.admin_site.name

        return TemplateResponse(request, 'admin/auth/user/change_password.html', context)

    def user_change_temporary_password(self, request, id, form_url=''):
        if not self.has_change_permission(request):
            raise PermissionDenied
        user = self.get_object(request, unquote(id))
        if user is None:
            raise Http404('%(name)s object with primary key %(key)r does not exist.' % {
                'name': force_text(self.model._meta.verbose_name),
                'key': escape(id),
            })
        if request.method == 'POST':
            form = self.change_password_form(user, request.POST)
            if form.is_valid():
                # 수동 구현
                from django.contrib.auth.hashers import make_password
                user.temporary_password = make_password(form.data['password1'])
                user.save()
                # 이후는 django default 구현
                change_message = self.construct_change_message(request, form, None)
                self.log_change(request, user, change_message)
                msg = 'Password changed successfully.'
                messages.success(request, msg)
                update_session_auth_hash(request, form.user)
                return HttpResponseRedirect(
                    reverse(
                        '%s:%s_%s_change' % (
                            self.admin_site.name,
                            user._meta.app_label,
                            user._meta.model_name,
                        ),
                        args=(user.pk,),
                    )
                )
        else:
            form = self.change_password_form(user)

        fieldsets = [(None, {'fields': list(form.base_fields)})]
        adminForm = admin.helpers.AdminForm(form, fieldsets, {})

        context = {
            'title': 'Change password: %s' % escape(user.get_username()),
            'adminForm': adminForm,
            'form_url': form_url,
            'form': form,
            'is_popup': (IS_POPUP_VAR in request.POST or
                         IS_POPUP_VAR in request.GET),
            'add': True,
            'change': False,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_absolute_url': False,
            'opts': self.model._meta,
            'original': user,
            'save_as': False,
            'show_save': True,
        }
        context.update(self.admin_site.each_context(request))

        request.current_app = self.admin_site.name

        return TemplateResponse(request, 'admin/auth/user/change_password.html', context)


class UserAdmin(AbstractUserAdmin):
    list_display = ['id',
                    'nickname',
                    'uid',
                    'age',
                    'birth_year',
                    '_created_at',
                    '_last_login', ]


    actions = [
        'set_banned',
        'unset_banned',
    ]

    list_per_page = 20
    # show_full_result_count = False
    paginator = FixedCountAdminPaginator
    exclude = ['set_banned', 'unset_banned', export_as_csv(), ]


class DeleteUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'str_withdrawal_reasons', 'created_at']
    raw_id_fields = ['user']

    def str_withdrawal_reasons(self, obj):
        reason = ''
        for idx, withdrawal_reasons in enumerate(obj.withdrawal_reasons.all()):
            reason += withdrawal_reasons.withdrawal_reason
            if idx != obj.withdrawal_reasons.all():
                reason += '<br>'
        return reason

    str_withdrawal_reasons.short_description = u'탈퇴이유'
    str_withdrawal_reasons.allow_tags = True


staff_panel.register(User, UserAdmin)
staff_panel.register(DeleteUser, DeleteUserAdmin)
