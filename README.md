# ActiveCampaign

The ActiveCampaign Python library provides convenient access to the [ActiveCampaign version 3](https://developers.activecampaign.com/v3/reference) of the API endpoints from applications written in the Python language.

## Installation

`pip install active_campaign`

## Requirements

- Python 2.7+ or Python 3.4+

## Documentation

### Pagination

Endpoints that return collections of resources must limit the number of records returned in a given response.

Name                    | Type                 | Description
------------------------|----------------------|-
limit                   | int                  | Number of results to display in each page (default = 20; max = 100)
offset                  | int                  | Starting point for the result set of a page using a zero-based index

**Usage**

```python
connection.list(
    limit=20,
    offset=0
)
```

### Ordering

To apply multiple sorting criteria to a request.

Name                    | Type                 | Description
------------------------|----------------------|-
ordering                | dict                 | Where the `key` is the field name and the `value` accepts `ASC` for Ascending order or `DESC` for Descending order.

**Usage**

```python
connection.list(
    ordering={'service': 'ASC'}
)
```

### Filtering

To apply multiple, convention oriented filters to a request

Name                    | Type                 | Description
------------------------|----------------------|-
filters                 | dict                 | Where the `key` is the field name and the `value` is the value of the field to filter by.

**Usage**

```python
connection.list(
    filters={'service': 'REV365'}
)
```

### ACClient

ACClient initializes the needed credentials for authentication in ActiveCampaign.

Name                    | Type                 | Description
------------------------|----------------------|-
account                 | str                  | Name of the account
api_token               | str                  | API token from a specific account

**Usage**

```python
from active_campaign import ACClient

client = ACClient(account='rev365', api_token='sampleapitoken')
```

### Contact

ACContacts represent the people that the owner of an ActiveCampaign account is marketing to or selling to.

Name                    | Type                 | Description
------------------------|----------------------|-
client                  | ACClient             | ACClient object

**Methods**

**_create_or_update_**

Creates or updates a contact.

Name                    | Type                 | Description
------------------------|----------------------|-
email                   | str                  | Email address of the contact
first_name              | str (_optional_)     | First name of the contact
last_name               | str (_optional_)     | Last name of the contact
phone                   | str (_optional_)     | Phone number of the contact
org_id                  | int (_optional_)     | Organization the contact belongs to
deleted                 | bool (_optional_)    | True if to delete contact, False otherwise

**_retrieve_**

Retrieves the contact's details.

Name                    | Type                 | Description
------------------------|----------------------|-
id                      | int                  | ID of the contact

**_update_list_status_**

Subscribes/Unsubsribes a contact from a list.

Name                    | Type                 | Description
------------------------|----------------------|-
list                    | int                  | ID of the list to subscribe the contact to
contact                 | int                  | ID of the contact to subscribe to the list
status                  | int                  | Use `ACContact.STATUS_SUBSCRIBE` to subscribe or `ACContact.STATUS_UNSUBSCRIBE` to unsubscribe from a list

**Usage**

```python
from active_campaign import ACClient, ACContact

client = ACClient(account='rev365', api_token='sampleapitoken')
contact = ACContact(client=client)

success, response = contact.create_or_update(
    email='jlorencelim@gmail.com',
    first_name='Lorence',
    last_name='Lim',
)

success, response = contact.retrieve(1)

success, response = contact.update_list_status(
    list=1,
    contact=1,
    status=ACContact.STATUS_SUBSCRIBE, # or use ACContact.STATUS_UNSUBSCRIBE
)
```

### Deep Data Integrations

#### ACConnection

Deep Data connection represent a link between an ActiveCampaign account and an account in some external service. This is intended to be used by third-parties who create integrations between such services and ActiveCampaign.

Name                    | Type                 | Description
------------------------|----------------------|-
client                  | ACClient             | ACClient object

**Methods**

**_create_**

Create a new connection resource.

Name                    | Type                 | Description
------------------------|----------------------|-
service                 | str                  | Name of the service
external_id             | str                  | ID of the account in the external service.
name                    | str                  | Name associated with the account in the external service. Often this will be a company name
logo_url                | str                  | URL to a logo image for the external service
link_url                | str                  | URL to a page where the integration with the external service can be managed in the third-party's website

**_list_**

Lists all existing connection resources.

**Usage**

```python
from active_campaign import ACClient
from active_campaign.ecommerce import ACConnection

client = ACClient(account='rev365', api_token='sampleapitoken')
connection = ACConnection(client=client)

success, response = connection.create(
    service='REV365',
    external_id='sidecommerce',
    name='SIDE-Commerce',
    logo_url='https://www.sidecommerce.com/logo.png',
    link_url='https://www.sidecommerce.com/',
)

success, response = connection.list()
```

#### ACCustomer

E-commerce customer represent a customer in an external e-commerce service. Customer resources primarily hold aggregate e-commerce data associated with a contact.

Name                    | Type                 | Description
------------------------|----------------------|-
client                  | ACClient             | ACClient object
connection_id           | int                  | ID of the connection object for the service where the customer originates.

**Methods**

**_create_**

Create a new e-commerce customer resource.

Name                    | Type                 | Description
------------------------|----------------------|-
external_id             | str                  | ID of the customer in the external service
email                   | str                  | Email address of the customer

**_list_**

Lists all e-commerce customer resources.

**Usage**

```python
from active_campaign import ACClient
from active_campaign.ecommerce import ACConnection, ACCustomer

client = ACClient(account='rev365', api_token='sampleapitoken')
customer = ACCustomer(client=client, connection_id=1)

success, response = customer.create(
    external_id='1',
    email='jlorencelim@gmail.com',
)

success, response = customer.list()
```

#### ACProduct

E-commerce product that is being ordered.

Name                    | Type                 | Description
------------------------|----------------------|-
name                    | str                  | Name of the product
price                   | double               | Price of the product, in cents. Must be greater than or equal to zero.
quantity                | int                  | Quantity ordered
external_id             | str (_optional_)     | ID of the product in the external service
category                | str (_optional_)     | Category of the product
description             | str (_optional_)     | Description for the product
product_url             | str (_optional_)     | URL for the product in the external service
image_url               | str (_optional_)     | URL for the image for the product in the external service

**Usage**

```python
from active_campaign.ecommerce import ACConnection, ACProduct

product = ACProduct(
    name='Shirt',
    price=10,
    quantity=1
)
```

#### ACOrder

E-Commerce order resources represent orders in an external e-commerce service. Before you can create any orders, you must have created a connection resource for the e-commerce service and a customer resource for the customer who placed the order.

Name                    | Type                 | Description
------------------------|----------------------|-
client                  | ACClient             | ACClient object
connection_id           | int                  | ID of the connection object for the service where the customer originates.

**Methods**

**_create_**

Creates a new e-commerce order resource.

Name                    | Type                 | Description
------------------------|----------------------|-
external_id             | str                  | ID of the order in the external service
customer_id             | int                  | ID of the customer associated with this order
email                   | str                  | Email address of the customer who placed the order
products                | ACProduct list       | List of products being ordered
currency                | str                  | Currency of the order (3-digit ISO code, e.g., 'USD')
total_price             | double               | The total price of the order in cents, including tax and shipping charges. Must be greater than or equal to zero.
order_date              | datetime             | Date the order was placed
order_number            | str (_optional_)     | Order number in the external system. This may differ from the external_id.
order_url               | str (_optional_)     | URL for the order in the external service
shipping_method         | str (_optional_)     | Shipping method of the order
source                  | int (_optional_)     | Order source code. Use `ACOrder.SOURCE_SYNC` for sync and `ACOrder.SOURCE_REALTIME_WEBHOOK` for realtime webhook.

**_abandon_cart_**

Creates a new abandoned cart.

Name                    | Type                 | Description
------------------------|----------------------|-
external_checkout_id    | str                  | ID of the order in the external service
customer_id             | int                  | ID of the customer associated with this order
email                   | str                  | Email address of the customer who placed the order
products                | ACProduct list       | List of products being ordered
currency                | str                  | Currency of the order (3-digit ISO code, e.g., 'USD')
total_price             | double               | The total price of the order in cents, including tax and shipping charges. Must be greater than or equal to zero.
abandoned_date          | datetime             | Date the cart was abandoned
external_created_date   | datetime             | Date the abandoned cart was created
order_number            | str (_optional_)     | Order number in the external system. This may differ from the external_id.
order_url               | str (_optional_)     | URL for the order in the external service
external_updated_date   | str (_optional_)     | Date the abandoned cart was updated
shipping_method         | str (_optional_)     | Shipping method of the order
source                  | int (_optional_)     | Order source code. Use `ACOrder.SOURCE_SYNC` for sync and `ACOrder.SOURCE_REALTIME_WEBHOOK` for realtime webhook.

**Usage**

```python
import datetime
from active_campaign.ecommerce import ACConnection, ACProduct, ACOrder

product = ACProduct(
    name='Shirt',
    price=10.00,
    quantity=1
)

client = ACClient(account='rev365', api_token='sampleapitoken')
order = ACOrder(client=client, connection_id=1)

success, response = order.create(
    external_id=1,
    customer_id=1,
    email='jlorencelim@gmail.com',
    products=[products],
    currency='USD',
    total_price=10.00,
    order_date=datetime.datetime.now()
)

success, response = order.abandon_cart(
    external_checkout_id=1,
    customer_id=1,
    email='jlorencelim@gmail.com',
    products=[products],
    currency='USD',
    total_price=10.00,
    abandoned_date=datetime.datetime.now()
    external_created_date=datetime.datetime.now()
)
```
