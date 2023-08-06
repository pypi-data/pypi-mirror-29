prbit
======

Pull Request Cli Tool for Bitbucket. Cli Library by Click : http://click.pocoo.org

Install
-------

Use pip package manager for python 
**pip install prbit**

How to usage
------------

- **First** : You should run `prbit config` for Create configuration file.

  Usage: prbit config [OPTIONS]

  Options:
    -u, --username  Username of Bitbucket Account
    -p, --password  Password of Bitbucket Account


- **Second** : Next run `prbit create` to create pull request.

  Usage: prbit create [OPTIONS]

  Options:
    -t, --topic         Topic of Pull-Request
    -d, --description   Description
    -r, --repo          Repository
    -s, --source        Source Branch
    -t, --target        Target Branch
    -u, --reviewer      Assign some user to review



