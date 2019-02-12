import json

from active_campaign.base import BaseAC


class ACCustomer(BaseAC):
    """E-commerce customer resources represent a customer in an external e-commerce service.
    Customer resources primarily hold aggregate e-commerce data associated with a contact.

    Arguments:
        client {ACClient} -- ACClient object.
        connection_id {int} -- The id of the connection object for the service
                                   where the customer originates.
    """

    def __init__(self, *, client, connection_id):
        self.client = client
        self.connection_id = connection_id

    def create(self, *, external_id, email):
        """Create a new e-commerce customer resource.

        Arguments:
            external_id {str} -- The id of the customer in the external service.
            email {str} -- The email address of the customer.

        Returns:
            bool -- True if success, False otherwise.
            dict -- Response of the /ecomCustomers/ endpoint.
        """
        url = '{}/ecomCustomers/'.format(self.client.base_url)
        payload = {
            'ecomCustomer': {
                'connectionid': self.connection_id,
                'externalid': external_id,
                'email': email,
            }
        }
        request = self.client.session.post(url, json=payload)
        return request.ok, json.loads(request.text)

    def list(self, filters={}, ordering={}, limit=20, offset=0):
        """List all e-commerce customer resources.

        Optional Arguments:
            filters {dict} -- To apply multiple, convention oriented filters to a request. (default: {{}})
                              key - Field name
                              value - Value to fitler by
            ordering {dict} -- To apply multiple sorting criteria to a request. (default: {{}})
                               key - Field name
                               value - ASC = Ascending order
                                       DESC = Descending order
            limit {int} -- The number of results to display in each page. (default: {20}; max: {100})
            offset {int} -- The starting point for the result set of a page. (default: {0})

        Returns:
            bool -- True if success, False otherwise.
            dict -- Response of the /ecomCustomers/ endpoint.
        """

        url = '{}/ecomCustomers/'.format(self.client.base_url)
        payload = {
            limit: limit,
            offset: offset
        }
        payload.update(self.format_filters(filters))
        payload.update(self.format_ordering(ordering))

        request = self.client.session.get(url, params=payload)
        return request.ok, json.loads(request.text)
