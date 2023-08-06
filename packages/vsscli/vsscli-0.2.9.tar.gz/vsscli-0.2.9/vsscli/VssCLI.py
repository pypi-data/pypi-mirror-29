import os
import json
from click import ClickException
from vsscli import __version__ as product_version,\
    __name__ as product_name
from pyvss import __version__ as __pyvss_version__
from pyvss.manager import VssManager, VssError
from base64 import b64decode, b64encode


class VssCLIError(ClickException):
    pass


class CLIManager(VssManager):

    def __init__(self, click, config,
                 offline=False,
                 tk=None,
                 username=None, password=None,
                 debug=False,
                 output=None):
        super(CLIManager, self).__init__(tk)
        # define user agent
        self.user_agent = self._default_user_agent(
            name=product_name, version=product_version,
            extensions='pyvss/{}'.format(__pyvss_version__)
        )
        self.click = click
        self.output = output
        self.offline = offline
        # debug
        self.debug = debug
        # config dir/file
        self.full_config_path = os.path.expanduser(config)
        # sets username if any
        self.username = username
        # sets password if any
        self.password = password

    def get_token(self, user=None, password=None):
        """
        Generates token based on two environment variables or
        provided OR and password:

        - ``VSS_API_USER``: username
        - ``VSS_API_USER_PASS``: password

        Finally checks for unread messages if any.

        :param user: Username
        :type user: str
        :param password: Username password
        :type password: str
        :return: generated token or VssError

        """
        self.api_token = super(CLIManager, self).get_token(user, password)
        # check for unread messages
        self.check_unread_messages()
        return self.api_token

    @property
    def output_json(self):
        return self.output == 'json'

    def update_endpoints(self, endpoint):
        """ Rebuilds API endpoints
        :param endpoint: Base API endpoint
        :return:
        """
        self.api_endpoint = '{}/v2'.format(endpoint)
        self.base_endpoint = endpoint
        self.token_endpoint = '{}/auth/request-token'.format(endpoint)

    def configure(self, username, password, endpoint, replace=False):
        self.username = username
        self.password = password
        # update instance endpoints if provided
        self.update_endpoints(endpoint)
        # directory available
        if not os.path.isdir(os.path.dirname(self.full_config_path)):
            os.mkdir(os.path.dirname(self.full_config_path))
        # config file
        if os.path.isfile(self.full_config_path):
            try:
                # load credentials by endpoint
                e_username, e_password, e_api_token = \
                    self.load_profile_from_config(self.base_endpoint)
                if not (e_username and e_password and e_api_token):
                    print('Profile not found.')
                    self.write_config_file()

                if e_username and e_password and e_api_token:
                    confirm = replace or self.click.confirm(
                        'Would you like to replace existing configuration?')
                    if confirm:
                        self.write_config_file()
                else:
                    self.click.echo(
                        'Successfully configured credentials for {}. '
                        'You are ready to use '
                        'VSS CLI.'.format(self.base_endpoint))
            except VssCLIError as ex:
                self.click.echo(ex)
                confirm = self.click.confirm(
                    'Would you like to replace existing configuration?')
                if confirm:
                    self.write_config_file()
        else:
            self.write_config_file()

    def load_profile_from_config(self, endpoint):
        username, password, token = None, None, None
        profiles = self.load_raw_config_file()
        profile = profiles.get(endpoint)
        if profile:
            # get auth attr
            auth = profile.get('auth')
            # get token attr
            token = profile.get('token')
            if not auth or not token:
                raise VssCLIError('Invalid configuration file')
            auth_enc = auth.encode()
            credentials_decoded = b64decode(auth_enc)
            # get user/pass
            username, password = \
                credentials_decoded.split(b':')
        return username, password, token

    def load_raw_config_file(self):
        try:
            with open(self.full_config_path, 'r') as f:
                profiles = json.load(f)
                return profiles
        except ValueError as ex:
            raise VssCLIError('Invalid configuration file.')

    def check_unread_messages(self):
        try:
            messages = self.get_user_messages(filter='status,eq,Created',
                                              per_page=100)
            n_messages = len(messages)
            if messages:
                self.click.echo('You have {} unread messages. Please, '
                                'run: vss message ls '.format(n_messages))
        except ValueError as ex:
            self.click.echo('Could not check for messages {}'.format(ex))

    def load_config(self):
        try:
            if os.environ.get('VSS_API_ENDPOINT'):
                self.update_endpoints(os.environ.get('VSS_API_ENDPOINT'))
            # check for environment variables
            if os.environ.get('VSS_API_TOKEN') or \
                    (os.environ.get('VSS_API_USER') and
                     os.environ.get('VSS_API_USER_PASS')):
                # don't load config file
                if os.environ.get('VSS_API_TOKEN'):
                    # set api token
                    self.api_token = os.environ.get('VSS_API_TOKEN')
                    return self.username, self.password, self.api_token
                elif os.environ.get('VSS_API_USER') \
                        and os.environ.get('VSS_API_USER_PASS'):
                    # generate a new token - won't save
                    try:
                        self.get_token()
                    except VssError as ex:
                        raise VssCLIError(str(ex))
                    return self.username, self.password, self.api_token
                else:
                    raise VssCLIError(
                        'Environment variables error. Please, verify '
                        'VSS_API_TOKEN or VSS_API_USER and VSS_API_USER_PASS')
            else:
                if self.debug:
                    print('Loading configuration file: {}'.format(
                        self.full_config_path))
                if os.path.isfile(self.full_config_path):
                    # read config and look for profile
                    self.username, self.password, self.api_token = \
                        self.load_profile_from_config(self.base_endpoint)
                    if self.debug:
                        print('Loaded from file {}: {}'.format(
                            self.base_endpoint, self.username
                        ))
                    creds = self.username and self.password
                    if not (creds or self.api_token):
                        raise VssCLIError(
                            "Invalid endpoint {} configuration. \n "
                            "Please, run 'vss configure' to add "
                            "endpoint to "
                            "configuration.".format(self.base_endpoint))
                    try:
                        self.whoami()
                    except VssError as ex:
                        if self.debug:
                            print(ex)
                            print('Generating a new token')
                        self.api_token = self.get_token(self.username,
                                                        self.password)
                        if self.debug:
                            print('Token generated successfully')
                        self.write_config_file(new_token=self.api_token)
                    return self.username, self.password, self.api_token
            raise VssCLIError("Invalid configuration. "
                              "Please, run "
                              "'vss configure' to initialize configuration.")
        except Exception as ex:
            raise VssCLIError(str(ex))

    def write_config_file(self, new_token=None):
        """
        Creates or updates configuration file with different
        endpoints.

        :param new_token: new api token to store
        :return:
        """
        token = new_token or self.get_token(self.username,
                                            self.password)
        username = self.username if isinstance(self.username, bytes) \
            else self.username.encode()
        password = self.password if isinstance(self.password, bytes) \
            else self.password.encode()
        credentials = b':'.join([username,
                                 password])
        config_dict = {self.base_endpoint: {
            'auth': b64encode(credentials).strip().decode('utf-8'),
            'token': token}
        }
        try:
            self.click.echo('Writing configuration '
                            'file: {}'.format(self.full_config_path))
            # validate if file exists
            if os.path.isfile(self.full_config_path):
                with open(self.full_config_path, 'r+') as fp:
                    try:
                        _conf_dict = json.load(fp)
                    except ValueError:
                        _conf_dict = {}
                    _conf_dict.update(config_dict)
                    fp.seek(0)
                    json.dump(_conf_dict, fp,
                              sort_keys=True,
                              indent=4)
                    fp.truncate()
            else:
                with open(self.full_config_path, 'w') as fp:
                    _conf_dict = config_dict
                    json.dump(_conf_dict, fp,
                              sort_keys=True,
                              indent=4)
        except IOError as e:
            raise VssCLIError('An error occurred writing '
                              'configuration file: {}'.format(e))

        self.click.echo('Successfully written configuration '
                        'file {}'.format(self.full_config_path))
