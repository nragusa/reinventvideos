# Overview

To get the backend working, you'll need a few things in place:

* Create a virtualenv and install the requirements from requirements.txt via pip.
* Symlink the directory site-packages (in the current directory) to the site-packages directory within the virtualenv
* Create parameters in Systems Manager Parameter Store to hold the values of the YouTube developer key, Algolia API key, Algolia App name, and Algolia indexes. The parameter names are referenced in the update-youtube-stats function in the serverless.yml config. (This also assumes you already have an Algolia account and indexes up and running!)
* [Deploy](https://serverless.com/framework/docs/providers/aws/guide/deploying/) with the serverless framework