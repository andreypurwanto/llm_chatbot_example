from typing import List
from requests import Session, Response

# from web_app.api.external.slack import SlackAPI
from web_app.logs import LOG
from web_app.utils.requests import get_session_with_retries

class RequestAPI:
    """
    A utility class to handle HTTP requests with optional retry and notification support.
    """
    
    def __init__(
        self,
        url: str,
        session: Session = None,
        timeout: int = 30,
        success_code: List[int] = [200],
        retry_count: int = 0,
        notify: bool = False,
        notification_channel: str = '',
        slack_url: str = ''
    ) -> None:
        """
        Initializes the RequestAPI instance.
        """
        self.url = url
        self.success_code = success_code
        self.timeout = timeout
        self.retry_count = retry_count
        self.notify = notify
        self.notification_channel = notification_channel
        self.slack_url = slack_url
        
        # Use provided session or create one with retries
        self.session = get_session_with_retries() if not session else session
        
        # Slack API integration (currently disabled)
        self.slack_api = None  # Placeholder for Slack integration
        
        self.__validate()

    def __validate(self):
        """
        Validates required parameters for notifications.
        """
        if self.notify and not self.notification_channel:
            raise ValueError('notification_channel cannot be empty if "notify" is enabled')
        
        if self.notification_channel == 'slack' and not self.slack_url:
            raise ValueError('slack_url cannot be empty if notification_channel is slack')
        
        assert isinstance(self.session, Session), 'self.session must be a Session object'

    def __str__(self):
        return str(self.__class__) + ': ' + str(self.__dict__)

    def post(self, body: dict, headers: dict = None, endpoint: str = None, data=None) -> Response:
        """
        Sends a POST request.
        """
        url = f'{self.url}{endpoint}' if endpoint else self.url
        
        response = self.session.post(
            url=url,
            headers=headers,
            json=body,
            timeout=self.timeout,
            data=data,
        )
        
        self.send_notif(response)
        return response

    def get(self, body: dict, headers: dict = None, endpoint: str = None, data=None) -> Response:
        """
        Sends a GET request.
        """
        url = f'{self.url}{endpoint}' if endpoint else self.url
        
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
        """
        Logs an error if the request fails and notification is enabled.
        """
        if not self.notify:
            return
        
        if response.status_code not in self.success_code:
            message = (f'Error sending request to: {response.url}, '
                       f'retried {self.retry_count} times, status code {response.status_code}')
            LOG.error(message)
            # Placeholder for Slack notification integration