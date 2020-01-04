from django.contrib.auth.models import User


def test_NewUserForm_save(register_valid_post_request, db_w_group):
    from account.forms import NewUserForm
    from account.templatetags import user_utils

    request = register_valid_post_request
    form = NewUserForm(request.POST)
    form.save()

    user = User.objects.get(pk=1)

    assert user.username == request.POST.get('username')
    assert user.email == request.POST.get('email')
    assert user_utils.has_group(user, 'basic_web_user')
    assert user_utils.has_permission(user, 'do stuff')
