# Cloudtoken ADFS Auth Plugin

This is an Microsoft ADFS auth plugin for [Cloudtoken](https://bitbucket.org/atlassian/cloudtoken).

## Installation

    $ pip3 install cloudtoken-plugin.adfs

## Configuring Cloudtoken

You will need to add the `adfs` plugin to auth section your `~/.config/cloudtoken/config.yaml` and have the `saml` plugin
immediately after it. You `config.yaml` should look something like this: 

    auth:
        - adfs
        - saml

You will also need to add the ADFS url into `config.yaml` as a top level key. Your config.yaml should look something
like this:

    adfs_url: 'https://myidp.mydomain.com/adfs/ls/IdpInitiatedSignOn.aspx?loginToRp=urn:amazon:webservices'
    plugins:
        pre_auth:
        auth:
            - idp
            - saml
        post_auth:
            - export_credentials_shell

If you have not yet configured Microsoft ADFS I recommend these links:

* https://aws.amazon.com/blogs/security/how-to-set-up-sso-to-the-aws-management-console-for-multiple-accounts-by-using-ad-fs-and-saml-2-0/
* https://aws.amazon.com/blogs/security/how-to-establish-federated-access-to-your-aws-resources-by-using-active-directory-user-attributes/
   

## 401's when authenticating?
IIS might be trying to authenticate your credentials using Windows Authentication instead of Forms authentication.

You can follow the instructions [here](http://www.richardawilson.com/2010/10/adfs-20-login-page.html) to fix that.

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