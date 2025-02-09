from requests import Session
from requests.adapters import HTTPAdapter
from urllib3 import Retry


def get_session_with_retries():
    ''' 
    notes:

        1. {backoff factor} * (2 ** ({number of total retries} - 1)) 
        2. 525 : SSL Handshake Failed
        3. 526 : Invalid SSL Certificate
        4. 502 : Bad Gateway
        5. 104 : connection reset by peer

    '''
    session = Session()
    adapter = HTTPAdapter(
        max_retries=Retry(
            total=1,
            backoff_factor=0.1,
            status_forcelist=[525, 526, 502, 104],
        )
    )

    session.mount('http://', adapter)
    session.mount('https://', adapter)

    return session