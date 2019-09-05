from django.contrib.auth import get_user_model
from django.utils import timezone

from accounts.models import DeviceInfo
from logs.models import LoginLog

User = get_user_model()


def get_client_ip(request):
    """
    request 의 ip 주소를 식별하는 함수입니다.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def loginlog_on_login(request, user):
    try:
        user.last_login = timezone.now()
        print(user)
        user.save()
        print('----')
        print(user.last_login)
        ip_ad = get_client_ip(request)
        print(ip_ad)
        device, _ = DeviceInfo.objects.get_or_create(device_type=request.device_type,
                                                     device_id=request.device_id)
        if hasattr(request, 'android_version'):
            LoginLog.objects.create(
                user=user,
                ip_address=ip_ad,
                device=device,
                client_type=LoginLog.ANDROID,
                client_user_type=request.client_user_type,
                app_id=request.app_id,
                version=request.android_version
            )
        elif hasattr(request, 'ios_version'):
            LoginLog.objects.create(
                user=user,
                ip_address=get_client_ip(request),
                device=device,
                client_type=LoginLog.IOS,
                client_user_type=request.client_user_type,
                app_id=request.app_id,
                version=request.ios_version
            )
        else:
            LoginLog.objects.create(user=user, ip_address=ip_ad)
    except Exception as e:
        pass