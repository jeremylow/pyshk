[![Build Status](https://travis-ci.org/jeremylow/pyshk.svg?branch=master)](https://travis-ci.org/jeremylow/pyshk)

Pyshk is a python client for the mlkshk.com api.

### Installation
For now, clone the repository:

    git clone git@github.com:jeremylow/pyshk.git

and then create a virtual environment. Install the requirements with:

    pip install -r requirements.txt

In order to get started, you have to sign up for mlkshk (yay!) and create an application on mlkshk.com. First, you'll need to sign up for an account here: [Create Account](http://mlkshk.com/create-account).

Then, create we'll create an application so that you can use the API. You should do that [here](http://mlkshk.com/developers). Give your application a title and a description. Make sure to fill in the "Redirect URL" cause we'll use that later. The redirect url has to be exactly the same on mlkshk.com and in your code or the server will return a 500 server error when you try to authenticate.

Once you click the big "Create" button, you'll be given a "Key" and a "Secret". Write those down. We'll need them later.

### Usage

Start a python interpreter and then import the API:

    from pyshk.api import Api

If you don't have an access token (you won't if this is the first run), start up the API using the Key and Secret from above:

    a = Api(consumer_key=[Key], consumer_secret=[Secret])
    a.get_auth(redirect_uri=[the redirect url from above])

At this point, your web browser will open and you'll be prompted to allow your application (whatever you named it) to access your account. Allow the app access and you'll be redirected to whatever redirect URL you specified when creating the app. The URL bar will have something like `http://[redirect_url]?code=[code]`. Copy and paste the code back into the python interpreter and hit enter. You'll then be given an access token and secret. Write those down.

At this point, the API is authenticated and you can start making calls to the mlkshk server.

### API Coverage:

#### Working resources:
* `GET /api/favorites`
* `GET /api/friends`
* `GET /api/user`
* `GET /api/user_id/(user_id)`
* `GET /api/user_name/(username)`
* `GET /api/incoming`
* `GET /api/magicfiles`
* `GET /api/shakes`
* `GET /api/sharedfile/(sharekey)`
* `GET /api/sharedfile/(sharekey)/comments`
* `GET /api/shakes/(id)`
* `POST /api/upload`
* `POST /api/sharedfile/(sharekey)/like`

#### Untested resources
* `GET /api/favorites/after/(afterkey)`
* `GET /api/favorites/before/(beforekey)`
* `GET /api/friends/after/(afterkey)`
* `GET /api/friends/before/(beforekey)`
* `GET /api/incoming/(id)/after/(afterkey)`
* `GET /api/incoming/(id)/before/(beforekey)`
* `GET /api/magicfiles/(id)/after/(afterkey)`
* `GET /api/magicfiles/(id)/before/(beforekey)`
* `GET /api/shakes/(id)/after/(afterkey)`
* `GET /api/shakes/(id)/before/(beforekey)`
* `POST /api/sharedfile/(sharekey)`
* `POST /api/sharedfile/(sharekey)/comments`
* `POST /api/sharedfile/(sharekey)/save`

#### Notes
* `POST /api/upload` returns a 200 response, not 201 as stated in mlkshk docs.
* `GET /api/user_id/[x]` & `GET /api/user_name[x]` for user x who does not exist raises a 500 Server Error, not 404 as in the API docs.
