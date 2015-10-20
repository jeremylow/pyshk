.. _models:

******
Models
******

.. _models_user:

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

	.. method:: AsDict()

		Return the User object as a dictionary of values. NB: Dates will be returned as native, UTC-timezone (but not timezone aware) ``datetime.datetime`` objects.

	.. method:: AsJsonString()

		Return the User object as JSON string. NB: any dates will be converted to ISO strings as part of the serialization.


.. _models_shake:

.. class:: Shake([id=None], [name=None], [owner=None], [url=None], [thumbnail_url=None], [description=None], [type=None], [created_at=None], [updated_at=None])

	Object representing a Shake on mlkshk.com

    :param id: (id): ID of the Shake
    :param name: (str): Shake's name
    :param owner: (User): User object representing the owner of the Shake
    :param url: (str): URL of the Shake (i.e., mlkshk.com/commute)
    :param thumbnail_url: (str): "Avatar" for the Shake
    :param description: (str): Description of the Shake
    :param type: (str): ``user`` or ``group`` denoting whether the Shake is has no contributors other than the owner (``user`` shake) or many (``group`` shake).
    :param created_at: (datetime): ``datetime.datetime`` representing the creation date & time of the Shake.
    :param updated_at: (datetime): Last modified ``datetime.datetime`` of the Shake.

