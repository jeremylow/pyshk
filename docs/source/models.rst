.. _models:

******
Models
******

.. _models_user:

User
====

.. class:: User([id=None], [name=None], [profile_image_url=None], [about=None], [website=None], [shakes=None])

    Represents a User on mlkshk and has the properties listed below. User information cannot be changed via the API as there is no endpoint for this functionality.

    :param id: (int) ID of the user for mlkshk; unable to be changed via mlkshk.com or the API.
    :param name: (str): Username; unable to be changed via mlkshk.com or the API.
    :param profile_image_url: (str): Profile picture of the user. User can change this on the website.
    :param about: (str): Short description of the user.
    :param website: (str): User's website (i.e., not the user's page on mlshk.com).
    :param shakes: (list): List of :ref:`models_shake` objects.

    .. _models_user_methods:

    .. method:: NewFromJson([data=None])

        Create a User object from a JSON string. Returns a User object.

    .. method:: AsDict([dt=True])

        :param dt: (bool) Return dates as ``datetime`` objects; false to return as ISO strings.
            Return the User object as a dictionary of values. NB: Dates will be returned as native, UTC-timezone (but not timezone aware) ``datetime.datetime`` objects.

    .. method:: AsJsonString()

        Return the User object as JSON string. NB: any dates will be converted to ISO strings as part of the serialization.


.. _models_shake:

Shake
=====

.. class:: Shake([id=None], [name=None], [owner=None], [url=None], [thumbnail_url=None], [description=None], [type=None], [created_at=None], [updated_at=None])

    Object representing a Shake on mlkshk.com

    :param id: (id): ID of the Shake
    :param name: (str): Shake's name
    :param owner: (User): User object representing the owner of the Shake
    :param url: (str): URL of the Shake (i.e., mlkshk.com/commute)
    :param thumbnail_url: (str): "Avatar" for the Shake
    :param description: (str): Description of the Shake
    :param type: (str): 'user' or 'group' denoting whether the Shake is has no contributors other than the owner (``user`` shake) or many (``group`` shake).
    :param created_at: (datetime): ``datetime.datetime`` representing the creation date & time of the Shake.
    :param updated_at: (datetime): Last modified ``datetime.datetime`` of the Shake.


    .. method:: NewFromJson([data=None])

        Return a Shake object from a JSON string.

    .. method:: AsDict([dt=True])

        :param dt: (bool) Return dates as ``datetime`` objects; false to return as ISO strings.
            Return the User object as a dictionary of values. NB: Dates will be returned as native, UTC-timezone (but not timezone aware) ``datetime.datetime`` objects.

    .. method:: AsJsonString()

        Return a JSON string representing this Shake instance. NB: any dates will be converted to ISO strings as part of the serialization.

.. _models_sharedfile:

SharedFile
==========

.. class:: SharedFile([sharekey=None], [name=None], [user=None], [title=None], [description=None], [posted_at=None], [permalink=None], [width=None], [height=None], [views=None], [likes=None], [saves=None], [comments=None], [nsfw=None], [image_url=None], [source_url=None], [saved=None], [liked=None])

    Object representing a file or embedded video on mlkshk.com

    :param sharekey: (str): Sharekey of the file.
    :param name: (str): Filename as uploaded to mlkshk.com
    :param user: (User): User object representing user who uploaded the file
    :param title: (str): Title of the SharedFile
    :param description: (str): Description of the SharedFile
    :param posted_at: (datetime): ``datetime.datetime`` object representing the time the SharedFile was uploaded
    :param permalink: (str): URL of the SharedFile. Example: "http://mlkshk.com/1645C"
    :param width: (int): Width of the image.
    :param height: (int): Height of the image
    :param views: (int): How many views the SharedFile has received.
    :param likes: (int): How many likes/favorites the SharedFile has received.
    :param saves: (int): How many saves the SharedFile has received.
    :param comments: (list): List of Comment objects posted to the SharedFile.
    :param nsfw: (bool): Whether the file is not safe for work (NB: folks in the community sometimes flag very large GIFs as NSFW).
    :param image_url: (str): URL for hotlinking to the image file.
    :param source_url: (str): If not an image, this can be a YouTube, Vine, etc. link.
    :param saved: (bool): If the currently authenticated user has saved the file.
    :param liked: (bool): If the currently authenticated user has liked the file.


    .. method:: NewFromJson([data=None])

        Return a SharedFile object from a JSON string.

    .. method:: AsDict([dt=True])

        :param dt: (bool) Return dates as ``datetime`` objects; false to return as ISO strings.
            Return the User object as a dictionary of values. NB: Dates will be returned as native, UTC-timezone (but not timezone aware) ``datetime.datetime`` objects.

        Return a dictionary representing the SharedFile object.

    .. method:: AsJsonString()

        Return a JSON string representing this SharedFile instance. NB: any dates will be converted to ISO strings as part of the serialization.
