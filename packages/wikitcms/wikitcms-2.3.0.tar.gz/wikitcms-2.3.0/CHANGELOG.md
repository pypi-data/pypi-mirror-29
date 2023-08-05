## Changelog

### 2.3.0 - 2018-02-20

*   [wikitcms-2.3.0.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.3.0.tar.gz)

1.  Improve handling of corner cases around candidate compose event fedfind release discovery
2.  Extend test suite
3.  pylint cleanups
4.  Use image URLs provided by fedfind rather than constructing ourselves (needs fedfind 3.3.0)

### 2.2.2 - 2017-12-07

*   [wikitcms-2.2.2.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.2.2.tar.gz)

1.  Don't pass `oldtext` kwarg to mwclient `save()` method, which doesn't understand it

### 2.2.1 - 2017-11-16

*   [wikitcms-2.2.1.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.2.1.tar.gz)

1.  **NEW**: Support OpenID Connect authentication for Fedora wikis

### 2.2.0 - 2017-11-10

*   [wikitcms-2.2.0.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.2.0.tar.gz)

1.  **NEW**: Support validation events for Fedora-Modular composes (Fedora 27 Modular Server)
2.  **API**: `helpers.cid_to_event` now returns 4-tuple not 3-tuple (added `dist` as first value)
3.  **API**: `ResTuple` is now a 15-tuple not 14-tuple (added `modular` as last item)

### 2.1.11 - 2017-03-17

*   [wikitcms-2.1.11.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.1.11.tar.gz)

1.  Include download table and individual page links in summary pages

### 2.1.10 - 2016-12-16

*   [wikitcms-2.1.10.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.1.10.tar.gz)

1.  Drop the page edit captcha solving code entirely, it's useless since MW 1.18
2.  Drop downstream addition of `end` arg for `TcmsPageList` again (merged upstream in 0.8.2)
    Requires mwclient 0.8.2 or higher

### 2.1.9 - 2016-12-16

*   [wikitcms-2.1.9.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.1.9.tar.gz)

This update addresses a security issue with potentially serious consequences
but very limited scope. The issue could have been exploited by a malicious wiki
administrator - with the ability to craft the wiki's response to `save()`
requests - to execute arbitrary code with the privileges of the user running
wikitcms. It was not vulnerable to attack by anyone besides a wiki admin.

1.  **SECURITY** Finally get rid of the `eval()` usage in captcha handling

### 2.1.8 - 2016-12-08

*   [wikitcms-2.1.8.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.1.8.tar.gz)

1.  Update some fedfind usage (don't use `get_release_cid` any more)
2.  Don't bother trying to find events for FedoraRespin, Fedora-Atomic etc. composes

### 2.1.7 - 2016-11-09

*   [wikitcms-2.1.7.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.1.7.tar.gz)

1.  Convert 'Final' to 'RC' when release is > 24 in `Wiki.get_validation_{event,page}`

### 2.1.6 - 2016-04-20

*   [wikitcms-2.1.6.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.1.6.tar.gz)

1.  **NEW** `Listing.TcmsPageList`: re-add `end` support
2.  **NEW** `Wiki.alltestdays`, `Wiki.allresults`: re-add `end` support

### 2.1.5 - 2016-04-08

*   [wikitcms-2.1.5.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.1.5.tar.gz)

1.  `ValidationPage.find_resultrow`: handle rows that differ only by environment

### 2.1.4 - 2016-03-23

*   [wikitcms-2.1.4.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.1.4.tar.gz)

1.  Drop ability to pass `cid` to `ValidationEvent.create` (and `DownloadPage.__init__`)
2.  Enable running tests from `setup.py`

### 2.1.3 - 2016-03-17

*   [wikitcms-2.1.3.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.1.3.tar.gz)

1.  Adjust `DownloadPage` download table generation to use `subvariant` rather than `payload`

### 2.1.2 - 2016-03-16

*   [wikitcms-2.1.2.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.1.2.tar.gz)

1.  Turn some `Event` instance attributes into properties to avoid unnecessary remote trips

### 2.1.1 - 2016-03-16

*   [wikitcms-2.1.1.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.1.1.tar.gz)

1.  Fix `creation_date` for `NightlyEvent`s that do not yet exist
2.  Improve `triplet_sort` for new-style composes

### 2.1.0 - 2016-03-16

*   [wikitcms-2.1.0.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.1.0.tar.gz)

1.  **MAJOR**: not technically an API change, but pages now have more Pungi 4-like names with respin values
2.  **API**: `Wiki.get_validation_event_url` (added in 2.0.0) is dropped again
3.  **API**: `Wiki.get_validation_{event,page}` no longer do release guessing
4.  **API**: Event properties `has_bootiso` and `compose_exists` dropped
5.  **API**: Event method `get_package_versions` dropped (moved to fedfind)
6.  **NEW**: `Wiki.get_validation_{event,page}` now accept `cid` argument (compose ID)
7.  **NEW**: Events and Pages now have `creation_date` properties, for use in sorting
8.  Major test suite coverage improvements
9.  Several small bug fixes

### 2.0.2 - 2016-03-04

*   [wikitcms-2.0.2.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.0.2.tar.gz)

1.  Add missing 2.0.1 changelog

### 2.0.1 - 2016-03-04

*   [wikitcms-2.0.1.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.0.1.tar.gz)

1.  Move credential reading to helpers, add `/etc/fedora/credentials` as a system wide credentials file

### 2.0.0 - 2016-03-03

*   [wikitcms-2.0.0.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-2.0.0.tar.gz)

This is a major release of python-wikitcms. The most significant change is support for Python 3. To simplify this, and to match mwclient behaviour, python-wikitcms is now intended to always produce unicode strings even under Python 2. I recommend you do the same with any code that uses python-wikitcms: `from __future__ import unicode_literals`. Passing non-unicode literals to python-wikitcms constructors may possibly result in unicode decode errors in Python 2. Python 3 support requires python-mwclient 0.8.1 or higher.

There is also work to adjust to Fedora's new Pungi 4-based compose process. For now this is managed without any incompatible API changes, though a few new API bits are added.

1.  Python 3 support
2.  When running under Python 2, use unicode literals everywhere
3.  Properly handle not-found pages in `Wiki.report_validation_results()`
4.  Resync a few things with upstream mwclient (drop downstream workarounds for bugs)
5.  Add `username` and `fasname` to the list of example names ignored when finding results
6.  Add quite a lot more test coverage
7.  Whitespace-strip comments from old `{{testresult}}` template results
8.  **NEW** `Wiki.get_validation_event_url` for getting an event from a Pungi 4 compose URL
9.  **NEW** `NightlyEvent` now accepts optional `url` param to specify compose location
10. Adjust fedfind parsing a bit to account for new productmd-style image metadata
11. Drop `Event` abstract class (it did almost nothing), `ValidationEvent` is now the top level
11. Fix `ValidationEvent.valid_pages` for `NightlyEvent`s (it was returning `ComposePage`s)
12. **NEW** `ValidationEvent.create()` method for creating the event (code moved from relval)
13. **API** `ResultRow` equality is now done via a `matches()` method instead of 'real' equality
14. Many many smaller bugfixes and pylint cleanups

### 1.13.3 - 2015-12-24

*   [wikitcms-1.13.3.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.13.3.tar.gz)

1.  Fix handling of similarly named resultrows like 'QA:Testcase_foo' and 'QA:Testcase_foo_bar'
2.  Update and reorganize documentation
3.  Add several missing releases to this CHANGELOG

### 1.13.2 - 2015-10-27

*   [wikitcms-1.13.2.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.13.2.tar.gz)

1.  Fix a bug causing triplet_sort to crash in certain cases

### 1.13.1 - 2015-10-26

*   [wikitcms-1.13.1.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.13.1.tar.gz)

1.  Fix RC1 sorting as older than TC10 in sort functions

### 1.13 - 2015-10-20

*   [wikitcms-1.13.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.13.tar.gz)

1.  Add tests for sorting and find_bugs() functions
2.  Fix a bug in triplet_unsort() where it would replace bits of dates with strings
3.  **API** drop fedora_release_unsort (it could never work reliably)
4.  **API** drop next_composes (was never used for its intended purpose and is fairly useless)

### 1.12.3 - 2015-09-20

*   [wikitcms-1.12.3.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.12.3.tar.gz)

1.  Have image download table get image description from fedfind instead of producing it here

### 1.12.2 - 2015-09-17

*   [wikitcms-1.12.2.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.12.2.tar.gz)

1.  Refine image download table to use imagesubtype as well as imagetype

### 1.12.1 - 2015-08-29

*   [wikitcms-1.12.1.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.12.1.tar.gz)

1.  **API** (addition) Add an improved release sort helper, triplet_sort
2.  **API** (addition) Add 'unsort' functions - fedora_release_unsort and triplet_unsort
2.  **SECURITY** Protect the eval() used to solve captchas from malicious server admins
3.  Use mwclient page.text() instead of page.edit() (deprecated upstream)

### 1.12 - 2015-06-30

*   [wikitcms-1.12.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.12.tar.gz)

1.  **API**: `listing.TcmsCategory` renamed to `listing.ValidationCategory` (it's unlikely anyone was using this directly)
2.  Added `listing.TestDayCategory` for Test Day category pages
3.  Moved `results_wikitext` property to `Page` class so it is also usable for `TestDayPage`s
4.  Added `result.find_results_by_row()` to facilitate accurate result finding in Test Day pages
5.  Improve page generator handling of Test Day pages
6.  Add `TestDayPage.bugs` property to represent all bugs in a `TestDayPage` (including those not associated with a result)
7.  Maybe other Test Day parsing-related stuff

### 1.11.4 - 2015-04-21

*   [wikitcms-1.11.4.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.11.4.tar.gz)

1.  Add support for new Wikitcms 'bot' feature to mark results from automated test systems: `bot` element added to the tuple used by `wiki.report_validation_results()`, `bot` argument added to `result.Result.__init__()` and `result.find_results()`. No BC break, but older python-wikitcms versions will not correctly parse `{{result` templates that use the bot parameter.

### 1.11.3 - 2015-04-17

*   [wikitcms-1.11.3.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.11.3.tar.gz)

1.  use system `cached_property`, not fedfind bundled one - fedfind's bundled copy was removed

### 1.11.2 - 2015-03-26

*   [wikitcms-1.11.2.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.11.2.tar.gz)

1.  bugfix: fix ResultRow() equivalence check - it was too strict, which broke reporting multiple results to one row in a single `report_validation_results()` / `add_results()` operation

### 1.11.1 - 2015-03-25

*   [wikitcms-1.11.1.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.11.1.tar.gz)

1.  python-wikitcms: handle `milestone=False` and `milestone=None` properly in `get_validation_page()` / `get_validation_event()` - this makes `relval size-check` work without explicitly setting the compose to check (as it's supposed to)

### 1.11 - 2015-03-25

*   [wikitcms-1.11.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.11.tar.gz)

1.  substantial enhancements to result reporting; new `ValidationPage.add_results()` and `Wiki.report_validation_results()` methods allow reporting multiple results in a single operation (with only one wiki edit operation per page), `report_validation_results()` accepts simple tuples and handles instantiation of `ValidationPage`, `ResultRow` and `Result` objects (no API incompatibility, `ValidationPage.add_result()` remains available)
2.  implement equivalence check for `ResultRow` instances
3.  implement caching of `Page.text()` and `Page.sections()` results
4.  add `Page.find_resultrow()`, for finding exactly one result row with specified attributes (moved here from relval report-auto)
5.  `Wiki.__init__()` now defaults to Fedora wiki location if none specified, and `Wiki.login()` now uses credentials file if available and no credentials specified; this allows simple init for editing with just `from wikitcms import Wiki; wiki = Wiki(); wiki.login()` if creds file is available

### 1.10.2 - 2015-02-18

*   [wikitcms-1.10.2.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.10.2.tar.gz)

1.  Make the page object generator handle Branched nightly pages correctly (return a `NightlyPage` not a `ComposePage`)

### 1.10.1 - 2015-02-18

*   [wikitcms-1.10.1.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.10.1.tar.gz)

1.  Restore a refinement to the Rawhide/Branched logic which was lost in the transfer from `relval report-results` to `Wiki.get_validation_event()`

### 1.10 - 2015-02-18

*   [wikitcms-1.10.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.10.tar.gz)

1.  Adjustments for the attempt to consolidate versioning across fedfind, python-wikitcms and relval using `release`, `milestone`, `compose` attributes to identify all images/events
2.  add `Wiki.get_validation_event()` and `Wiki.get_validation_page()` methods which consolidate heuristics for guessing at the desired event/page previously spread across different relval sub-commands and openqa_fedora_tools
3.  multiple bugfixes mostly related to `relval report-auto` and openqa_fedora_tools use

### 1.9 - 2015-02-12

*   [wikitcms-1.9.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.9.tar.gz)

1.  add `Wiki.current_event property` (returns 'current' `ValidationEvent` object)
2.  use abstract base classes to enforce class inheritance in event.py
3.  pylint cleanups to event.py and page.py
4.  add `ff_release` property to `ValidationEvent` classes (the `fedfind.Release` object matching the event)
5.  add `DownloadPage` class for per-event template page of image download links to be transcluded into release validation instructions, and `ValidationEvent.image_table` property to generate its contents
6.  **API** rename `NightlyEvent.tree` attribute to `NightlyEvent.milestone` (for consistency with fedfind and templates)
7.  Sort of rename wikitcms to python-wikitcms (bit half-assed, though)

### 1.8.4 - 2015-01-07

*   [wikitcms-1.8.4.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.8.4.tar.gz)

1.  Fix a bug in page writing (broke any page write which didn't use wikitcms' oldtext/newtext comparison, which is most of them)

### 1.8.3 - 2015-01-02

*   [wikitcms-1.8.3.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.8.3.tar.gz)

1.  Fix result row test case / name detection for cells like `[[QA:Testcase_foo|QA:Testcase_bar]]` (use foo as testcase and bar as name, instead of bar as both)
2.  Note in README that wikitcms data retrieved from wiki should be treated as untrusted input

### 1.8 - 2014-12-22

*   [wikitcms-1.8.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.8.tar.gz)

1.  **API** `matrices` and `testtypes` properties moved from the Event class to the Wiki class, as they are really properties of the wiki, not of a specific event
2.  **API** (minor) `has_bootiso` property moved from NightlyEvent to ValidationEvent as it's valid and potentially useful for all validation events, not just nightlies (should not affect consumers as ValidationEvent is the parent class)
3.  **API** (addition) `compose_exists` property added to ValidationEvent
4.  Protect harder against odd results in `page.results_sections()`

### 1.7 - 2014-12-19

*   [wikitcms-1.7.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.7.tar.gz)

1.  **API** major design overhaul, wikitcms now acts as an extension to mwclient. Too many API changes to list, mainly to Page and Event classes
2.  improvements to page name regexes, now handles more unusual older release page names and F21 monthly pages
3.  adjust to match changed approach to nightly builds in the wiki templates

### 1.6.1 - 2014-12-16

*   [wikitcms-1.6.1.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.6.1.tar.gz)

1.  revert change to `category_walk()` method used when finding result pages, it caused duplicates to show up sometimes
2.  have `ValidationPage.get_resultrows()` strip comments from result text like `results_wikitext` does
3.  fix `ValidationPage` handling of Fedora 12 page name idiosyncracies (broken by 1.6 API change)

### 1.6 - 2014-12-16

*   [wikitcms-1.6.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.6.tar.gz)

1.  **API** Revise nightly compose handling: changes to required arguments for `page.ComposePage` and `event.ComposeEvent`, `from_wikipage` method moves from `page.ComposePage` to new `page.ValidationPage`, introduction of `page.NightlyPage`, `page.ValidationPage` (parent to `ComposePage` and `NightlyPage`), `event.NightlyEvent` and `event.ValidationEvent` (parent to `ComposeEvent` and `NightlyEvent`). New class methods `page.ComposePage.compose_from_wikipage` and `page.NightlyPage.nightly_from_wikipage`. This is a cleaner and more robust approach, and will scale to other types of compose if necessary
2.  `ValidationPage` from_wikipage methods now check if wikipage exists (returning None if not) before doing anything else

### 1.5 - 2014-12-08

*   [wikitcms-1.5.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.5.tar.gz)

1.  Support for nightly build testing

### 1.4.1 - 2014-10-31

*   [wikitcms-1.4.1.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.4.1.tar.gz)

1.  wikitcms now requires python-mwclient 0.7 (result reporting messes up result pages with 0.6.5)
2.  Fix URL in bug report links in testcase-stats detail pages

### 1.4 - 2014-10-25

*   [wikitcms-1.4.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.4.tar.gz)

1.  Refactored result parsing to be less tied to wiki text parsing and more extensible
2.  Small improvements to display of things like section names and environments in relval (produced by better parsing in wikitcms)

### 1.3.1 - 2014-10-24

*   [wikitcms-1.3.1.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.3.1.tar.gz)

1.  Add a string representation of Result objects (relval report-results uses this to display existing results)

### 1.3 - 2014-10-21

*   [wikitcms-1.3.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.3.tar.gz)

1.  Various tweaks in wikitcms to make result submission viable, including overhaul of section parsing / handling
2.  helpers.next_compose() to find the likely candidates for the next compose after any given current one
3.  A few bug fixes

### 1.2 - 2014-10-16

*   [wikitcms-1.2.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.2.tar.gz)

1.  fix walk_category() not to return duplicates
2.  strip comment blocks from results wikitext
3.  track numeric index of sections when parsing result rows

### 1.1 - 2014-10-14

*   [wikitcms-1.1.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.1.tar.gz)

1.  Parsing of existing test result pages in wikitcms
2.  Added the 'Release' class to wikitcms, providing properties of releases
3.  Allow finding ComposePage object from mwclient page object, and ComposeEvent from ComposePage
4.  Added a helper function for doing Fedora release order sorting, and gave ComposeEvent and ComposePage objects a 'sortname' property

### 1.0 - 2014-10-06

*   [wikitcms-1.0.tar.gz](https://files.pythonhosted.org/packages/source/w/wikitcms/wikitcms-1.0.tar.gz)

1.  Initial release
2.  Supports writing individual result pages and summary pages, correctly handling category membership and category page content, and optionally updating Current redirect pages, for TC and RC builds
