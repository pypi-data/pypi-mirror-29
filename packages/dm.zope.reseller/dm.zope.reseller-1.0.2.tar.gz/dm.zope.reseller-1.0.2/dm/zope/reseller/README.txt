A package to support resellers.

It maintains in a postgres database information about providers,
products (called articles),
clients, orders and deliveries. It uses a Zope2 frontend
for user interaction.

It assumes a single (implicit) reseller
and several "provider"s and "client"s.

Each provider provides "article"s which the clients can buy.

Clients buy articles in "unit"s; the provider provides them
in "packet"s which contain an integral number of "unit"s. If
the "packet_size" is different from 1, then the reseller repackages
the delivered articles for its clients.

The reseller continously collects "client_order_item"s and
periodically issues "order"s to a provider consisting of
"provider_order_item"s.

The reseller occationally receives a "provider_delivery" for an order
consisting of "provider_delivery_item"s and splits them into
"client_delivery_item"s.

There is a special client, used as stock. It can be used to
balance orders and deliveries. It (and it alone) can have
negative "unit" values in its "client_delivery_items" - indicating
that units have been taken out of the stock.

Usually, we do not delete items. Instead, we mark them as not "active".
This is in order not to break references.



