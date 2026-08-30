"""Integration check for cookie files mounted individually by Docker."""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import Config


cookie_value = b'BAHARUNE=bind-mounted-invalid-cookie'
with open(Config.cookie_path, 'wb') as cookie_file:
    cookie_file.write(cookie_value)
with open(Config.cookie_path.replace('cookie.txt', 'invalid_cookie.txt'), 'wb') as invalid_cookie_file:
    invalid_cookie_file.write(b'older-cookie')

Config.invalid_cookie()

with open(Config.cookie_path, 'rb') as cookie_file:
    assert cookie_file.read() == b''
with open(Config.cookie_path.replace('cookie.txt', 'invalid_cookie.txt'), 'rb') as invalid_cookie_file:
    assert invalid_cookie_file.read() == cookie_value
assert os.path.exists(Config.cookie_path)

print('bind-mounted cookie invalidation passed')
