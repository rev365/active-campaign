import requests


class ACClient(object):
    """ACClient initializes the needed credentials for authentication in ActiveCampaign.

    Arguments:
        account {str} -- Name of the account.
        api_token {str} -- API token from a specific account.
    """

    def __init__(self, *, account, api_token):
        self.base_url = 'https://{account}.api-us1.com/api/3'.format(account=account)

        self.session = requests.Session()
        self.session.headers.update({'Api-Token': api_token})
        self.session.timeout = 5
