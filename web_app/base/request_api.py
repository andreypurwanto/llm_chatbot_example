from typing import List
from requests import Session, Response

# from web_app.api.external.slack import SlackAPI
from web_app.logs import LOG
from web_app.utils.requests import get_session_with_retries


class RequestAPI:
    def __init__(
        self,
        url: str,
        session: Session = None,
        timeout: int = 30,
        success_code: List[int] = [200,],
        retry_count: int = 0,
        notify: bool = False,
        notification_channel: str = '',
        slack_url: str = ''

    ) -> None:

        self.url = url
        self.success_code = success_code
        self.timeout = timeout
        self.retry_count = retry_count
        self.notify = notify
        self.notification_channel = notification_channel
        self.slack_url = slack_url
        self.session = get_session_with_retries() if not session else session
        if slack_url:
            # self.slack_api = SlackAPI(slack_url)
            self.slack_api = None

        self.__validate()

    def __validate(self):
        if self.notify and self.notification_channel == '':
            raise ValueError(
                'notification_channel cannot be empty if enable "notify"')

        if self.notification_channel == 'slack' and not self.slack_url:
            raise ValueError(
                'slack_url cannot be empty if notification_channel is slack')

        assert isinstance(
            self.session, Session), 'self.session must Session object'

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)

    def post(self, body: dict, headers: dict = None, endpoint: str = None, data=None) -> Session.request:
        if endpoint:
            url = f'{self.url}{endpoint}'
        else:
            url = self.url

        response = self.session.post(
            url=url,
            headers=headers,
            json=body,
            timeout=self.timeout,
            data=data,
        )

        self.send_notif(response)

        return response

    def get(self, body: dict, headers: dict = None, endpoint: str = None, data=None) -> Session.request:
        if endpoint:
            url = f'{self.url}{endpoint}'
        else:
            url = self.url

        response = self.session.get(
            url=url,
            headers=headers,
            json=body,
            timeout=self.timeout,
            data=data,
        )

        self.send_notif(response)

        return response

    def send_notif(self, response: Response):
        if not self.notify:
            return

        if response.status_code not in self.success_code:
            message = f'error send requests to: {response.url}, retry {self.retry_count} times, status code {response.status_code}'
            LOG.error(message)
            # if self.notification_channel == 'slack':
            #     self._send_slack_notif(message)