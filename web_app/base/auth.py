import base64
from web_app.constant.api import WEB_PASS_AUTH, WEB_USER_AUTH
from web_app.logs import LOG
from typing import Tuple


class BasicAuth:
    def __init__(self) -> None:
        self.users = {
            'eryops': {
                'auth': WEB_PASS_AUTH,
                'user': WEB_USER_AUTH
            }
        }

    def get_all_basic_auth(self) -> list:
        basic_auth = []
        for user in self.users:
            res, val = self.__encoder(
                self.users[user]['user'], self.users[user]['auth'])
            if res:
                basic_auth.append(f'Basic {val}')
        return basic_auth

    def __encoder(self, user: str, password: str) -> Tuple[bool, str]:
        try:
            auth_bytes = f'{user}:{password}'.encode(
                "ascii")
            auth_base64_bytes = base64.b64encode(auth_bytes)
            return True, auth_base64_bytes.decode("ascii")
        except Exception as e:
            LOG.error(f'faile encode base 64 {e}', exc_info=True)
            return False, ''
