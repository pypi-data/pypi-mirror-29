====================
LogUp SDK for Python
====================

The LogUp SDK for Python enables Python developers to easily integrate LogUp service in their projects.

Getting Started
---------------

Sign up for LogUp
:::::::::::::::::

Before you begin, you need a LogUp account. Please see the `Getting started <https://docs.logup.co/getting_started.html>`_
section of the developer guide for information about how to create a LogUp account and create your first `gate
<https://docs.logup.co/gate.html>`_.

Install the SDK
:::::::::::::::

Install the SDK library using `pip <https://pypi.python.org/pypi/pip>`_

.. code-block:: bash
    pip install logup

Initialize the LogUp Client Object
::::::::::::::::::::::::::::::::::

.. code-block:: python

    id_gate = "{your-id-gate}"
    gate_secret_key = "{your-gate-secret-key}"
    # Create an instance of LogupClient using the default API Version
    logup_client = LogupClient(
        id_gate,
        gate_secret_key
    )

    # Create an instance of LogupClient specifying the API version

    api_version = "v1_1"
    logup_client_1 = LogupClient(
        id_gate,
        gate_secret_key,
        api_version
    )

Now you're ready to verify the token received. On the redirect page where the user is sent to after the LogUp, get from
the URL those parameters:

- **logupToken** : the unique token to verify user identity

- **isNewUser** : true if the user is new for your website, false if the user said he has already an account on your
website. `More about this parameter <https://docs.logup.co/access.html#response-parameters>`_

Verify user identity
::::::::::::::::::::

This code is how you can verify that the **token received** is correct and see **who the user is**.

.. code-block:: python

    logup_token = "{very-long-token-received-as-URL-query-parameter}"
    is_new_user = True or False

    if logup_client.is_logup_verified(logup_token, is_new_user):
        # user was successfully logged in!
        # get the subscription object
        subscription = logup_client.subscription
    else:
        print("Ops, the user did not log in")

Subscription
------------

With the subscription object you can get more information about the actor who logged in, as well as access to its saved
DB. A DB is a key-value store of parameters you can associated to your user. `Read mode about DB <https://docs.logup.co/subscription.html>`_.

Read the values
:::::::::::::::

This is how a Subscription object is made:

.. code-block:: python

    subscription.id_subscription # the id of the subscription
    subscription.id_actor # the id of the actor that access the subscription
    subscription.is_new_user # true if it is a new user, false otherwise

For difference explanation between id actor and id subscription `see our documentation <https://docs.logup.co/access.html#subscription-and-actor-difference>`_.

Get subscription DB values
::::::::::::::::::::::::::

To read DB values of that subscription.

.. code-block:: python

    db = subscription.db
    print("idSubscription retrieved: " + subscription.id_subscription)
    print("With this DB associated: ")
    print(db)

Add / Update DB values
::::::::::::::::::::::

Add or update a DB value.

.. code-block:: python

    data = {
        "key-test": "",
        "second-key-test": 1,
        "third-key-test": True
    }
    db = subscription.update_db(data)
    print("Db values updated: ")
    print(db)

Some **limitations** may apply to the values you want to add to a DB: read them in our
`documentation <https://docs.logup.co/subscription.html>`_.
When you update or add values, you do not need to give all the previous values, but **just those you need to update / add**.
The db in response will have all the values currently stored in the DB.


Delete DB values
::::::::::::::::

.. code-block:: python

    keys = ["third-key-test"]
    db = subscription.delete_db_value(keys)
    print("New db values: ")
    print(db)

Enter an array with one or more strings representing the **keys you want to remove** from the DB. The **response** will have
the **current db** without the removed values.

Operate on custom object
::::::::::::::::::::::::

If you want to operate on a subscription that is not the one retrieved during login, you need to create a new
Subscription object with **the subscription id you are looking for.** This is an example:

.. code-block:: python

    id_subscription = "sub_XXXXXXXXXXX"
    subscription = logup_client.subscription_custom(id_subscription)
    # on subscription now you can perform all the operation mentioned above

Remember that if you create a custom new subscription, *you won't have the values of*
- idActor
- isNewUser

Since they are related to the user trying to access your website, and not to a generic loaded subscription.
