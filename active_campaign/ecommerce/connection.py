import json

from active_campaign.base import BaseAC


class ACConnection(BaseAC):
    """Deep Data connection resources represent a link between an ActiveCampaign account
    and an account in some external service. This is intended to be used by third-parties
    who create integrations between such services and ActiveCampaign.

    Arguments:
        client {ACClient} -- ACClient object.
    """

    def __init__(self, *, client):
        self.client = client

    def create(self, *, service, external_id, name, logo_url, link_url):
        """Create a new connection resource.

        Arguments:
            service {str} -- The name of the service.
            external_id {str} -- The id of the account in the external service.
            name {str} -- The name associated with the account in the external service.
                          Often this will be a company name.
            logo_url {str} -- The URL to a logo image for the external service.
            link_url {str} -- The URL to a page where the integration with the external
                              service can be managed in the third-party's website.

        Returns:
            bool -- True if success, False otherwise.
            dict -- Response of the /connections/ endpoint.
        """
        url = '{}/connections/'.format(self.client.base_url)
        payload = {
            'connection': {
                'service': service,
                'externalid': external_id,
                'name': name,
                'logoUrl': logo_url,
                'linkUrl': link_url,
            }
        }
        request = self.client.session.post(url, json=payload)
        return request.ok, json.loads(request.text)

    def list(self, filters={}, ordering={}, limit=20, offset=0):
        """List all existing connection resources.

        Optional Arguments:
            filters {dict} -- To apply multiple, convention oriented filters to a request. (default: {{}})
                              key - Field name
                              value - Value to filter by
            ordering {dict} -- To apply multiple sorting criteria to a request. (default: {{}})
                               key - Field name
                               value - ASC = Ascending order
                                       DESC = Descending order
            limit {int} -- The number of results to display in each page. (default: {20}; max: {100})
            offset {int} -- The starting point for the result set of a page. (default: {0})

        Returns:
            bool -- True if success, False otherwise.
            dict -- Response of the /connections/ endpoint.
        """

        url = '{}/connections/'.format(self.client.base_url)
        payload = {
            limit: limit,
            offset: offset,
        }
        payload.update(self.format_filters(filters))
        payload.update(self.format_ordering(ordering))

        request = self.client.session.get(url, params=payload)
        return request.ok, json.loads(request.text)
