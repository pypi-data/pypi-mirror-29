passivetotal
============

PassiveTotal client

Installation
------------

From the project root directory::

    $ python setup.py install

Usage
-----

Simply run it::

    $ passivetotal

Use --help/-h to view info on the arguments::

    $ passivetotal --help

Use setup to apply your username and api key::

    $ passivetotal setup <username> <api key>


Usage Examples
-----
Get account info::

    $ passivetotal account --account

Get quotas::

    $ passivetotal account --quotas
    $ passivetotal account --quotas --json #it's a bit easier to read as json

Create a project::

    $ passivetotal project create "<project name>" {public, private}

Update a project::

    $ passivetotal project update "<project UUID>" --tags <comma separated tags> \
    --description "<short description for the project>" --visibility {public, private}

Delete a project::

    $ passivetotal project delete "<project UUID>"

Find a project::

    $ passivetotal project find -h

Create an artifact::

    $ passivetotal artifact create <project UUID> <artifact queries>

Tag items::

    $ passivetotal actions tag set <comma separated tags> #set tags
    $ passivetotal actions tag add <comma separated tags> #add tags
    $ passivetotal actions tag delete <comma separated tags> #remove tags

Get enrichment data::

    $ passivetotal enrich <domain to enrich>
    $ passivetotal enrich --osint <domain to enrich>
    $ passivetotal enrich --malware <domain to enrich>
    $ passivetotal enrich --subdomains <domain to enrich>

Get whois info::

    $ passivetotal whois <domain> 
    $ passivetotal whois <domain> --json #sometimes it's easier to read the json response
    $ passivetotal whois <query> --field <field to search by>
    $ passivetotal whois --keyword <query>

Get pdns info::

    $ passivetotal dns <domain>
    $ passivetotal dns --unique <domain>
    $ passivetotal dns --keyword <keyword>

Get ssl info::

    $ passivetotal ssl <sha1>
    $ passivetotal ssl --keyword <keyword>
    $ passivetotal ssl --field <field> <query>

Release Notes
-------------

:1.0.0:
    Project released
