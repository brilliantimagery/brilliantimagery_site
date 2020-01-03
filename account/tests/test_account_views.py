from unittest.mock import patch


def test_register_get(register_get_request, db):
    from account.views import register

    response = register(register_get_request)
    expected_username_field = b'<input type="text" name="username" maxlength="150" autofocus class="textinput ' \
                              b'textInput form-control" required id="id_username">'

    assert response.status_code == 200
    assert b'Join Today' in response.content
    assert expected_username_field in response.content


def test_register_post_valid(register_valid_post_request, db_w_group):
    from account.views import register

    from unittest.mock import patch
    with patch('django.contrib.messages.success', return_value=None):
        with patch('account.views.login', return_value=None):
            with patch('django.contrib.messages.info', return_value=None):
                response = register(register_valid_post_request)
    assert response.status_code == 302
    assert response.url == '/'


# def test_register_post_user_exists(register_valid_post_request, db_w_group):
#     from account.views import register
#
#     from unittest.mock import patch
#     with patch('django.contrib.messages.success', return_value=None):
#         with patch('django.contrib.auth.login', return_value=None):
#             with patch('django.contrib.messages.info', return_value=None):
#                 response = register(register_valid_post_request)
#     assert response.status_code == 302
#     assert response.url == '/'


def test_register_post_password_mismatch(register_password_mismatch_post_request, db_w_group):
    from account.views import register

    from unittest.mock import patch
    with patch('django.contrib.messages.error', return_value=None):
        response = register(register_password_mismatch_post_request)
    assert response.status_code == 200
    assert b'<input type="text" name="username" value="user1" maxlength="150" autofocus ' \
           b'class="textinput textInput form-control" required id="id_username">' in response.content


def test_profile_not_logged_in(profile_anonymous_user_get_request):
    from account.views import profile

    response = profile(profile_anonymous_user_get_request)

    assert response.status_code == 302
    assert '/account/login/?next=/account/profile/' in response.url


def test_profile_logged_in_get(profile_logged_in_get_request, db):
    from account.views import profile

    response = profile(profile_logged_in_get_request)

    assert response.status_code == 200
    assert b'<input type="text" name="username" value="user1" maxlength="150" class="textinput ' \
           b'textInput form-control" required id="id_username">' in response.content
    assert b'Currently: <a href="/media/default.jpg">default.jpg</a>' in response.content


def test_profile_logged_in_post(profile_logged_in_post_request, db):
    from unittest.mock import patch
    from account.views import profile

    with patch('django.forms.forms.BaseForm.is_valid', return_value=True):
        with patch('django.forms.models.BaseModelForm.save'):
            with patch('django.contrib.messages.success'):
                response = profile(profile_logged_in_post_request)

    assert response.status_code == 302
    assert response.url == '/account/profile/'


def test_profile_logged_in_invalid_form_post(profile_logged_in_invalid_form_post_request, db):
    from account.views import profile

    response = profile(profile_logged_in_invalid_form_post_request)

    assert response.status_code == 200
    assert b'<input type="text" name="username" value="user1" maxlength="150" class="textinput ' \
           b'textInput form-control" required id="id_username">' in response.content


def test_login_get_request(login_get_request):
    from account.views import login_request

    response = login_request(login_get_request)

    assert response.status_code == 200
    assert b'<legend class="border-bottom mb-4">Log In</legend>' in response.content


def test_login_valid_user_post_request(login_w_valid_db_user_post_request):
    from account.views import login_request
    from unittest.mock import patch

    with patch('django.forms.forms.BaseForm.is_valid', return_value=True):
        with patch('account.views.AuthenticationForm'):
            with patch('account.views.authenticate', return_value=True):
                with patch('account.views.login'):
                    with patch('account.views.messages.info'):
                        response = login_request(login_w_valid_db_user_post_request)

    assert response.status_code == 302
    assert response.url == '/'


def test_login_invalid_user_post_request(login_w_valid_db_user_post_request):
    from account.views import login_request

    response = login_request(login_w_valid_db_user_post_request)

    assert response.status_code == 200
    assert b'<li>Please enter a correct username and password. ' \
           b'Note that both fields may be case-sensitive.</li>' in response.content


def test_login_user_not_found_post_request(login_w_valid_db_user_post_request):
    from account.views import login_request

    with patch('django.forms.forms.BaseForm.is_valid', return_value=True):
        with patch('account.views.AuthenticationForm'):
            with patch('account.views.authenticate', return_value=None):
                with patch('account.views.messages.error'):
                    response = login_request(login_w_valid_db_user_post_request)

    assert response.status_code == 200
    assert b'href="/account/login/">Login</a>' in response.content


def test_logout_request(logout_request_request):
    from account.views import logout_request
    from unittest.mock import patch

    with patch('account.views.logout'):
        with patch('django.contrib.messages.info', return_value=None):
            response = logout_request(logout_request_request)

    assert response.status_code == 302
    assert response.url == '/'


def test_privacy_policy_request(privacy_policy_request):
    from account.views import privacy_policy

    response = privacy_policy(privacy_policy_request)

    assert response.status_code == 200
    assert b'What We Gather and When' in response.content
