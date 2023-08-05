README
======

Domain Availability API helps you check whether a domain name is
available for registration quickly and accurately.

To get started you need a developer's account with WhoisXmlApi.com.
Authentication is required each time in order to use the API. The first
500 domain name availability lookups are complimentary when you register
for a free developer account.

The maximum number of requests per second is 30. In case that the limit
is breached, your subsequent requests will be rejected until the next
second.

How do I get set up?
--------------------

-  Install this script with:

   -  pip3 py\_whoisxmlapi --upgrade (or pip py\_whoisxmlapi --upgrade )

-  ready to use it!

How do I use it
---------------

::

    from py_whoisxmlapi import domainAvailability

    usr = "user name"
    pwd = "your Password"

    domain = "google.com"

    d = domainAvailability(usr, pwd)

    data = d.getData(domain)

**Output :**

::

    {"DomainInfo": {
      "domainAvailability": "UNAVAILABLE",
      "domainName": "google.com"
    }}

Thats all!!

Who do I talk to?
-----------------

-  Theodorus van der Sluijs (friends call me Theo)
-  theodorus@vandersluijs.nl

License
-------

Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)

You are free to:
~~~~~~~~~~~~~~~~

-  Share — copy and redistribute the material in any medium or format
-  Adapt — remix, transform, and build upon the material

-The licensor cannot revoke these freedoms as long as you follow the
license terms.-

Under the following terms:
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Attribution — You must give appropriate credit, provide a link to the
   license, and indicate if changes were made. You may do so in any
   reasonable manner, but not in any way that suggests the licensor
   endorses you or your use.
-  NonCommercial — You may not use the material for commercial purposes.
-  ShareAlike — If you remix, transform, or build upon the material, you
   must distribute your contributions under the same license as the
   original.
