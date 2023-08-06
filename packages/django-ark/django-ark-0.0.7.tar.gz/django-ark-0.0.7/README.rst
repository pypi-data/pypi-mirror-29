=====
Ark
=====

Django-Ark is a complete integration of Ark Ecosystem with Django. It allows you to use the Django ORM to query the blockchain,
has a transaction protocol which stores transactions locally and opens a graphql api endpoint for querying.

Detailed documentation is in the "docs" directory.

Quick start
-----------
pip install requirements.txt

arky requires the dependencies::

    sudo apt-get install python3-dev libusb-1.0-0-dev libudev-dev


Create a .env file in your project directory (where manage.py is located) and enter these variables:

    ARK_DB_PASSWORD=
    ARK_DB_USER=
    ARK_DB_HOST=
    ARK_DB_PORT=
    DB_NAME=
    SECRET_KEY=
    DEBUG=

1. Add "ark" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'ark',
    ]

2. Set the name of the Ark db::

    # used by the django-ark db router
    ARK_DB_NAME = 'ark_mainnet'

3. Add ark.router.ArkRouter to your DB routers (conversely you can also use .using('ark_mainnet') in every ORM query)::

    DATABASE_ROUTERS = [
        .....................
        'ark.router.ArkRouter',
        .....................
        ]

4. Include the ark URLconf in your project urls.py like this::

    from graphene_django.views import GraphQLView
    from schema import schema

    urlpatterns = [
        url(r'^admin/', admin.site.urls),
        url(r'^graphql', GraphQLView.as_view(graphiql=True, schema=schema)),
    ]

5. Run `python manage.py migrate` to create the ark models.


6. Visit http://127.0.0.1:8000/graphql/ to query the db using relay.


Django-ark also has a transaction protocol for queueing transactions, and rebroadcasting if failed::

    from ark.transactions import TX, TxBroadcaster

    tx = TX(
        network='dark',
        recipient='DRvZ1a7bX35EjyHhvtgprjegjdBT63Mq4X',
        amount='100000000',
        secret='talk coral spatial wall pipe wolf orient attack soft favorite ordinary buzz',
        smartbridge='sometokentobeused',
        desc='your own administration',
        broadcaster=0
        )

    tx.queue()

    dark_caster = TxBroadcaster(
        broadcaster=0,
        max_retry=10,
        check_until_confs=51,
        use_open_peers=True,
        wait_time=30
        )

    dark_caster.run()

The broadcaster will keep checking the queued transactions, and rebroadcasting until it is confirmed. It then continues
to check the tx until it has reached check_until_confs confirmations (incase of a fork, this will ensure it gets truly
added in the blockchain)

You can create a background process to keep a broadcaster (or multiple) running for each network.
TX are stored as unique transactions in the DB, so even if multiple broadcasters pick it up, there is no risk of double
spending. Broadcasters make use of an atomic DB lock, so only one instance of a broadcaster is ever running per uid.