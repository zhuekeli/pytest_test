import pytest


@pytest.mark.parametrize('passwd', ['123456', 'abcdefdfs', 'as52345fasdf4'])
def test_passwd_length(passwd):
    """
    这是一个密码长度的测试，会执行三遍
    """
    assert len(passwd) >= 8, '密码长度小于 8 位'


@pytest.mark.parametrize('user, passwd',
                         [('jack', 'abcdefgh'),
                          ('tom', 'a123456a')])
def test_passwd_md5(user, passwd):
    """
    多参数示例
    """
    db = {
        'jack': 'e8dc4081b13434b45189a720b77b6818',
        'tom': '1702a132e769a623c1adb78353fc9503'
    }
    import hashlib
    assert hashlib.md5(passwd.encode()).hexdigest() == db[user]


if __name__ == '__main__':
    pytest.main()
