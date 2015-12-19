*****
pyshk
*****


Pyshk is a python client for the mlkshk.com api.

Documentation is available at `<http://pyshk.readthedocs.org/en/latest/>`_

Installation
############

Install with ::

   pip install pyshk

In order to get started, you have to sign up for mlkshk (yay!) and create an application on mlkshk.com. First, you'll need to sign up for an account here: `<http://mlkshk.com/create-account>`_.

Then, create we'll create an application so that you can use the API. You should do that at `<http://mlkshk.com/developers/new-api-application>`_. Give your application a title and a description. Make sure to fill in the "Redirect URL" cause we'll use that later. The redirect url has to be exactly the same on mlkshk.com and in your code or the server will return a 500 server error when you try to authenticate.

Once you click the big "Create It!" button, you'll be given a "Key" and a "Secret". Write those down. We'll need them later.

Usage
#####

Start a python interpreter and then import the API::

    from pyshk.api import Api

If you don't have an access token (you won't if this is the first run), start up the API using the Key and Secret from above::

    a = Api(consumer_key=[Key], consumer_secret=[Secret])
    a.get_auth(redirect_uri=[the redirect url from above])

At this point, your web browser will open and you'll be prompted to allow your application (whatever you named it) to access your account. Allow the app access and you'll be redirected to whatever redirect URL you specified when creating the app. The URL bar will have something like ``http://[redirect_url]?code=[code]``. Copy and paste the ``[code]`` portion back into the python interpreter and hit enter. You'll then be given the access code and the access secret; you should write those down so you don't have to go through this again.

At this point, the API is authenticated and you can start making calls to the mlkshk server. If you went through this before and you already have an acces code & secret, you can pass those to the API when you instantiate it. Itl'll be something like::

	api = Api(consumer_key='blah',
			  consumer_secret='blahsecretblah',
			  access_token_key='blah',
			  access_token_secret='blahsupersecretblah')

API Coverage & Working resources::
##################################

* ``GET /api/favorites``
* ``GET /api/favorites/after/(afterkey)``
* ``GET /api/favorites/before/(beforekey)``

--------------------

* ``GET /api/friends``
* ``GET /api/friends/after/(afterkey)``
* ``GET /api/friends/before/(beforekey)``

--------------------

* ``GET /api/incoming``
* ``GET /api/incoming/(id)/after/(afterkey)``
* ``GET /api/incoming/(id)/before/(beforekey)``

--------------------

* ``GET /api/magicfiles``
* ``GET /api/magicfiles/(id)/after/(afterkey)``
* ``GET /api/magicfiles/(id)/before/(beforekey)``

--------------------

* ``GET /api/shakes``
* ``GET /api/shakes/(id)``
* ``GET /api/shakes/(id)/after/(afterkey)``
* ``GET /api/shakes/(id)/before/(beforekey)``

--------------------

* ``GET /api/sharedfile/(sharekey)``
* ``POST /api/sharedfile/(sharekey)``
* ``GET /api/sharedfile/(sharekey)/comments``
* ``POST /api/sharedfile/(sharekey)/comments``
* ``POST /api/sharedfile/(sharekey)/like``
* ``POST /api/sharedfile/(sharekey)/save``

--------------------

* ``GET /api/user``
* ``GET /api/user_id/(user_id)``
* ``GET /api/user_name/(username)``

--------------------

* ``POST /api/upload``

Notes
#####

* ``POST /api/upload`` returns a 200 response, not 201 as stated in mlkshk docs.
* ``GET /api/user_id/[x]`` & ``GET /api/user_name[x]`` for user x who does not exist raises a 500 Server Error, not 404 as in the API docs.
