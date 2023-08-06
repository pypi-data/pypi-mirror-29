# Cloudtoken

Utility for authenticating with IdP's and obtaining access credentials form public cloud providers on the command line.
Also provides a fake AWS metadata endpoint for local development.

You can contact us via Bitbucket Cloud issues or on our community Discord server, https://discord.gg/rb3hZky

## Why do I need this?

If you use a public cloud provider with Federated Authentication then this utility is for you. 

Here's an example of how to use it:

    $ cloudtoken
    Available roles to choose from:
        1. arn:aws:iam::xxxxxxxxxxxx:role/Sysadmin-Role
        2. arn:aws:iam::xxxxxxxxxxxx:role/User-Role
    
    Enter number of role you want: 2
    Using role arn:aws:iam::xxxxxxxxxxxx:role/User-Role
    
    $ env | grep AWS
    AWS_ROLE_NAME=User-Role
    AWS_SECRET_ACCESS_KEY=<snipped>
    AWS_EXPIRATION_TIMESTAMP=2017-11-28T04:50:03Z
    AWS_DELEGATION_TOKEN=<snipped>
    AWS_LASTUPDATED=2017-11-28T03:50:04Z
    AWS_EXPIRATION=2017-11-28T04:50:03Z
    AWS_SESSION_TOKEN=<snipped>
    AWS_ACCESS_KEY_ID=<snipped>
    AWS_ACCOUNT_ID=xxxxxxxxxxxx
    AWS_SECURITY_TOKEN=<snipped>

In the above example I have run `cloudtoken` which authenticates me against our in house IdP then obtains a list of
IAM Roles I have access to. After selecting the IAM Role `cloudtoken` does the SAML dance with AWS and obtains a set
of ephemeral credentials which are then made available to my shell. Any application written using the AWS SDK's will
use these environment variables to authenticate with AWS API's. 

Almost all functionality is provided via plugins. In this way the tool can be used with any authentication source or
cloud provider. We have included example plugins for using Microsoft ADFS as an IdP and output plugins for making the
tokens available in your shell, writing them out to JSON and also putting them into your `~/.aws/credentials` file.


## Quick Usage

    $ cloudtoken -f sysadmin-role

## Installation

### Prerequisites

* Python >= 3.5

### First install the Cloudtoken packages from Pypi.

    $ pip3 install cloudtoken cloudtoken-plugin.saml cloudtoken-plugin.shell-exporter cloudtoken-plugin.json-exporter

This installs both the core package and standard plugin packages via PyPi.

### Initialise the Cloudtoken configuration directory and copy in the configuration files.

    $ cloudtoken --init
    Creating /home/testuser/.config/cloudtoken directory.
    Populating /home/testuser/.config/cloudtoken with skeleton configuration files.

### Add the following to your .bash_profile
You will then need to add the following to your Bash files to source in the shell additions. If you have installed
the package under a virtualenv or similiar you will need identify where the `bashrc_additions` file is located and
substitute that path in the code below.

    if [[ -f /usr/local/share/cloudtoken/shell_additions/bashrc_additions ]]; then
        source /usr/local/share/cloudtoken/shell_additions/bashrc_additions
    fi

You will need to start a new shell for it to take effect

## Usage

    $ cloudtoken --help
    usage: cloudtoken [-h] [-u USERNAME] [-p PASSWORD]
                    [--password-file PASSWORD_FILE] [-U] [-q]
                    [--refresh-interval REFRESH_INTERVAL] [--debug] [-d] [-i] [-l]
                    [-f FILTER] [-n] [--refresh] [-r ROLE_NUMBER] [-j JSON_TOKENS]
                    [-t] [-e]

    Sets AWS token in your command line so you can run aws cli tools.

    optional arguments:
      -h, --help            show this help message and exit
      -u USERNAME, --username USERNAME
                            Your username
      -p PASSWORD, --password PASSWORD
                            Your password.
      --password-file PASSWORD_FILE
                            File containing your password.
      -U, --unset           Execute unset() in all plugins. Normally removes any
                            credential files plugins have written.
      -q, --quiet           Suppress most output.
      --refresh-interval REFRESH_INTERVAL
                            How often do we refresh the token (in seconds) if
                            --deamon (-d) is specified.
      --debug               Print debug information.
      -d, --daemon          Run a fake AWS metadata proxy.
      -i, --init            Initialise .cloudtoken directory and populate with
                            skeleton files.
      -l, --list            List all roles available to the user then exit.
      -f FILTER, --filter FILTER
                            Only show roles matching filter.
      -n, --numbers-only    Only list role numbers. Useful for automation.
      --refresh             Refresh tokens for last selected Role.
      -r ROLE_NUMBER, --role-number ROLE_NUMBER
                            Specify a role without prompting you to select from
                            the list.
      -j JSON_TOKENS, --json-tokens JSON_TOKENS
                            Specify location of tokens.json file.
      -t, --temp            Set tokens in this shell only.
      -e, --export          Print the tokens.shell file suitable for eval'ing in a
                            shell script.

## Documentation

Cloudtoken allows command line access to the ephemeral tokens obtained when using AWS Federated authentication. These
tokens are normally only valid for 60 minutes which is not an issue when performing long running tasks inside AWS as
your SDK will automatically retrieve a new set of tokens from the AWS metadata endpoint (http://169.254.169.254) when
your existing set expire, but does cause problems when you are trying to perform long running tasks in your local dev
environment (aka laptop). We've worked around this limitation by building a replica metadata endpoint into cloudtoken
(--daemon):

    $ cloudtoken -f training -r 1 -d
    Launching in daemon mode...
    Configuring link-local address on lo0...done.
    Using role arn:aws:iam::xxxxxxxxxx:role/Training-Role
    Metadata proxy now available on http://169.254.169.254
    ------------------------------------------------------
    169.254.169.254 - - [07/04/2017 11:17:06] "GET http://169.254.169.254/ HTTP/1.1" 200
    169.254.169.254 - - [07/04/2017 11:17:09] "GET http://169.254.169.254/latest/meta-data/ HTTP/1.1" 200

    In another shell...

    $ curl http://169.254.169.254
    latest
    2016-09-02

    $ curl http://169.254.169.254/latest/meta-data/
    ami-id
    ami-launch-index
    ami-manifest-path
    block-device-mapping/
    hostname
    iam/
    instance-action
    instance-id
    instance-type
    kernel-id
    local-hostname
    local-ipv4
    mac
    metrics/
    network/
    placement/
    profile
    public-keys/
    reservation-id
    security-groups
    services/

Daemon mode is configured via ~/.config/cloudtoken/proxy.yaml

If you don't want to use daemon mode then plugins exist to export your credentials to your shell as environment
variables which all the AWS SDK's will use if available.

Almost all the functionality is provided by plugins which can be loaded in 3 stages: pre-auth, auth and post-auth. The
plugins to load and the order in which they are loaded is specified in a YAML configuration file
(~/.config/cloudtoken/config.yaml):

    plugins:
        pre_auth:
            - version_check
        auth:
            - idp
            - saml
        post_auth:
            - export_credentials_json
            - export_credentials_shell
            - export_credentials_awscli
    defaults:
            username: charlie

As you can see above it's also possible to specify default values for the argparse arguments.

An example plugin in the pre-auth stage might check that your plugin packages are up to date, while the plugins in the
auth stage might validate you with your Identity Provider and then process the SAML response from AWS. A post-auth
plugin might then write the obtained credentials out to a file that is sourced by your shell as environment variables.
Most of the plugins just described have already been written and are available for use.

## Plugins

Most of the features provided by cloudtoken are implemented via plugins. Plugins must exist in the cloudtoken_plugin module
namespace. For an easy to understand plugin example see the export_credentials_json plugin in the
cloudtoken-standard-plugins package.

Example plugin:

    class Plugin(object):
        def __init__(self, config):
            self._config = config
            self._name = 'example_plugin'
            self._description = 'This is my example plugin.'

        def __str__(self):
            return __file__

        @staticmethod
        def unset(args):
            """ When --unset is passed this function will be run. Used for cleaning up resources."""
            pass

        def arguments(self, defaults):
            """ Provides arguments to load into argparse. """
            parser = argparse.ArgumentParser()
            parser.add_argument("-s",
                                "--json-tokens",
                                type=str,
                                dest="json_tokens",
                                help="Specify location of tokens.json file that will be written out.",
                                default=defaults.get('json-tokens', "{0}/tokens.json".format(self._cloudtoken_dir)))
            parser.add_argument("-t",
                                "--temp",
                                dest="temp",
                                action="store_true",
                                default=defaults.get('temp', False),
                                help="Set tokens in current shell only.")
            return parser

        def execute(self, data, args, flags):
            """ Main execution method for the plugin. """
            try:
                # Load some data from the previous plugin.
                # You can reference it by plugin name or location in the plugin chain.
                data = dict(data[-1])['data']
            except KeyError:
                print("Unable to load data from previous plugin. Exiting.")
                exit(1)

            # Store some output data for other plugins to use.
            data.append({'plugin': self._name, 'data': data})
            return data

## Known Issues

None. Please raise any issues found.

## Tests

None. We should probably make some.

## Contributors

Pull requests, issues and comments welcome. For pull requests:

* Add tests for new features and bug fixes
* Follow the existing style
* Separate unrelated changes into multiple pull requests

See the existing issues for things to start contributing.

For bigger changes, make sure you start a discussion first by creating
an issue and explaining the intended change.

Atlassian requires contributors to sign a Contributor License Agreement,
known as a CLA. This serves as a record stating that the contributor is
entitled to contribute the code/documentation/translation to the project
and is willing to have it used in distributions and derivative works
(or is willing to transfer ownership).

Prior to accepting your contributions we ask that you please follow the appropriate
link below to digitally sign the CLA. The Corporate CLA is for those who are
contributing as a member of an organization and the individual CLA is for
those contributing as an individual.

* [CLA for corporate contributors](https://na2.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=e1c17c66-ca4d-4aab-a953-2c231af4a20b)
* [CLA for individuals](https://na2.docusign.net/Member/PowerFormSigning.aspx?PowerFormId=3f94fbdc-2fbe-46ac-b14c-5d152700ae5d)

## License

Copyright (c) 2016 Atlassian and others.
Apache 2.0 licensed, see [LICENSE.txt](LICENSE.txt) file.
