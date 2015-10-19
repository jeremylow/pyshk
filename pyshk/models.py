import json
import datetime


def convert_time(dt):
    """
    2015-10-09T15:58:11Z -> datetime.datetime(2015, 10, 9, 15, 58, 11)
    """
    try:
        return datetime.datetime.strptime(dt, "%Y-%m-%dT%H:%M:%SZ")
    except:
        return None


class User(object):

    """
    A class representing a MLKSHK user.

    Exposes the following properties of a user:
        user.id
        user.name
        user.profile_image_url
        user.about
        user.website
        user.shakes
    """

    def __init__(self, **kwargs):
        param_defaults = {
            'id': None,
            'name': None,
            'profile_image_url': None,
            'about': None,
            'website': None,
            'shakes': None}
        for (param, default) in param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    @property
    def mlkshk_url(self):
        return "https://mlkshk.com/user/{0}".format(self.name)

    @property
    def shake_count(self):
        if self.shakes:
            return len(self.shakes)
        else:
            return 0

    def AsDict(self, dt=True):
        """
        A dict representation of this User instance.

        The return value uses the same key names as the JSON representation.

        Args:
            dt (bool): If True, return dates as python datetime objects. If
            False, return dates as ISO strings.

        Return:
            A dict representing this User instance
        """
        data = {}
        if self.name:
            data['name'] = self.name
            data['mlkshk_url'] = self.mlkshk_url
        if self.profile_image_url:
            data['profile_image_url'] = self.profile_image_url
        if self.id:
            data['id'] = self.id
        if self.about:
            data['about'] = self.about
        if self.website:
            data['website'] = self.website
        if self.shakes:
            data['shakes'] = [shk.AsDict(dt=dt) for shk in self.shakes]
        data['shake_count'] = self.shake_count
        return data

    def AsJsonString(self):
        """A JSON string representation of this User instance.

        Returns:
          A JSON string representation of this User instance
        """
        return json.dumps(self.AsDict(dt=False), sort_keys=True)

    @staticmethod
    def NewFromJSON(data):
        """
        Create a new User instance from a JSON dict.

        Args:
            data (dict): JSON dictionary representing a user.

        Returns:
            A User instance.
        """
        if data.get('shakes', None):
            shakes = [Shake.NewFromJSON(shk) for shk in data.get('shakes')]
        else:
            shakes = None

        return User(
            id=data.get('id', None),
            name=data.get('name', None),
            profile_image_url=data.get('profile_image_url', None),
            about=data.get('about', None),
            website=data.get('website', None),
            shakes=shakes)

    def __eq__(self, other):
        """
        Compare two user objects against one another.

        Args:
            other (User): another User object against which to compare the
                current user.
        """
        try:
            return other and \
                self.id == other.id and \
                self.name == other.name and \
                self.profile_image_url == other.profile_image_url and \
                self.about == other.about and \
                self.website == other.website and \
                self.shakes == other.shakes
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        """ String representation of this User instance. """
        return self.AsJsonString()


class Comment(object):

    """
    A class representing a Comment on mlkshk.

    Exposes the following properties of a Comment:
        comment.body
        comment.posted_at
        comment.user
    """

    def __init__(self, **kwargs):
        param_defaults = {
            'body': None,
            'posted_at': None,
            'user': None}
        for (param, default) in param_defaults.items():
            setattr(self, param, kwargs.get(param, default))

    def AsDict(self, dt=True):
        """
        A dict representation of this Comment instance.

        The return value uses the same key names as the JSON representation.

        Args:
            dt (bool): If True, return dates as python datetime objects. If
            False, return dates as ISO strings.

        Return:
          A dict representing this Comment instance
        """
        data = {}

        if self.body:
            data['body'] = self.body
        if self.posted_at:
            data['posted_at'] = self.posted_at
        if self.user:
            data['user'] = self.user.AsDict()

        return data

    def AsJsonString(self):
        """
        A JSON string representation of this Comment instance.

        Returns:
          A JSON string representation of this Comment instance
       """
        return json.dumps(self.AsDict(dt=False), sort_keys=True)

    @staticmethod
    def NewFromJSON(data):
        """
        Create a new Comment instance from a JSON dict.

        Args:
            data (dict): JSON dictionary representing a Comment.

        Returns:
            A Comment instance.
        """
        return Comment(
            body=data.get('body', None),
            posted_at=data.get('posted_at', None),
            user=User.NewFromJSON(data.get('user', None))
        )

    def __eq__(self, other):
        try:
            return other and \
                self.body == other.body and \
                self.posted_at == other.posted_at and \
                self.user == other.user
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        """ String representation of this Comment instance. """
        return self.AsJsonString()


class Shake(object):

    """
    A class representing a Shake on mlkshk.

    Exposes the following properties of a Shake:
        shake.id
        shake.name
        shake.owner
        shake.url
        shake.thumbnail_url
        shake.description
        shake.type
        shake.created_at
        shake.updated_at
    """

    def __init__(self, **kwargs):
        param_defaults = {
            'id': None,
            'name': None,
            'owner': None,
            'url': None,
            'thumbnail_url': None,
            'description': None,
            'type': None,
            'created_at': None,
            'updated_at': None}
        for (param, default) in param_defaults.items():
            setattr(self, param, kwargs.get(param, default))
        self.created_at = kwargs.get('created_at', None)
        self.updated_at = kwargs.get('updated_at', None)

    @property
    def created_at(self):
        return self._created_at

    @created_at.setter
    def created_at(self, value):
        self._created_at = convert_time(value)

    @property
    def created_at_iso(self):
        return self._created_at.isoformat()

    @property
    def updated_at(self):
        return self._updated_at

    @updated_at.setter
    def updated_at(self, value):
        self._updated_at = convert_time(value)

    @property
    def updated_at_iso(self):
        return self._updated_at.isoformat()

    def AsDict(self, dt=True):
        """
        A dict representation of this Shake instance.

        The return value uses the same key names as the JSON representation.

        Return:
            A dict representing this Shake instance
        """
        data = {}

        if self.id:
            data['id'] = self.id
        if self.name:
            data['name'] = self.name
        if self.owner:
            data['owner'] = self.owner.AsDict()
        if self.url:
            data['url'] = self.url
        if self.thumbnail_url:
            data['thumbnail_url'] = self.thumbnail_url
        if self.description:
            data['description'] = self.description
        if self.type:
            data['type'] = self.type

        if dt:
            if self.created_at:
                data['created_at'] = self.created_at
            if self.updated_at:
                data['updated_at'] = self.updated_at
        else:
            if self.created_at:
                data['created_at'] = self.created_at_iso
            if self.updated_at:
                data['updated_at'] = self.updated_at_iso

        return data

    def AsJsonString(self):
        """
        A JSON string representation of this Shake instance.

        Returns:
          A JSON string representation of this Shake instance
       """
        return json.dumps(self.AsDict(dt=False), sort_keys=True)

    @staticmethod
    def NewFromJSON(data):
        """
        Create a new Shake instance from a JSON dict.

        Args:
            data (dict): JSON dictionary representing a Shake.

        Returns:
            A Shake instance.
        """
        s = Shake(
            id=data.get('id', None),
            name=data.get('name', None),
            url=data.get('url', None),
            thumbnail_url=data.get('thumbnail_url', None),
            description=data.get('description', None),
            type=data.get('type', None),
            created_at=data.get('created_at', None),
            updated_at=data.get('updated_at', None)
        )
        if data.get('owner', None):
            s.owner = User.NewFromJSON(data.get('owner', None))
        return s

    def __eq__(self, other):
        try:
            return other and \
                self.id == other.id and \
                self.name == other.name and \
                self.owner == other.owner and \
                self.url == other.url and \
                self.thumbnail_url == other.thumbnail_url and \
                self.description == other.description and \
                self.type == other.type and \
                self.created_at == other.created_at and \
                self.updated_at == other.updated_at
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        """ String representation of this Shake instance. """
        return self.AsJsonString()


class SharedFile(object):

    """
    A class representing a file shared on MLKSHK.

    Exposes the following properties of a sharedfile:
        sharedfile.sharekey
        sharedfile.name
        sharedfile.user
        sharedfile.title
        sharedfile.description
        sharedfile.posted_at
        sharedfile.permalink
        sharedfile.width
        sharedfile.height
        sharedfile.views
        sharedfile.likes
        sharedfile.saves
        sharedfile.comments
        sharedfile.nsfw
        sharedfile.image_url
        sharedfile.source_url
        sharedfile.saved
        sharedfile.liked

    Args:
        sharedfile.sharekey
        sharedfile.name
        sharedfile.user
        sharedfile.title
        sharedfile.description
        sharedfile.posted_at
        sharedfile.permalink
        sharedfile.width
        sharedfile.height
        sharedfile.views
        sharedfile.likes
        sharedfile.saves
        sharedfile.comments
        sharedfile.nsfw
        sharedfile.image_url
        sharedfile.source_url
        sharedfile.saved
        sharedfile.liked
    """

    def __init__(self, *args, **kwargs):
        param_defaults = {
            'sharekey': None,
            'name': None,
            'user': None,
            'title': None,
            'description': None,
            'posted_at': None,
            'permalink': None,
            'width': None,
            'height': None,
            'views': None,
            'likes': None,
            'saves': None,
            'comments': None,
            'nsfw': None,
            'image_url': None,
            'source_url': None,
            'saved': None,
            'liked': None,
        }
        for (param, default) in param_defaults.items():
            setattr(self, param, kwargs.get(param, default))
        self.posted_at = kwargs.get('posted_at', None)

    @property
    def posted_at(self):
        return self._posted_at

    @posted_at.setter
    def posted_at(self, value):
        self._posted_at = convert_time(value)

    @property
    def posted_at_iso(self):
        return self._posted_at.isoformat()

    def AsDict(self, dt=True):
        """
        A dict representation of this Shake instance.

        The return value uses the same key names as the JSON representation.

        Args:
            dt (bool): If True, return dates as python datetime objects. If
                False, return dates as ISO strings.

        Return:
          A dict representing this Shake instance
        """
        data = {}

        if self.sharekey:
            data['sharekey'] = self.sharekey
        if self.name:
            data['name'] = self.name
        if self.user:
            data['user'] = self.user.AsDict()
        if self.title:
            data['title'] = self.title
        if self.description:
            data['description'] = self.description
        if self.posted_at:
            if dt:
                data['posted_at'] = self.posted_at
            else:
                data['posted_at'] = self.posted_at_iso
        if self.permalink:
            data['permalink'] = self.permalink
        if self.width:
            data['width'] = self.width
        if self.height:
            data['height'] = self.height
        if self.image_url:
            data['image_url'] = self.image_url
        if self.source_url:
            data['source_url'] = self.source_url
        data['views'] = self.views
        data['likes'] = self.likes
        data['saves'] = self.saves
        data['comments'] = self.comments
        data['nsfw'] = self.nsfw
        data['saved'] = self.saved
        data['liked'] = self.liked

        return data

    def AsJsonString(self):
        """
        A JSON string representation of this SharedFile instance.

        Returns:
            A JSON string representation of this SharedFile instance
        """
        return json.dumps(self.AsDict(dt=False), sort_keys=True)

    @staticmethod
    def NewFromJSON(data):
        """
        Create a new SharedFile instance from a JSON dict.

        Args:
            data (dict): JSON dictionary representing a SharedFile.

        Returns:
            A SharedFile instance.
        """
        return SharedFile(
            sharekey=data.get('sharekey', None),
            name=data.get('name', None),
            user=User.NewFromJSON(data.get('user', None)),
            title=data.get('title', None),
            description=data.get('description', None),
            posted_at=data.get('posted_at', None),
            permalink=data.get('permalink', None),
            width=data.get('width', None),
            height=data.get('height', None),
            views=data.get('views', 0),
            likes=data.get('likes', 0),
            saves=data.get('saves', 0),
            comments=data.get('comments', None),
            nsfw=data.get('nsfw', False),
            image_url=data.get('image_url', None),
            source_url=data.get('source_url', None),
            saved=data.get('saved', False),
            liked=data.get('liked', False),
        )

    def __eq__(self, other):
        """
        Compare two SharedFiles on all attributes **except** saved status
        and liked status.
        """
        try:
            return other and \
                self.sharekey == other.sharekey and \
                self.name == other.name and \
                self.user == other.user and \
                self.title == other.title and \
                self.description == other.description and \
                self.posted_at == other.posted_at and \
                self.permalink == other.permalink and \
                self.width == other.width and \
                self.height == other.height and \
                self.views == other.views and \
                self.likes == other.likes and \
                self.saves == other.saves and \
                self.comments == other.comments and \
                self.nsfw == other.nsfw and \
                self.image_url == other.image_url and \
                self.source_url == other.source_url
        except AttributeError:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return self.AsJsonString()
