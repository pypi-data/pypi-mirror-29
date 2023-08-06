.. _release-notes

Release Notes
=============

v0.28.0
-------

*24 August 2017*

- Features

    + New `timeout` parameter for setting HTTP timeouts, defaults
      to 65 seconds
    + ``StageBasedMessagingApiClient`` and ``MessageSenderApiClient``
      inherit from the base class so that they support retrying requests

v0.25.0
-------

*28 July 2017*

- Features

    + ``IdentityStoreApiClient`` can be given an integer parameter
      ``retries`` when being initialized to indicate the number of
      times an HTTP request should be retried.

v0.17.0
-------
.. Pull request #24

*24 March 2017*

 - Fixes
    - Remove stray print command in identity store tests
 - Features
    - Add create inbound function for message store client
    - Add list inbound function for message store client

v0.18.0
-------

*4 April 2017*

- Features
    - Add create subscription function for stage based messaging client
