import os
import md5
import time
from gittip.models import Participant
from gittip.elsewhere import AccountElsewhere, _resolve

www_host = os.environ['BOUNTYSOURCE_WWW_HOST'].decode('ASCII')
api_host = os.environ['BOUNTYSOURCE_API_HOST'].decode('ASCII')

class BountysourceAccount(AccountElsewhere):
    platform = u'bountysource'

    def get_url(self):
        url = "https://www.bountysource.com/#users/%s" % self.user_info["slug"]
        return url


def resolve(login):
    return _resolve(u'bountysource', u'login', login)


def oauth_url(website, participant, redirect_url=None):
    """Return a URL to authenticate with Bountysource.

    :param participant:
        The participant whose account is being linked

    :param redirect_url:
        Optional redirect URL after authentication. Defaults to value defined
        in local.env

    :returns:
        URL for Bountysource account authorization
    """
    if redirect_url:
        return "/on/bountysource/redirect?redirect_url=%s" % redirect_url
    else:
        return "/on/bountysource/redirect"


# Bountysource Access Tokens
# ==========================

def create_access_token(participant):
    """Return an access token for the Bountysource API for this user.
    """
    time_now = int(time.time())
    token = "%s.%s.%s" % ( participant.id
                         , time_now
                         , hash_access_token(participant.id, time_now)
                          )
    return token


def hash_access_token(user_id, time_now):
    """Create hash for access token.
    :param user_id:
        ID of the user.

    :param time_now:
        Current time, in seconds, as an integer.

    :returns:
        MD5 hash of user_id, time, and Bountysource API secret
    """
    raw = "%s.%s.%s" % ( user_id
                       , time_now
                       , os.environ['BOUNTYSOURCE_API_SECRET'].decode('ASCII')
                        )
    return md5.new(raw).hexdigest()


def access_token_valid(access_token):
    """Helper method to check validity of access token.
    """
    parts = (access_token or '').split('.')
    return len(parts) == 3 and parts[2] == \
                                          hash_access_token(parts[0], parts[1])


def get_participant_via_access_token(access_token):
    """From a Gittip access token, attempt to find an external account

    :param access_token:
        access token generated by Gittip on account link redirect

    :returns:
        the participant, if found
    """
    if access_token_valid(access_token):
        parts = access_token.split('.')
        participant_id = parts[0]
        return Participant.query.filter_by(id=participant_id).one()


def filter_user_info(user_info):
    """Filter the user info dictionary for a Bountysource account.

    This is so that the Bountysource access token doesn't float around in a
    user_info hash (considering nothing else does that).

    """
    whitelist = ['id', 'display_name', 'first_name', 'last_name', 'email', \
                                                                  'avatar_url']
    filtered_user_info = {}
    for key in user_info:
        if key in whitelist:
            filtered_user_info[key] = user_info[key]

    return filtered_user_info

