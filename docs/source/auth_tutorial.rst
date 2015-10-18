***********************
Authentication Tutorial
***********************

Introduction
============

Mlkshk uses draft 12 of the OAuth2 specification. After we create an instance of the API, we authenticate against mlkshk.com. Thereafter, the API instance is authenticated. In order to access the mlkshk API, you need to create an application.

You should do that http://mlkshk.com/developers/new-api-application. Give your application a title and a description. Make sure to fill in the "Redirect URL" cause we'll use that later.

.. warning::
    The redirect url has to be exactly the same on mlkshk.com and in your code or the server will return a 500 server error when you try to authenticate.

Once you click the big "Create It!" button, you'll be given a "Key" and a "Secret". Write those down. We'll need them later in this tutorial.

Getting Authentication Tokens
=============================

If this is your first run and you don't have access tokens to use the API, you should start a python interpreter and import the ``api`` moduled.::

    from pyshk.api import Api

Next, we will create the API instance and get the access tokens. Here we'll use the consumer key, secret, and redirect URI from above, so have those handy. (Also, your default web browser will open after you enter the second line -- just fair warning.) ::

        a = Api(consumer_key=[Key], consumer_secret=[Secret])
        a.get_auth(redirect_uri=[the redirect url])

If everything went well, your browser opened and asked you to allow access to your account. Allow the app access and you'll be redirected to whatever redirect URL you specified when creating the app.

The URL bar will have something like `http://[redirect_url]?code=[code]`. Copy and paste the `[code]` portion back into the python interpreter and hit enter. You'll then be given the access code and the access secret; you should write those down so you don't have to go through this again.

Starting the API Client
=======================

At this point, the API is authenticated and you can start making calls to the mlkshk server. If you went through this before and you already have an acces code & secret, you can pass those to the API when you instantiate it. Itl'll be something like::

    api = Api(consumer_key='blah',
              consumer_secret='blahsecretblah',
              access_token_key='blah',
              access_token_secret='blahsupersecretblah')

So if everything above worked, you should be able to interact with the API at this point by starting it as above.

Checkout the 'Using the API' documentation for examples.
