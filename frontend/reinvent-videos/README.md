# Overview

To get the frontend up and running, you'll need to do the following:

* Specify Algolia configuration in the appropriate `env.environment` file. There's a blank one for the development environment as reference.
* For production deployment, make sure to have a CloudFront distribution with an S3 bucket already created. After a quick build of this environment, you simply need to sync the contents of the dist/ directory into the S3 bucket.

## Project setup

```bash
yarn install
```

### Compiles and hot-reloads for development

```bash
yarn run serve
```

### Compiles and minifies for production

```bash
yarn run build
```

### Run your tests

```bash
yarn run test
```

### Lints and fixes files

```bash
yarn run lint
```
