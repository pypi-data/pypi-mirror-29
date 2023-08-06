==============
rer.newsletter
==============

.. image:: https://travis-ci.org/PloneGov-IT/rer.newsletter.svg?branch=master
    :target: https://travis-ci.org/PloneGov-IT/rer.newsletter

This product allows the complete management of a newsletter.

========
Features
========

New Content-type
----------------

- Channel

  * Totally customizable because it is possible to set a header, a footer and CSS styles. This fields allows to uniform template of email that will be sent from one channel.
  * content type that inherit from folder content.

- Message

  * content type that inherit from folder content.

Portlet and Tile
----------------

The product provide a portlet and a tile for user subscribe.

Form for user subscribe have two fields: email and reCaptcha, so do not forget to
set key for reCaptcha fields. See `plone.formwidget.recaptcha <https://github.com/plone/plone.formwidget.recaptcha>`_ for more details.

User Manage
-----------

Allows complete management of user.

- Add user from admin setting
- Delete user from admin setting
- Import users directly from CSV file
- Export users directly to CSV file
- Delete a group of user directly from CSV file
- Subscribe users
- Unsubscribe users


=================
Advanced Features
=================


Utility for email sending
-------------------------

This product normaly send email through plone mailer, but creating a product which
implements the utility ``IChannelUtility`` it is possible use another system of
mailing-list, like for example mailman.

At the inside of ``IChannel Utility`` interface are described all methods that will be
implemented and the way that they must responded.

Utility declaration::

    <utility
      provides=".channel.IChannelUtility"
      factory=".base.BaseHandler" />

and creates a class that implement utility interface::

    @implementer(IChannelUtility)
    class BaseHandler(object):
        """ utility class to send channel email with mailer of plone """


Advanced security
-----------------

New permissions have been added for the management of the Newsletter:

- ``rer.newsletter: Add Channel``
- ``rer.newsletter: Add Message``
- ``rer.newsletter: Manage Newsletter``
- ``rer.newsletter: Send Newsletter``

This permission are assigned to Manager and Site Administrator. Besides it been
added a new role ``Gestore Newsletter`` which have permissions for all possible
operations on newsletter.


Asynchronous sending of email
-----------------------------

rer.newsletter supports asyncronous sendout using collective.taskqueue,
that it is already installed like a dependency of product.

For support this asyncronous sendout you must add to section instance-settings of your
buildout this configuration::

    zope-conf-additional =
       %import collective.taskqueue
       <taskqueue>
         queue rer.newsletter.queue
       </taskqueue>
       <taskqueue-server>
         queue rer.newsletter.queue
       </taskqueue-server>

This code adds a queue to which various email submissions are added.
See `collective.taskqueue <https://github.com/collective/collective.taskqueue>`_ for more details.


Cron job
--------

rer.newsletter have a view that can called from a cron job. This view delete all
users that not have confirmed subscription to a channel in time.

Inside the settings of the product there is a field that allows you to set
validity time of the channel subscription token.

View is::

    .../@@delete_expired_users

============
Installation
============

Install rer.newsletter by adding it to your buildout::

    [buildout]

    ...

    eggs =
        rer.newsletter


and then running ``bin/buildout``

============
Dependencies
============

This product has been tested on Plone 5.1

=======
Credits
=======

Developed with the support of `Regione Emilia Romagna <http://www.regione.emilia-romagna.it/>`_;

Regione Emilia Romagna supports the `PloneGov initiative <http://www.plonegov.it/>`_.


=======
Authors
=======

This product was developed by RedTurtle Technology team.

.. image:: http://www.redturtle.it/redturtle_banner.png
   :alt: RedTurtle Technology Site
   :target: http://www.redturtle.it/
