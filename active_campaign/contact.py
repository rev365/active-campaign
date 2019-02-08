import json


class ACContact(object):
    """Contacts represent the people that the owner of an ActiveCampaign account
    is marketing to or selling to.

    Arguments:
        client {ACClient} -- ACClient object.
    """
    STATUS_SUBSCRIBE = '1'
    STATUS_UNSUBSCRIBE = '2'

    def __init__(self, *, client):
        self.client = client

    def create_or_update(
        self,
        *,
        email,
        first_name='',
        last_name='',
        phone='',
        org_id=None,
        deleted=False
    ):
        """Creates or updates a contact.

        Arguments:
            email {str} -- Email address of the contact

        Optional Arguments:
            first_name {str} -- First name of the contact. (default: {''})
            last_name {str} -- Last name of the contact. (default: {''})
            phone {str} -- Phone number of the contact. (default: {''})
            org_id {int} -- Organization the contact belongs to. (default: {None})
            deleted {bool} -- True if to delete contact, False otherwise. (default: {False})

        Returns:
            bool -- True if success, False otherwise.
            dict -- Response of the /contact/sync/ endpoint.
        """
        url = '{}/contact/sync/'.format(self.client.base_url)
        payload = {
            'contact': {
                'email': email,
                'firstName': first_name,
                'lastName': last_name,
                'phone': phone,
                'orgid': org_id,
                'deleted': deleted,
            }
        }
        request = self.client.session.post(url, json=payload)

        return request.ok, json.loads(request.text)

    def retrieve(self, id):
        """Retrieve the contact details

        Arguments:
            id {int} -- ID of the contact

        Returns:
            bool -- True if success, False otherwise.
            dict -- Response of the /contacts/:id/ endpoint.
        """
        url = '{}/contacts/{}'.format(self.client.base_url, id)
        request = self.client.session.get(url)
        return request.ok, json.loads(request.text)

    def update_list_status(self, *, list, contact, status):
        """Subscribe a contact to a list or unsubscribe a contact from a list.

        Arguments:
            list {int} -- ID of the list to subscribe the contact to.
            contact {int} -- ID of the contact to subscribe to the list.
            status {int} -- Set to "1" to subscribe the contact to the list.
                            Set to "2" to unsubscribe the contact from the list.

        Returns:
            bool -- True if success, False otherwise.
            dict -- Response of the /contactLists/ endpoint.
        """
        url = '{}/contactLists/'.format(self.client.base_url)
        payload = {
            'contactList': {
                'list': list,
                'contact': contact,
                'status': status,
            }
        }
        request = self.client.session.post(url, json=payload)
        return request.ok, json.loads(request.text)
