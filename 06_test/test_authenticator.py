import pytest
from authenticator import Authenticator

# セットアップ(ユーザー未登録のAuthenticatorインスタンスを提供するfixture)
@pytest.fixture 
def auth():
    return Authenticator()

# セットアップ(ユーザー登録されたAuthenticatorインスタンスを提供するfixture)
@pytest.fixture
def auth_with_registered():
    auth = Authenticator()
    auth.users = {
        "user1": "pass1",
        "user2": "pass2",
    }
    return auth

# ユーザー登録 正常系
@pytest.mark.parametrize("username, password", [
    ("user1", "pass1"),
    ("user2", "pass2"),
])
def test_register_success(auth, username, password):
    assert auth.register(username, password) is None # ユーザー登録が成功することを検証

# ユーザー登録 異常系（既存ユーザーの登録）
def test_register_existing_user(auth):
    username = "user1"
    password = "pass1"
    auth.register(username, password)
    with pytest.raises(ValueError, match="エラー: ユーザーは既に存在します。"):
        auth.register(username, password)

# ログイン 正常系
@pytest.mark.parametrize("username, password", [
    ("user1", "pass1"),
    ("user2", "pass2"),])
def test_login_success(auth_with_registered, username, password):
    assert auth_with_registered.login(username, password) == "ログイン成功"

# ログイン 異常系 パスワードが間違っている場合
@pytest.mark.parametrize("username,wrong_password", [
    ("user1", "wrongpass"),
    ("user2", "wrongpass2"),
])
def test_login_wrong_password(auth_with_registered, username, wrong_password):
    with pytest.raises(ValueError, match="エラー: ユーザー名またはパスワードが正しくありません。"):
        auth_with_registered.login(username, wrong_password)
