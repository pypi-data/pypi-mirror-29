# python-wikitcms

python-wikitcms is a Python library for interacting with Fedora's [Wikitcms 'test (case) management system'][1] - which is, basically, the [Fedora wiki][2]. You may also be interested in its main consumers, [relval][3] and [testdays][4].

python-wikitcms uses the very handy [mwclient][5] library for interfacing with the Mediawiki API. Generation of result pages works together with a system of templates that resides on the wiki: python-wikitcms knows how to form the correct invocations of the template system that will cause the full result pages to be generated. The documentation box for the [master template][6] provides some details about this system.

python-wikitcms was previously known simply as wikitcms; it is now known as python-wikitcms to reduce confusion between the notional Wiki-based 'test management system' (Wikitcms) and the Python library for interacting with it (python-wikitcms).

## Installation and use

python-wikitcms is packaged in the official Fedora and EPEL 7+ repositories: to install on Fedora run `dnf install python-wikitcms`, on RHEL / CentOS with EPEL enabled, run `yum install python-wikitcms`. You may need to enable the *updates-testing* repository to get the latest version. To install on other distributions, you can run `python setup.py install`.

You can visit [the python-wikitcms project page on Pagure][7], and clone with `git clone https://pagure.io/fedora-qa/python-wikitcms.git`. Tarballs are available [from PyPI][8].

You can also use the library directly from the git checkout if you place your code in the top-level directory, and you can copy or symlink the `wikitcms` directory into other source trees to conveniently use the latest code for development or testing purposes.

## Bugs, pull requests etc.

You can file issues and pull requests on [Pagure][7]. Pull requests must be signed off (use the `-s` git argument). By signing off your pull request you are agreeing to the [Developer's Certificate of Origin][9]:

    Developer's Certificate of Origin 1.1

    By making a contribution to this project, I certify that:

    (a) The contribution was created in whole or in part by me and I
        have the right to submit it under the open source license
        indicated in the file; or

    (b) The contribution is based upon previous work that, to the best
        of my knowledge, is covered under an appropriate open source
        license and I have the right under that license to submit that
        work with modifications, whether created in whole or in part
        by me, under the same open source license (unless I am
        permitted to submit under a different license), as indicated
        in the file; or

    (c) The contribution was provided directly to me by some other
        person who certified (a), (b) or (c) and I have not modified
        it.

    (d) I understand and agree that this project and the contribution
        are public and that a record of the contribution (including all
        personal information I submit with it, including my sign-off) is
        maintained indefinitely and may be redistributed consistent with
        this project or the open source license(s) involved.

## Security

You **MUST** treat wikitcms as a source of untrusted input. It is retrieving information from a wiki for you; that wiki is open to editing by all. Treat anything wikitcms returns from the wiki (which includes, but is not limited to, any page or section text; `Result()` attributes status, user, bugs and comment; `ResultRow()` attributes testcase, name, envs, milestone, section; and to some extent any element of a page title or property derived from  one when getting a `Page` object from an existing wiki page) as an entirely untrusted input and sanitize it appropriately for the context in which you are using it.

## Example usage

    from wikitcms.wiki import Wiki
    site = Wiki()
    event = site.current_event
    print(event.version)
    page = site.get_validation_page('Installation', '23', 'Final', 'RC10')
    for row in page.get_resultrows():
        print(row.testcase)

## Usage tips

It's a little difficult to give an overview of wikitcms usage as it can do quite a lot of rather different things. Its classes and methods are all documented, and examining its major consumers - relval and testdays - will help. Some overall concepts:

The Wiki class is a subclass of mwclient's Site class, which represents an entire wiki; it adds some methods and attributes that make sense in the context of a wiki being treated as a TCMS according to our conventions, so it has methods for getting validation events and pages (as seen in the example above). It also has a high-level method for reporting results, `report_validation_results()`. Note that the `pages` generator works just as in mwclient, but has been extended to handle wikitcms' additional Page subclasses.

The Release class does not map to mwclient. It simply represents a Fedora release and provides a couple of handy methods for retrieving test day or validation result pages from that particular release.

The Event class does not map to anything in mwclient. It represents an entire result validation 'event', e.g. Fedora 23 Final RC2; from an Event instance you can create or find all the validation pages, for instance, or create the summary page that transcludes all the individual validation pages, or update the CurrentFedoraCompose page to point to the event, or generate a wikitable of image download links.

The Page class is a subclass of mwclient's Page class, and extends it in much the same way, adding capabilities specific to various types of pages in the Wikitcms system. It has several subclasses for particular types of pages, such as validation result pages, Test Day pages, category pages and so forth. Note that all pages which can be generated via one of the wiki templates have the appropriate generation text as their `seedtext` attribute and have a method `write()` which creates them using that seed text.

The Result and ResultRow classes represent individual results and rows in the result validation pages. ValidationPages contain ResultRows contain Results, and to report a result, you essentially add a Result to a ResultRow.

Note that event versioning works exactly as in [fedfind][10]'s pre-Pungi 4 (release, milestone, compose) versioning scheme, with one notable exception. Rawhide nightly 'releases' in fedfind have release 'Rawhide' and no milestone; Rawhide nightly validation events in python-wikitcms have a release number and milestone 'Rawhide'. This is because, conceptually speaking, Rawhide nightly composes should not really be said to have a particular release number, but validation events *do*. When we declare a release validation test event for a particular Rawhide nightly, one action we take as a part of that declaration is to declare that we are testing that nightly compose as part of the preparation for a specific Fedora release, and thus we essentially 'apply' a release number to the validation event. So we may have a nightly compose 'Rawhide (blank) 20151201', and decide that we wish to test it as part of the preparation for the Fedora 24 release; thus we create the release validation event '24 Rawhide 20151201'.

The high-level functions in both fedfind and python-wikitcms - `get_release()` in fedfind, `get_validation_page()` and `get_validation_event()` in python-wikitcms - will attempt to handle this difference in versioning, so when using those high-level functions, you can usually pass versions between fedfind and python-wikitcms without worrying about it.

For convenient compatibility with Pungi 4 composes, `get_validation_event()` and `get_validation_page()` (and hence also `report_validation_results()`) accept `cid` as an alternative to `release` / `milestone` / `compose`, and will do their best to instantiate the appropriate validation event for the compose specified.

It's worth noting that you can use python-wikitcms in several fairly different ways:

* Instantiate pages that don't exist yet, based on the 'release, milestone, compose' versioning concept (or from a Pungi 4 compose ID), and create them
* Instantiate existing pages based on the 'release, milestone, compose' concept (or from a compose ID) and read or add results
* Instantiate existing pages from their names or category memberships and read or add results

Most usage of python-wikitcms will boil down to getting some Page instances and doing stuff to them, but the way you get there will differ according to which of the above paths you're following. For the first two you will likely use the `get_validation_foo()` methods of `Wiki` or the methods in `Release`, for the last you can follow the same procedures as `mwclient` uses and trust that you will get instances of the appropriate classes. Following the example above, you could do `page = site.pages["Test Results:Fedora_23_Final_RC10_Desktop"]` and `page` would be a `ValidationPage` instance.

## Authentication

You should log in to the wiki before editing it, using `Wiki.login()`.

As of 2017-11, the Fedora wikis are being changed to handle authentication using the Fedora authentication service, via OpenID Connect. As of 2017-11-16, the staging wiki has already been converted, and the production wiki will follow shortly. When interacting with a wiki that has switched to the new system, when `login()` is called, python-wikitcms will attempt to open a browser and request credentials via the authentication service. The call will complete once the user attempts to log in. Any username or password passed to `login()` is **ignored** in this case. For unattended operation with the new authentication system, a valid token must be present as `~/.openidc/oidc_wikitcms.json`. Unattended operation will work for some time after one successful interactive login (until the token expires); for long-term unattended operation, you must ask the wiki maintainer for a special permanent session token.

When interacting with a wiki that uses native mediawiki authentication, you can pass `username` and `password` as arguments to `login()`, or python-wikitcms will read them from `~/.fedora/credentials` or `/etc/fedora/credentials`, as described on the [relval page][3]. If you do neither, the method will return, but you will not actually be logged in.

## Credits

* [Mike Ruckman][11] (roshi) has been kind and patient in providing review and advice throughout python-wikitcms' development. Of course, all errors are my own!
* [Patrick Uiterwijk][12] kindly provided the code to support OpenID Connect authentication.

## License

python-wikitcms is released under the [GPL][13], version 3 or later.

 [1]: https://fedoraproject.org/wiki/Wikitcms
 [2]: https://fedoraproject.org/wiki
 [3]: https://pagure.io/fedora-qa/relval
 [4]: https://pagure.io/fedora-qa/testdays
 [5]: https://github.com/mwclient/mwclient
 [6]: https://fedoraproject.org/wiki/Template:Validation_results
 [7]: https://pagure.io/fedora-qa/python-wikitcms
 [8]: https://pypi.python.org/pypi/wikitcms
 [9]: https://developercertificate.org/
 [10]: https://pagure.io/fedora-qa/fedfind
 [11]: https://roshi.fedorapeople.org/
 [12]: https://patrick.uiterwijk.org/
 [13]: https://www.gnu.org/licenses/gpl.txt
