# Cloudtoken Centrify Auth Plugin

This is an Centrify auth plugin for [Cloudtoken](https://bitbucket.org/atlassian/cloudtoken).

## Installation

    $ pip3 install cloudtoken-plugin.centrify

## Configuring Centrify plugin.

You will need to add the `centrify` plugin to auth section your `~/.config/cloudtoken/config.yaml` and have the `saml` plugin
immediately after it. Your `config.yaml` should look something like this: 

    auth:
        - centrify
        - saml

You will also need to add the following config url into `config.yaml`:

    defaults:
      centrify:
        appkey: <your Centrify AWS app key>
        tenant_id: <your Centrify Tenant ID>

There are also a few bits of optional, but recommended, configuration.

### Auth Preferences

When authenticating with Centrify you will be presented with 1 or more Challenges. Each Challenge contain
from one or more Authentication Mechanisms. You must successfully authenticate using one of the listed mechanisms for
the Challenge to be successful. After a successful Challenge you will either move on to the next Challenge or be
authenticated.

If you do not specify your Authentication Mechanism preferences in your `config.yaml` Cloudtoken will prompt you for 
which Authentication Mechanism you would like to use for each Challenge. Specifying this configuration will allow the
Centrify plugin to automatically select your Authentication Mechanism in order of your preferences listed if they are
listed as an available option.

For example the below example would prefer Password authentication followed by MFA. This works well with Centrify
configurations which prompt for a password during the first Challenge and then an MFA code for the second Challenge.

The values are matched first against the Centrify 'UiPrompt' value and secondly against the
'PromptSelectMech' value.

    defaults:
      centrify:
        auth_preferences:
            - Password
            - MFA (US-East-1)

NOTE: The above auth_preference values will most likely be different for you as they are freeform text configured
in Centrify.
            
### Centrify Vanity ID

Centrify allows you to use a vanity URL, e.g https://mycorp.my.centrify.com rather than the default
https://<tenantid>.my.centrify.com url. If you have a vanity URL configured then Centrify will redirect you to this
URL if you attempt to use the tenant ID URL. This results in a delay in authentication while the redirection occurs. By
specifying the Vanity ID in your `config.yaml` the Centrify plugin can make requests to your vanity URL directly

    defaults:
      centrify:
        vanity_id: mycorp
        
### Complete config example

    defaults:
      centrify:
        appkey: <your Centrify AWS app key>
        tenant_id: <your Centrify Tenant ID>
        vanity_id: <your vanity id>
        auth_preferences:
        - Password
        - MFA (US-East-1)
        

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