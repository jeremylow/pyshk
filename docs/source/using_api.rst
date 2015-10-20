.. _usage:

********************
Using the API Client
********************

Introduction
============

If you haven't, please go through the Authentication Tutorial. You'll need an authenticated API client for the next section.

Examples
========

Let's start by creating an API client to use: ::

    >>> from pyshk.api import Api

    >>> client = Api(
    ...    consumer_key='key',
    ...    consumer_secret='secret',
    ...    access_token_key='key',
    ...    access_token_secret='supersecret')

Users
+++++

To get a User object for the currently authenticated user, we can call ``client.get_user()`` ::

    >>> user = client.get_user()

This will return a User instance containing the user's Shakes and some information about the user: The User object has the following properties: ::

* about
* id
* name
* profile_image_url
* shakes
* website

Unfortunately, you cannot post to this resource, so those properties are unable to be changed. But, we can play around with the user's Shakes, so let's do that.

Shakes
++++++

The ``user.shakes`` property from above is a list of Shake objects. If the user has a pro account, they can have more than one Shake; if not, the only Shake will be their User Shake. To get the user's Shakes directly, there's another method, which will return a list of Shakes: ::

    >>> shakes = client.get_user_shakes()

Getting the first Shake in that list, we can print some info about it: ::

    >>> shake = shakes[0]
    >>> shake.id
    68435

    >>> print(shake.created_at)
    2015-04-27 17:22:54

    # The time fields are actually stored as python datetime objects:

    >>> shake.created_at
    datetime.datetime(2015, 4, 27, 17, 22, 54)

    # The Shake object contains a User object as well stored as 'owner':

    >>> shake.owner.id
    67136
    >>> shake.owner.name
    'jcbl'


Uploading Files
+++++++++++++++

Now that we have a Shake object, we can start posting files to it. The client method for this is ``client.post_shared_file()`` ::

    >>> uploaded_file = client.post_shared_file(
            image_file='scully.gif',
            title='scully.gif',
            description="this is an excellent gif")

What we'll get back is the name of the ShareFile and the sharekey. ::

    {'name': 'scully.gif', 'share_key': '1645C'}

.. warning::
    While most methods return an object, this one doesn't -- it just returns some info.

From there, we can get some info on the uploaded file and maybe post a comment or two.

SharedFiles
+++++++++++

SharedFiles on mlkshk have a bunch of properties; we won't go into detail, but you can check out the modules page to see what's up. So now that we have the sharekey from above, we can get some more info on our awesome gif. ::

    >>> awesome_gif = client.get_shared_file(sharekey='1645C')

    # Let's see how many people liked this GIF:
    >>> awesome_gif.likes
    1

    # This is a crime, but moving on, let's just see what all awesome_gif contains:
    >>> vars(awesome_gif)
    {'_posted_at': datetime.datetime(2015, 10, 9, 20, 34, 34),
     'comments': 0,
     'description': None,
     'height': 180,
     'image_url': None,
     'liked': False,
     'likes': 1,
     'name': 'tumblr_mo6ur4bPUm1rxfs8ro5_250.gif',
     'nsfw': False,
     'permalink': None,
     'saved': False,
     'saves': 0,
     'sharekey': '1645C',
     'source_url': None,
     'title': 'scully.gif',
     'user': {
        "id": 67136,
        "mlkshk_url": "https://mlkshk.com/user/jcbl",
        "name": "jcbl",
        "profile_image_url": "[...]",
        "shake_count": 0},
     'views': 0,
     'width': 245}

.. warning::

    A couple of things to note before moving on: ``awesome_gif.views`` is wrong. At the time of this writing, it's off by 142 views. Everything else about the SharedFile seems to be correct, except that now ``user.shake_count`` is ``0``. This is a function of the fact that the endpoint (``/api/sharedfile/:id``) returns information about the user, but it doesn't return information about the user's shakes.

Comments, Saves, & Likes
++++++++++++++++++++++++

TKTK