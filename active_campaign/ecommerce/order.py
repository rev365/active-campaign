import json


class ACProduct(object):
    """E-commerce product that is being ordered.

    Arguments:
        name {str} -- The name of the product
        price {double} -- The price of the product, in cents. (i.e. $456.78 => 45678).
                          Must be greater than or equal to zero.
        quantity {int} -- The quantity ordered.

    Optional Arguments:
        external_id {str} -- The id of the product in the external service.
        category {str} -- The category of the product.
        description {str} -- The description for the product.
        product_url {str} -- The URL for the product in the external service.
        image_url {str} -- The URL for the image for the product in the external service.
    """

    def __init__(
        self,
        *,
        name,
        price,
        quantity,
        external_id=None,
        category=None,
        description=None,
        product_url=None,
        image_url=None
    ):
        self.name = name
        self.price = str(price).replace('.', '')
        self.quantity = quantity
        self.external_id = external_id
        self.category = category
        self.description = description
        self.product_url = product_url
        self.image_url = image_url

    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price,
            'quantity': self.quantity,
            'external_id': self.external_id,
            'category': self.category,
            'description': self.description,
            'product_url': self.product_url,
            'image_url': self.image_url,
        }


class ACOrder(object):
    """E-Commerce order resources represent orders in an external e-commerce service.
    Before you can create any orders, you must have created a connection resource for the
    e-commerce service and a customer resource for the customer who placed the order.

    Arguments:
        client {ACClient} -- ACClient object.
        connection_id {int} -- The id of the connection from which this order originated.
    """
    SOURCE_SYNC = 0
    SOURCE_REALTIME_WEBHOOK = 1

    STATE_ORDERED = 1
    STATE_ABANDONED = 2

    def __init__(self, *, client, connection_id):
        self.client = client
        self.connection_id = connection_id

    def create(
        self,
        *,
        external_id,
        customer_id,
        email,
        products,
        currency,
        total_price,
        order_date,
        order_number=None,
        order_url=None,
        shipping_method=None,
        source=SOURCE_REALTIME_WEBHOOK
    ):
        """Create a new e-commerce order resource.

        Arguments:
            external_id {str} -- The id of the order in the external service.
            customer_id {int} -- The id of the customer associated with this order.
            email {str} -- The email address of the customer who placed the order.
            products {list of Product} -- The list of products being ordered.
            currency {str} -- The currency of the order (3-digit ISO code, e.g., 'USD').
            total_price {double} -- The total price of the order in cents, including
                                    tax and shipping charges. (i.e. $456.78 => 45678).
                                    Must be greater than or equal to zero.
            order_date {datetime} -- The date the order was placed.

        Optional Arguments:
            order_number {str} -- The order number in the external system
                                  This may differ from the external_id. (default: {None})
            order_url {str} -- The URL for the order in the external service. (default: {None})
            shipping_method {str} -- The shipping method of the order. (default: {None})
            source {int} -- The order source code. (default: {None})
                            0 - sync
                            1 - realtime webhook.

        Returns:
            bool -- True if success, False otherwise.
            dict -- Response of the /ecomOrders/ endpoint.
        """
        url = '{}/ecomOrders/'.format(self.client.base_url)
        payload = {
            'ecomOrder': {
                'connectionid': self.connection_id,
                'externalid': external_id,
                'customerid': customer_id,
                'email': email,
                'orderProducts': [product.to_dict() for product in products],
                'currency': currency,
                'totalPrice': str(total_price).replace('.', ''),
                'orderDate': str(order_date),
                'orderNumber': order_number,
                'orderUrl': order_url,
                'shippingMethod': shipping_method,
                'source': source,
            }
        }
        request = self.client.session.post(url, json=payload)
        return request.ok, json.loads(request.text)

    def abandon_cart(
        self,
        *,
        external_checkout_id,
        customer_id,
        email,
        products,
        currency,
        total_price,
        abandoned_date,
        external_created_date,
        order_number=None,
        order_url=None,
        external_updated_date=None,
        shipping_method=None,
        source=SOURCE_REALTIME_WEBHOOK
    ):
        """Create a new abandoned cart.

        Arguments:
            external_checkout_id {str} -- The id of the order in the external service.
            customer_id {int} -- The id of the customer associated with this order.
            email {str} -- The email address of the customer who placed the order.
            products {list of Product} -- The list of products being ordered.
            currency {str} -- The currency of the order (3-digit ISO code, e.g., 'USD').
            total_price {double} -- The total price of the order in cents, including
                                    tax and shipping charges. (i.e. $456.78 => 45678).
                                    Must be greater than or equal to zero.
            abandoned_date {datetime} -- The date the cart was abandoned.
            external_created_date {datetime} -- The date the abandoned cart was created.

        Optional Arguments:
            order_number {str} -- The order number in the external system
                                  This may differ from the external_id. (default: {None})
            order_url {str} -- The URL for the order in the external service. (default: {None})
            external_updated_date {datetime} -- The date the abandoned cart was updated. (default: {None})
            shipping_method {str} -- The shipping method of the order. (default: {None})
            source {int} -- The order source code. (default: {None})
                            0 - sync
                            1 - realtime webhook.

        Returns:
            bool -- True if success, False otherwise.
            dict -- Response of the /ecomOrders/ endpoint.
        """
        url = '{}/ecomOrders/'.format(self.client.base_url)
        payload = {
            'ecomOrder': {
                'connectionid': self.connection_id,
                'externalcheckoutid': external_checkout_id,
                'customerid': customer_id,
                'email': email,
                'orderProducts': [product.to_dict() for product in products],
                'currency': currency,
                'totalPrice': str(total_price).replace('.', ''),
                'abandonedDate': str(abandoned_date),
                'externalCreatedDate': str(external_created_date),
                'orderNumber': order_number,
                'orderUrl': order_url,
                'externalUpdatedDate': str(external_updated_date) if external_updated_date else None,
                'shippingMethod': shipping_method,
                'source': source,
            }
        }
        request = self.client.session.post(url, json=payload)
        return request.ok, json.loads(request.text)
