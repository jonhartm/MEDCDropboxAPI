"""Session definiton module."""
import dropbox
import logging
import json
import os

#to get medcbox package version
import importlib.metadata

logger = logging.getLogger(__name__)


class Session:
    """
    Class that represents a user's authenticated connection to Dropbox.
    """
    #Constructor
    def __init__(self, secrets):
        self.client = None
        logger.info("Starting authentication flow.")
        self.authorize(secrets)


    #Properties
    def user(self):
        """
        Gets name of currently logged user.
        """
        return self.client.users_get_current_account()

    #Authorizes user and establishes client to make API requests as user.
    def authorize(self, secrets):
        """
        Authenticate the session using provided secrets

        Args:
            secrets(str or dict):
            Either a path to a json file or a dictionary of credentials.

        Returns:
            None
        """
        #Checking the passed secrets variable
        if isinstance(secrets, str):
            if os.path.exists(secrets):
                try:
                    with open(secrets) as f:
                        creds = json.load(f)
                except json.decoder.JSONDecodeError:
                    logger.debug("Invalid json file. Please check the path.")
            else:
                raise FileNotFoundError("Please provide a valid path.")
        elif isinstance(secrets, dict):
            creds = secrets
        else:
            raise TypeError("Expecting either a path(str) or dict; recieved a "+
                            f"{type(secrets)}")

        #Make sure we have the app key
        assert 'app_key' in secrets.keys(), 'secrets must have app_key!'

        #Use the app_key to start the flow
        auth_flow = dropbox.DropboxOAuth2FlowNoRedirect(secrets['app_key'],
                                    use_pkce=True, token_access_type='offline')

        #Getting OAuth token
        authorize_url = auth_flow.start()
        print("1. Go to: " + authorize_url)
        print("2. Click \"Allow\" (you might have to log in first).")
        print("3. Copy the authorization code.")
        auth_code = input("Enter the authorization code here: ").strip()

        try:
            oauth_result = auth_flow.finish(auth_code)
        except Exception as e:
            print('Error: %s' % (e,))
            exit(1)

        #Start the client with the OAuth token we just got
        self.client = dropbox.Dropbox(oauth2_refresh_token=oauth_result.refresh_token,
            user_agent='medcbox/'+importlib.metadata.version('medcbox'),
            app_key=secrets['app_key'])
        logger.info("Successfully set up client!")
