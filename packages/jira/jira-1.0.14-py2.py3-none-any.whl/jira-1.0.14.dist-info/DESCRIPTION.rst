===================
JIRA Python Library
===================

.. image:: https://img.shields.io/pypi/v/jira.svg
        :target: https://pypi.python.org/pypi/jira/

.. image:: https://img.shields.io/pypi/l/jira.svg
        :target: https://pypi.python.org/pypi/jira/

.. image:: https://img.shields.io/pypi/wheel/jira.svg
        :target: https://pypi.python.org/pypi/jira/

.. image:: https://img.shields.io/codeclimate/issues/github/pycontribs/jira.svg
        :target: https://github.com/pycontribs/jira/issues

------------

.. image:: https://readthedocs.org/projects/jira/badge/?version=master
        :target: http://jira.readthedocs.io

.. image:: https://api.travis-ci.org/pycontribs/jira.svg?branch=master
        :target: https://travis-ci.org/pycontribs/jira

.. image:: https://codecov.io/gh/pycontribs/jira/branch/develop/graph/badge.svg
        :target: https://codecov.io/gh/pycontribs/jira

.. image:: https://img.shields.io/bountysource/team/pycontribs/activity.svg
        :target: https://www.bountysource.com/teams/pycontribs/issues?tracker_ids=3650997

.. image:: https://requires.io/github/pycontribs/jira/requirements.svg?branch=master
        :target: https://requires.io/github/pycontribs/jira/requirements/?branch=master
        :alt: Requirements Status


This library eases the use of the JIRA REST API from Python and it has been used in production for years.

As this is an open-source project that is community maintained, do not be surprised if some bugs or features are not implemented quickly enough. You are always welcomed to use BountySource_ to motivate others to help.

.. _BountySource: https://www.bountysource.com/teams/pycontribs/issues?tracker_ids=3650997


Quickstart
----------

Feeling impatient? I like your style.

.. code-block:: python

        from jira import JIRA

        jira = JIRA('https://jira.atlassian.com')

        issue = jira.issue('JRA-9')
        print issue.fields.project.key             # 'JRA'
        print issue.fields.issuetype.name          # 'New Feature'
        print issue.fields.reporter.displayName    # 'Mike Cannon-Brookes [Atlassian]'


Installation
------------

Download and install using ``pip install jira`` or ``easy_install jira``

You can also try ``pip install --user --upgrade jira`` which will install or
upgrade jira to your user directory. Or maybe you ARE using a virtualenv_
right?

By default only the basic library dependencies are installed, so if you want
to use the ``cli`` tool or other optional dependencies do perform a full
installation using ``pip install jira[opt,cli,testing]``

.. _virtualenv: http://www.virtualenv.org/en/latest/index.html


Usage
-----

See the documentation_ for full details.

.. _documentation: http://jira.readthedocs.org/en/latest/


Development
-----------

Development takes place on GitHub_, where the git-flow_ branch structure is used:

* ``master`` - contains the latest released code.
* ``develop`` - (default branch) is used for development of the next release.
* ``feature/XXX`` - feature branches are used for development of new features before they are merged to ``develop``.

.. _GitHub: https://github.com/pycontribs/jira
.. _git-flow: http://nvie.com/posts/a-successful-git-branching-model/


Credits
-------

In additions to all the contributors we would like to thank to these companies:

* Atlassian_ for developing such a powerful issue tracker and for providing a free on-demand JIRA_ instance that we can use for continuous integration testing.
* JetBrains_ for providing us with free licenses of PyCharm_
* Travis_ for hosting our continuous integration
* Navicat_ for providing us free licenses of their powerful database client GUI tools.

.. _Atlassian: https://www.atlassian.com/
.. _JIRA: https://pycontribs.atlassian.net
.. _JetBrains: http://www.jetbrains.com
.. _PyCharm: http://www.jetbrains.com/pycharm/
.. _Travis: https://travis-ci.org/
.. _navicat: https://www.navicat.com/

.. image:: https://raw.githubusercontent.com/pycontribs/resources/master/logos/x32/logo-atlassian.png
   :target: http://www.atlassian.com

.. image:: https://raw.githubusercontent.com/pycontribs/resources/master/logos/x32/logo-pycharm.png
    :target: http://www.jetbrains.com/

.. image:: https://raw.githubusercontent.com/pycontribs/resources/master/logos/x32/logo-navicat.png
    :target: http://www.navicat.com/

CHANGES
=======

1.0.13
------

* Fix README.rst images

1.0.12
------

* Fix setup.cfg: UnicodeDecodeError
* Add pbr >= 3.0.0 as a module dependency
* Fix build scripts
* jirashell: Import InteractiveShellEmbed depending on IPython version
* Make OPTIONAL default and allowed value of mutual\_authentication
* Add testing section to contributions
* Update Contribution Guidlines to be more explicit
* Place imports on separate lines
* Touch ChangeLog To Fix PR Checks
* Fix Continuous Integration Testing
* Make Kerberos option mutual\_authentication configurable
* Accept custom authentication URL
* fixed linting errors
* Update client.py
* Allow through TRAVIS Environment Variables
* Add worklog to transition\_issue()
* Fixing move\_to\_backlog()
* Fix bug
* [client] Support JIRA.close()
* add add\_user to role resource
* added .idea/codeStyleSettings.xml to repo
* contributing.rst: Update JIRA community link
* contributing.rst: Remove reference to BitBucket
* Include changelog in description
* Move requirements extras to setup.cfg
*  #361 Made ipython a direct dependency
* build logic and code cleanup
* Fixed github deploy credentials
* linting fixes
* Forcing a rebuild
* Pass integer ids when creating customer requests
* Skip Service Desk tests on instances that don't support it
* Pass ids when creating a customer request
* Create Service Desk project during testing if it is missing
* Add a test for create\_customer\_request
* PEP-8 H306
* PEP-8 H301
* PEP-8
* Add supports\_service\_desk check
* Only add Service Desk properties if is\_internal is set
* allow to define internal comments in service desk
* Allow service desk parameter to be an integer
* Explicitly import resources
* Add support for customer, request\_type and create\_customer\_requests
* Flake8 cleanup
* Update examples.rst
* Update examples.rst
* Fixed github deploy credentials

1.0.10
------

* Added back the jirashell command line entry point
* Fixed version shield in readme

1.0.9
-----

* Fixed missing .egg\_base in source distribution
* Enabled codecov.io and hidden coveralls.io
* Fixed missing .egg\_base in source distribution
* Enabled codecov.io and hidden coveralls.io

1.0.8
-----

* travis.yml cleanup
* Printing the version
* Enabled builds on all branches
* Removed hardcoded version from setup.cfg
* tests: made project re-creation less likely to fail
* Changed delete version to return json response
* Added 401 return code to retriable ones due to Atlassian Cloud weird responses
* Fixed travis config as travis-after-all is now embeded into tox-travis
* tests: made fixtures and tests less likely to fail
* Enabled py36 for Travis
* tests: marked test\_delete\_project as xfail
* api: add\_user\_to\_group can now return False on failures
* Enabled py36 target on travis
* Adopted used of tox-travis
* tests: marking test\_add\_user\_to\_group as xfail to unexpected API response
* tests: kill\_websudo to be ignored on cloud deployment
* Enabled @flaky for all test classes
* Addressed flaky Travis parallel test execution by adding a retry mechanism
* linting fixes
* Enabled flakey for problematic tests
* travis concurrency fixes
* Improved travis build stability
* properly import input function from six. see #316
* Allows users to specify timeouts for underlying requests session
* Design fixes for bulk create support
* Support for bulk issue creation
* Add support for delete\_attachment
* When search\_issues() should return json maxResults is ignored
* Fix JIRA(validate=True) option, issue #300
* README: Fix formatting and tweak wording of the Development section
* Fixed #256 - documented branches
* Fix for issue #294 - Can't fetch all sprints
* jira cloud has migrated attachments to a more restrictive to a persnickety web service that demands correct Accept headers.  It currently return a HTTP 406 error.  This change resolves the issue
* Removing deprecated Agile-related methods
* Do not fail when a searched issue has no fields
* Adopted pbr and hacking
* Small typo fix in incompleted\_issues method
* Resize images in README.rst
* Fixed Citrix Logo image URL
* Job id prefix (jid) is now using travis numbers, shoudl work for PRs too

1.0.7
-----

* Fixed test execution
* Fix sphinx documentation not rendered correctly
* flake8 fix for FileNotFoundError and added gitreview file
* Use context processor for opening files
* made kerberos mutual auth optional as not all servers support this
* We shouldn't create files unless we're told to do so
* params object for \_fetch\_pages should not contain maxResults
* Removed tlslite requirement completly
* Temporarly removed gitchangelog and enabled s3 upload of artefacts
* tried to preinstall requirements on travis
* Downgrated wheel version requirement
* Fixed detection of package name and version for Travis
* Updated requirements
* Adding a test for #214
* Fixes #214
* Moved more build logic into Makefile
* Removed partial init of JiraTestManager as this breaks a lot of tests
* Added named parameter to skip test project creation
* Fixed delete\_project and added tests for it
* removed cloud options from backup methods in favor of checking for deploymentType in server\_info.  Also made backup\_download a bit more efficient by using streaming.  Fixes Issue #234
* removed cloud options from backup methods in favor of checking for deploymentType in server\_info.  Also made backup\_download a bit more efficient by using streaming
* Configured to use autopep8 as a module in order to work with venvs
* Removed Python 2.6
* Assured that we use stdout/stderr capture and a flake8 fix
* add ability to use request session proxy functionality
* Do not check for a newer version of the software by default
* Change http://pypi.python.org to https://pypi.python.org
* Fixes to get 'python setup.py develop' working
* Do not use Make for running tests, seems to cause timeout
* Fix mock data setup
* Fix tox errors for py2.7
* Improve auto-generated changelog
* Resolves issue #221, 'Allow for deactivating users'
* Added template\_name parameter to create\_project to be able to specify template directly, and fix issues where function cannot find suitable project name
* Fix #194 Exception AttributeError: "'NoneType' object has no attribute 'version\_info'"
* Delete Issue Link Bug Fix
* Fix #157
* Add documentation for attachments
* Add documentation for watchers
* Added docset building to the documentation build
* Adopted django versioning implementaion
* Added virtualenv usage to Makefile
* Sorted the project name duplication error with the tests
* Simplified setup Exception code in tests
* Attempt to keep py26 compatibility
* Log JiraError details on console for Travis
* Removed requests-kerberos requirements as it was breaking docs
* Fixed assert in test\_search\_users\_maxresults
* updated and moved requirements into one place
* ci maintenance
* Added requires.io badge
* Resolved #137 by removing the check for project key from the client app
* Update index.rst
* Switched to local travis\_after\_all.py
* flake8 fixes
* travis: Remove \`on\` inside afte\_deploy as is not supported
* Fixed two broken tests and many other warnings
* Attempt to fix travis publishing and the missing URLs for the uploaded releases. Also should start uploading dev release to pypitest
* Allows us to call delete\_project() with Project object instance
* Experimental change for testing error handling
* Fixed linting and enabled build of develop branch pn travis
* Switched to smart versioning for develop branch
* Fix #170 : use default 'hidden' email address when Jira server setting for showing email is hidden
* Added docs badge
* Make the sections numbered again
* Add section headers for each class in the API docs
* Split up documentation into multiple pages
* flake8 fixes (lots)
* Adds move\_to\_backlog from the agile API
* add missing issues report methods
* used to get xml in response to backup progress, now getting json
* added functionality for backing up from Cloud version
* Auto-generating release notes
* Auto-generating release notes
* Auto-generating release notes
* Tried to make release 1.0.6
* Improved release.sh

1.0.5
-----

* Auto-generating release notes

1.0.4
-----

* Auto-generating release notes
* Auto-generating release notes
* Auto-generating release notes
* Auto-generating release notes
* Auto-generating release notes
* Auto-generating release notes
* Auto-generating release notes
* Auto-generating release notes
* remove wrong parameter in release.sh
* test rsa key
* Changed linkId to id for consistency
* Correcting tabs vs spaces
* Adding functionality to allow deletion of issue links
* Adds support for Kerberos auth
* Updated PyCharm logo as they also removed the old one when they rebranded it
* Configured minimal versions for pep8 related packages
* fixed the version check for invalid request
* Logged the initial JSON response for templates when they do not contain the expected format. This should help us identify what happens while running tests on Travis
* changed api version calls to use "latest" instead of 2
* resolves issue where incompleted\_issues() was failing for missing key; 'incompletedIssues' corrected to 'issuesNotCompletedInCurrentSprint'
* Should fix the inconsistent failures with watchers tests
* Swiched back to the use of logging module directly instead of a variable
* Implemented a special retry mechanism for serverInfo REST call in order to workaround bug https://jira.atlassian.com/browse/JRA-59676
* Repaired delete\_project() as it seems not to be working on JIRA 6.x
* Fixed few others broken unittests
* Reworked the way we log warnings and errors, now we use the named logger "jira"
* Removed duplicate python versions from setup.py
* Removed pypi version badge as is useless
* More unittest fixes, now they should finally pass after months of having many of them broken
* Implemented \_\_eq\_\_ for Version resource
* Fixed many of the broken unittests. Disabled some uneeded logging for running unittests
* Badge cleanup
* Request JSON payloads to avoid the problem described in https://jira.atlassian.com/browse/JRA-38551
* assign\_issue() now returns errors
* Linting plus initial work on enabling local testing using the atlassian-sdk
* (Minor) Fix UniversalResourceTests.test\_pickling\_resource() - Work with the raw dict instead of pickling the whole resource and running into issues with PropertyHolder
* (#158) Fix initialisation of resources.Issue when raw is passed in
* Fix conflict markers from merge
* clean up string detection: string\_types
* remove superfluous self parameter
* Exclude tests working with users - not understood why they fail now
* Skip tests that rely on specifics of the standard Jira if a non-standard Jira is used
* Add correct treatment of "issuetype" parameter
* Fix whitespace and allow for python3
* Fix call of Resource.\_get\_url()
* Adapt project template search to new structure
* Fixed problems found during tests execution
* Fixed bugs found in new JIRA API
* Added option for ignoring existing users on user\_add
* Add new option 'agile\_rest\_path', which may be used to select new public JIRA Agile API
* Small improvements
* Added JIRA.\_fetch\_pages function and used it in all functions using pagination and extended ResultList class
* bump version
* cover python 3.5
* py3 compatible string test
* redundant if test in split
* test for clauseNames presence
* items for py3 compat
* Added type hints to Issue class
* Update release.sh
* Fix setup.py's setup\_requires and requirements.txt
* Move optional filemagic line to requirements-opt
* Do not try to recover if we're not going to do the retry
* Do not run prerelease as part of the standard test run. Instead run it after inside after\_success
* Restore missing delay in ResilientClient and & implement exponentional backoff
* gh-global-rank field is obsolete
* Ensure JIRA class has \_rank field

1.0.3
-----

* Fix #93: ability to retrieve custom fields by their JQL names
* Websudo fix when used with .netrc files
* Added support for the type parameter on create\_project, as this is required for JIRA 7
* Moved JIRAError to exceptions
* moved raise\_on\_error to resilientsession
* documentation improvements, fixed one test
* fixed #123 by enabling change of sprint state
* removed dead code
* HOTFIX in test; pass two elements into set properly
* Fix typo
* Add \_\_hash\_\_ and \_\_eq\_\_ methods to User class to allow user objects to be added to a Set correctly
* Fixup: Correctly cope with Requests object truthiness..
* Bugfixes for ResilientSession retry logic
* Issue 118 Add ability to send email notification when creating a new user
* Python > 3.1 do not need \`ordereddict\` package
* Change test to use simple regex
* Update self.issue\_1.key to self.issue\_1
* Update test and assert to use arrays
* Fix typo with assigning false boolean
* Add unit test for adding issue to sprint
* Refactor method of retrieving custom field info
* Issue 112 - sendEmail kwarg doesn't work when calling add\_user method
* Fix typo in list comprehension
* Perform dynamic lookup of custom field id for Sprint field
* Fix typo with assignment
* Workaround for adding an issue to a sprint
* Minor fixes to jirashell issues #100, #102, and #66, and tweaks fix from d5856742771890ad18165197f6bc7eb3ff8cd086. The oauth\_dance and print\_tokens options specified in jirashell.ini configuration file are now correctly parsed as boolean values and OAuth with pre-authenticated access\_token and access\_token\_secret (skipping oauth\_dance) is fixed. OAuth options are now minimally validated for completeness, so #66 is fixed, allowing for basic\_auth without causing issue #102 as the merged commit d5856742771890ad18165197f6bc7eb3ff8cd086 did previously
* Fixed #88 so now groups are returned as a sorted list of strings
* Fix issue #100 - The problem is that 'oauth\_dance' should be an optional option argument, if it is not set, or if it is set to false, a valid use case still exists where OAuth should be used if the user supplies access\_token and access\_token\_secret through command line or configuration file options. This would be the case if the user had already authenticated externally with OAuth and had valid, authenticated tokens to pass to jirashell

1.0.1
-----

* Attempt to fully automate the release and tagging of git based on what is released
* Attempt to fully automate the release and tagging of git based on what is released

0.50
----

* Enabled new travis builders as we do not need sudo. Fixed iteritems() which doesn't work anymore with py34. Increased version to v0.50

0.49
----

* Attempt to fix the unittest and to eliminate warnings from the test executions
* Make \`python setup.py test\` work without first needing to install any dependencies
* Fill in the current maintainer information
* Add update\_filter to client
* Fix jirashell.py for non-oauth authentication
* Honor fullname arg in add\_user
* Fix JIRAError to correctly include full details
* JIRA Issue 80 - delete project fails to delete
* Includes are now relative to jira package
* Added myself AIP support
* JWT authentitcation support for Atlassian Connect
* Fixed naming error in the documentation
* adding add\_simple\_link()
* Add attachment content streaming
* jirashell configured via jirashell.ini didn't allow no-oauth authentication
* Add support to Issue.update to use the update key, and make some common forms of updates easier
* Don't always set oauth flag, to prevent oauth mode from always being enabled, even if basic auth is requested
* Minor change to cause a new build to be triggered

0.48.1
------

* Bumping patch version number to 0.48.1
* Do not prevent users from adding remote links if we are not able to fetch applicationlinks
* Now travis should publish both sdist and wheel. Also included changelist

0.48
----

* Attempt to appease Travis
* Restore issue transitions by fixing some flubs

0.47
----

* increaded version to 0.47
* Implemented worklog tests and fixed worklog and timetracking
* Fixed mimetype issue with Jira attachment. MultipartEncoder sent attachment in 'text/plain' mode which caused issues with pdf files. See images 3 images from images directory, after the change, mimetype was identified correctly
* Now Travis should release only if all jobs do succeed
* sorted the decoding of the json response
* Increased version number to v0.45 but in the future this should be done automatically on each release
* Minor Travis fix for py3 build
* removed the pretest phase as now everyone should be able to run the tests
* Implemented a prerelease stage that will prevent running the tests on travis for already released versions. This is needed in order to enable future automatic releases
* Fix for #28 : broken permalinks
* Removed the secured credentials from Travis because they do not work with pull requests. See http://docs.travis-ci.com/user/pull-requests/ From now on everybody should be able to run the tests, lets hope that the OnDemand server will be able to cope with the tests
* validated .travis.yml
* fix #38 so the code will also work with PyInstaller
* Workaround for py34 weakref issue from https://github.com/kennethreitz/requests/issues/2303
* Added Citrix to credits, changed default documentation theme and documented the BountySource usage
* Bugfix in Travis config file which seems not to fail fast on multiple script commands
* fix atlassian header

0.43
----

* v0.43 release which fixes pickle bug
* #46 Experimental drop of custom getstate/setstate in Resource that was preventing Pickle from restoring the objects properly (\_options)
* Added sdist to release

0.42
----

* commented \`git add RELEASE\`
* v0.42 minor fix regarding release script tagging
* Added flattr button
* Allow OAuth dance to ignore ssl certificate
* v0.41 that enabled new unitises and fixes #44
* Comment: fix typo in comment 'visibility' name
* v0.40 - new release with small bug fixes
* Added an exception in case the just added attachment has size=0 so we can debug the weird case of empty attachments
* marked the pickle test as xfail and some pep8
* Finished initial baseline label test. Added test for issue #32 that looks for an exception from a bad label with spaces
* Added initial label unit test
* Update client.py
* Update client.py
* no need to take the tuple lookup hit with one item
* make it more clear about what we're doing to support pickling
* add tests for pickling resources
* enabling the pickling of resources
* v0.39: minor bug fixings
* fixing #23 bug: startDate in create\_version()
* Update client.py
* Raise an AttributeError if a requested attribute doesn't exist within self or self.raw. This is a bug fix to ensure calls to hasattr return false when the attribute doesn't exist
* Issue add\_field\_value should use Resource update function
* Corrected source URL inside the documentation
* Updated the link to documentation
* removed upload\_sphinx from release
* v0.38 which should work well on intranets
* Now the version check should take up to 2 seconds and should not prevent loading if it fails
* Update index.rst
* v0.37 release
* fixed error with last merge
* removed a test that is not needed anymore
* Repaired 3 additional tests
* added the first tests for JIRA Agile. Also this should fix the Issue.update()
* Give users ability to disable update check
* Deprecated GreenHopper class and moved all methors into JIRA. Other plugins should use the mixin pattern to add their methods
* allowing to pass Issue() instances instead of id/keys to issue()
* Optimized the check\_update code so it checks version only once. Fixed the comments tests
* py26 and py3 compatibility updates
* Changed the way we load the version in setup.py in order to properly perform coverage. Also added fallback on add\_attachment for the case where we do not have the filestreamer module
* added ordereddict dependency that is required for py26 compatibility improved the random password complexity to avoid falure from server side
* changed number of retries to 5 unless jira is running on localhost, when it will use 1
* pep8
* - Added tests to flesh out User and Group CRUD operations. - Added add\_group method to client. - Added remove\_group method to client. - Rewrote add\_user\_to\_group to use REST API - Added remove\_user\_from\_group to client
* fix resource \_load incorrect argument
* This should fix UserAdministrationTests and make them run on Travis too
* - Created unit test class for user administration - Created add\_user unit test
* Attempt to improve the retry mechanism. Will default to 3 for normal usage and 10 for running the tests
* reworked tests of votes so they should not randomly fail anymore
* Fixed failure of add\_attachment test when using retry was triggered. This was caused by the file stream. Now it will get a new file stream if the initial post fails
* fixed create\_issue() which was broken due to project being passed wrongly
* Increased verbosity in order to debug some CI failings
* Updated tests to prevent failure to upload attachment with Python 3
* Fix ResourceLeak warning with CPython3
* Now HTTP codes 502,503,504 do retry
* Configured default max\_retries to 3
* Fixed add\_attachments which now is able to stream the files, preventing size limitation bugs
* improved tests
* improved tests
* Added a new test for failed authentication Made test\_attachment more verbose Added export of coverage data into xml format
* README.rst: Double back quotes, fix links
* README.rst: Make valid on PyPI
* README.rst: syntax highlighting
* Implemented travis\_after\_all so we release only once
* Test changes towards getting them passing on Travis too
* additional travis compatibility changes
* additional travis compatibility changes
* additional travis compatibility changes
* additional travis compatibility changes
* disabled xdist plugin in order to execute on travis
* Major changes to unittests in order to make them pass on Travis
* Added new icons to README page
* autopep8
* Added upload\_docs and switch to usage of default GPG signature
* Merged in taquart/jira-python/taquart/fixing-the-commentupdate-example-1420064736261 (pull request #73)
* Merged in rowanthorpe/jira-python/fix-configparser-to-match-v3-import (pull request #71)
* Merged in evers/jira-python (pull request #72)
* Merged in franciscoruiz/jira-python/franciscoruiz/removed-print-statement-from-greenhopper-1417788172609 (pull request #69)
* Merged in mejoe/jira-python/completed\_points (pull request #68)
* Merged in simonventuri/jira-python/yosemite-six-fix (pull request #66)
* added wheel deployment

0.33
----

* Removal of gevents as it is incompatible with Python 2.7.8 and because we can use requests threading for the same purpose
* Fixing the comment.update() example
* fix issue.add\_field\_value, fixes #144
* dont forget raise\_on\_error if not autofixing
* Fix configparser usage to match v3-compat import
* Removed 'print' statement from Greenhopper.sprints\_by\_name
* Add sum of completed issues for a board/sprint
* Merged in misa/jira-python (pull request #62)
* Merged in rmelhem/jira-python (pull request #67)
* Implemented username rename for JIRA 6.0.0+
* Added support for client-side SSL with HTTP-Basic session
* Fix html\_parser import from six.moves
* navicat does not have https (sic!) :)
* Updated image links
* Updated Navicat Logo
* Update README.rst
* Update README.rst
* Merged in bunkerbewohner/jira-python (pull request #63)
* bugfix of KeyError in JIRA.add\_remote\_link during check of application links
* fixes #2
* Add a fields keyword arg; regular keyword arguments will take precedence
* Reverting commit 5f4c4a4, added an update method for Comment for fix #53
* Merged in rawfalafel/jira-python/fix/validate-search-query (pull request #61)

0.32
----

* v0.32 is fixing #132 decoding errors on several cases, cased by the wrong usage of response.content instead of response.text, first one being binary
* fixing #53 Unable to update a comment
* Fix for #112 : added startDate, released and archived to create\_version()
* Fixed #96 by documenting how to update components
* Fixing #81 by removing requests\_oauth from the package
* Fixing #61 - documenting how to get support on jira-python
* Assured that RELEASE file that contains the changelog is updated when making new releases

0.31
----

* Added automatic release note creation
* Fixed #101 - added back python 2.6 compatibility
* Fixed issue #94 jirashell being broken. Moved jirashell.py inside jira package, tools was clearly not an inspired name for a package
* Merged in tomikall/jira-python (pull request #60)
* Fix process\_config() to work with configparser from six and Python 3
* Fix #130 : Read options \`verify\`, \`resilient\`, and \`async\` as booleans from user's \`jirashell.ini\` file
* Add option to disable query validation. Part of the REST api
* pep8 tests still not working
* pep8 moved to setup.cfg few other fixes, should pass pep8 now
* v0.31 merge with bitbcket copy
* v0.31 manual merge with github fork (used to revive unittests)

0.30
----

* v0.30 containing a real fix for JIRA.\_\_init\_\_()

0.28
----

* v0.28 fast-track merge of latest patches
* Merged in xistence/jira-python/bugfix/future\_imports (pull request #59)
* Merged in xistence/jira-python/bugfix/jira.issues (pull request #58)
* removed pep8 from test cases
* pep8 work + forced py.test to run on single thread
* all the tests are now generic
* run tests from UserTests
* run job only with the class SearchTests
* Move from \_\_future\_\_ import statement
* Remove erroneous self
* added a few tests from ProjectTests
* generalised a few other tests
* another run
* add\_worklog does not work for python2.6
* one more run
* run again without IssuesTests
* added general tests for IssueTests
* tests for travis
* general tests for filters
* some changes for general projects
* probably fixing CI with jenkins
* added travis\_wait
* all working for python2.7 (for the moment)
* Updated tests for the new added projects
* pep8 + added py34 in addition to py33, one of them must be tested
* made autopep8 optional
* removed --upgrade from pip install
* reorganized requirements, hoping to make the test easier and also to reduce dependencies for installations
* added timeouts to curl, should fix the travis issue, hopefully
* removed -n4 from tox until we find a solution for working with fixtures with multiple threads, seems to be a design limitation with py.test
* added all the tests appart from 3 for which I don't have enough permissions and those from remote\_link
* added tests from VersionTests
* Added tests from UserTests
* added tests from ProjectTests
* added 3 new classes
* Tests from Issue tests are now working
* Fixed some other test cases
* Other 15 test cases are working
* tests for classes ResourceTest and ApplicationPropertiesTest are now working
* ZZF-15731 #comment this should end-up in jira
* some working tests from UniversalResourceTests
* Fix for test\_issue\_link(self) faild build #18.3
* fixed test\_issue\_link()
* tests cleanup, enabled py34 in travis, added pretest before running tests
* Updated user prefix
* logging improvement, corrected doc build via tox, probably fixed a deadlock with running unittests in parallel
* logging improvement, corrected doc build via tox, probably fixed a deadlock with running unittests in parallel
* fixed typo in nocheck -> no-check
* removed logging and fixed the test manager class
* added debug code for Travis failure as we were not able to replicate same failure locally
* Disabled kill session for the moment as it seems to cause some strange errors with unittests
* Added logging of fatal exceptions when initializing unit tests
* repairing unittests
* repaired project create
* Merged in abstracttype/jira-python/abstracttype/fix-greenhopperincompleted\_issues-base\_-1404297141573 (pull request #57)
* v0.29 added delete\_board()
* fixed broken images
* CI enablement work
* Added creatation time to log\_work, documented accetable values for assign\_issue, converted few prints to use the logger
* Update README
* v0.28 fixed critial bug related tu unicode support (type(str(..))) and initial work for enabling continous-integration with Travis and the Atlassian provided on-demand JIRA test instance
* Fix \`GreenHopper.incompleted\_issues\` - BASE\_URL was previously used as the \`params\` argument
* fixed typo in filename
* added tox, pep8 and autopep8 as requirements
* added travis config file
* Initial implementation of update\_sprint() which can alter start and end dates
* Partial fix for #116 : unicode errors
* flush async queue on delete
* Improved async support
* Re-enabling async support, now you can enable it by adding async=True when you create the JIRA object
* Merged in johnjiang/jira-python/fix-add-remote-link (pull request #56)
* Fix for instances where destination is NOT an issue but just a normal dict

0.25
----

* documented usage of add\_remote\_link()
* v0.25 fixing #34 : add\_remote\_link should be able to receive remote issue instances as parameter
* fixing #108 : jira \_\_init\_\_ kills version() method
* v0.24 fixing #107 by killing sessions inside the destructor

0.23
----

* v0.23 fixing the broken search
* Partial fix #46 now waiting for Atlassian to fix their side
* Fixed #106
* Merged in rentouch/jira-python/fixed\_get\_json\_params (pull request #55)
* Fix function calls which are using the "param" argument on the function \_get\_json(), as param isn't the second argument anymore since the "base" arg was added in eb8be46

0.22
----

* #104: added connection errors as recoverable errors: DNS resolve issues, connection refused
* pep8 reformatting
* #104 :retry mechanism. add resilient=True to the server options and it will retry failed requests
* Merged in SimplicityGuy/jira-python-fixes (pull request #51)
* Merged in chiemseesurfer/jira-python (pull request #53)
* Merged in jvtrigueros/jira-python/basic-auth-using-post (pull request #54)
* Fixing code formatting as per request
* add update to Version class to archive versions
* Merged in jvtrigueros/jira-python/basic-auth-using-post (pull request #52)
* When using Basic Authentication, use a POST request
* Merged in jaimesoriano/jira-python/trust-requests-proxy-selection (pull request #50)
* Merged bspeakmon/jira-python into master
* Fixed the last few issues of the GreeHopperResource usage
* Fixing issue where GreenHopper was using JIRA's API URL through \_get\_url
* Minor comment cleanup and addition of GreenHopper resources to resource\_class\_map
* Merged in SimplicityGuy/jira-python-fixes (pull request #49)
* Moving GreenHopper over to use GreenHopperResource, updating comments, and fixing a few TODOs
* Trust proxy selection provided by requests by default
* Minor cleanup
* Missed part of that checkin
* Merged bspeakmon/jira-python into master
* Fixing issue where importing print\_ from six tried to override the built in print. This does not work. So, fixed up existing print usage to avoid having to import print\_
* Fixed two import bugs introduced by previous commit
* Merged bspeakmon/jira-python into master
* Merged in platinummonkey/jira-python (pull request #45)
* added six as a dependency fro py2-py3 compatibility
* Merged in freeseacher/jira-python (pull request #44)
* Merged in guyroz/jira-python (pull request #46)
* Merged in SimplicityGuy/jira-python-fixes (pull request #47)
* Fixed issue with deprecated IPython usage
* Fixed issue #93, missing newline @ line 29
* move sphinx to test\_requre from setup\_requires
* PEP8 Compliance and fixed Python3 support utilizing the \`six\` library
* Merged in freeseacher/allow-request-full-search-result-1392721783002 (pull request #1)
* allow request full search result. for work with it like with simple dict

0.21
----

* removed tendo as a dependency
* Minor fixes needed for continous-integration
* v0.21 adding experimental support for iDalko Grid
* fixed release so it does force change of tags instead of failing to push them at the end of the release process

0.20
----

* release v0.20 minor bug fixing mainly, but should fix some pip install failures
* Fixing incompatibility between ipython and geven modules
* Merged in scott\_weintraub/jira-python (pull request #40)
* Merged in davidszotten/jira-python/fix\_setup\_requires (pull request #41)
* Merged in db\_atlass/jira-python/fix\_random (pull request #42)
* Merged in jdelic/jira-python/feature/output-auth-url-if-printtokens (pull request #43)
* Output auth\_url instead of opening a webbrowser when the user opted to print the tokens

0.19
----

* v0.19 Added get() method that returns attachment content
* Use SystemRandom where it is available instead of random
* remove \`requests\_oauthlib\` from \`setup\_requires\`
* Added create\_filter(name = None, description = None,                     jql = None, favourite = None)
* Merged in il\_bale/jira-python (pull request #39)
* Add configuration parameter to enable/disable SSL certificate verification
* Merged in nyetsche/jira-python (pull request #36)

0.18
----

* Enabled search\_issues() to return all issues by setting maxResults=None
* Merged in pnichols104/jira-python (pull request #38)
* fixed bug in add\_user\_to\_group where find statement always evaluates as True

0.17
----

* Release 0.17 : added support for comments in work logs
* Merged in fpierfed/jira-python (pull request #37)
* Added ability to specify a comment text in creating a worklog item
* Updated README to use the new package name
* add maxResults option to groups()

0.16
----

* Renamed the pypi product to jira from jira-python so it does match the package name
* Configured to use newer xmlrunner that exports the main class properly
* added requitements.txt for prepering the test execution
* Increased memory for test instance, enabled JMX RMI so we can debug it if needed
* switched to the renamed xmlrunner, which is patched and under our control
* Prevented tools from being included into the distribution in order to prevent polution of package namespace. jirashell is for the moment not distributed until we decide where we are going to put it
* Removed the tests from sdist, not not poluting module namespace anymore
* Various Python 2.6-3.3 compatibility fixes
* Release 0.16 adds LICENSE file to archive, optional login verification on instantiation
* added license file to the packaged distribution
* added optional parameter validate to the constructor that will validate your credential at instantiation time, solving #37
* removed typo in group\_members()
* Added group\_members() method
* Merged in aliles/jira-python (pull request #35)
* Fix warning for implicit close of libmagic

0.15
----

* Added release script and increased version to 0.15
* Implemented add\_user\_to\_group() and changed the initialization of unitests so it will test if a jira instance is running on 2990 and start it if necessary. Unit tests still failing with ~90/160, but that’s much better than the previous 100% failure
* Removed distributed option (-n4) form py.test config so it can run even without xdist
* Added test configs
* Added ability to auto-start jira test instance from unittests if it is not already running
* updated test command to install tox and autopep8 if needed
* pep8 fixes
* Merged in nferch/jira-python (pull request #34)
* 2nd fix for broken py26 due to sys.version
* fixed broken py26 due to sys.version
* support Python <= 2.6 sys.version\_info
* Executed autopep8, now part of the test execution
* Merged in jonromero/jira-python/jonromero/fixes-httpsbitbucketorgbspeakmonjirapyth-1380256994854 (pull request #33)
* Merged in alectolytic/jira-python/py3 (pull request #32)
* Real implementation or delete\_user()
* Implemented delete\_user()
* Implemented add\_user()
* [Issue #55] Additional changes for python3 support
* Basic Python 3 port
* Implemented create\_project() and delete\_project() - tested only on Jira 5.2.11
* Added rank() method for GreenHopper class, which now allows you to rank one issue before another
* Merged in jonromero/jira-python-2/jonromero/typo-1381168098819 (pull request #2)
* typo
* Merged in jonromero/jira-python-1/jonromero/handling-old-api-also-1381167726957 (pull request #1)
* minor patch in order to make sure that r\_json is defined
* handling old API also
* Added code to deal with failure to update issue because it has no assignee, this can happen when the current assignee is invalid
* Removed fixed dependency on tlslite fixing #58
* Merged in mdoar/jira-python-add-labels (pull request #28)
* Merged in joernsn/jira-python (pull request #29)
* Fix issue #63
* Fixes https://bitbucket.org/bspeakmon/jira-python/issue/56/rest-resource-sprints-renamed-to
* Added async support for update command, which would use requests. This is still experimental and triggered only manually so it should not affect normal usage
* Added support for specifying issue id as int
* Issue #52 added modifying labels to the documentation
* Fixing issue #50 by detecting the correct issue-type and reversing the direction when needed
* Fixing #49 by auto fixing assignee and reporter if update() fails due them having invalid values. This will work only if you do not specify these fields in the original requests and if you enable this feature by adding autofix='username' as a parameter when you create the JIRA instance
* added applicationlinks() method
* Added default headers to the configuration so you can override them for all calls
* added missing jira params for search-user
* Merged in jjinux/jira-python (pull request #27)
* Fixed an error in a comment in an example
* Added jira.backup() that would call backup option in Jira admin
* Added code for auto-detection and usage of HTTP(S) proxies. Also this would allow you to use a custom proxy if you want
* Added debug information regarding the load of the config.ini (visible only python logging level is set to DEBUG)
* Merged in frobnic8/jira-python (pull request #26)
* Fixed bug for unloaded resources in Resource.\_\_repr\_\_
* Added additional fallback for Resource.\_\_repr\_\_
* Added detection for authentication failure in the response
* Merged in frobnic8/jira-python (pull request #25)
* Merged in markeganfuller/jira-python (pull request #23)
* Merged in kraiz/jira-python/kraiz/be-aware-of-wrong-magic-version-which-ha-1369150687222 (pull request #24)
* Merged in agrimm/jira-python/gh-epic (pull request #22)
* Added better unicode handling for Resource.\_\_str\_\_
* Added child support for nested selects to the \_\_str\_\_ method on Resource
* Added \_\_str\_\_ and \_\_repr\_\_ support to the basic Resource class
* Merged bspeakmon/jira-python into master
* be aware of wrong magic version (which has no keyword argument "mime")
* Essential fix that will enable you to connect to more than one Jira instance at once, otherwise it will fail as the defaults dictionary was not copied on instantiation
* Added improved output of error messages for Jira 6.x
* Merged bspeakmon/jira-python into master
* Add method for adding issues to epics
* Added rename\_user() method, current implementation relies on Script Runner plugin. Still, if this is missing it will fail nicely indicating what you have to do
* Added the option to load the default jira profile specified inside the config.ini
* Prevented reindex() from throwing exception when reindex operation returns 503 while jira is doing the foreground reindexing
* Added reindex() for JIRA class. Now you can trigger Jira reindexing using python-jira. Implementation supports force mode and background/foreground mode
* Merged in sorin/jira-python (pull request #19)
* Switched to SafeConfigParser for config module
* Added config.py module which allows people to init JIRA with a single command and by keeping credentials to another file
* Added jira.config module which allows people to load jira credentials from a config file
* Added sphinx to setup.py so now you can build documentation using \`python setup.py build\_sphinx\` modified:   setup.py
* Improved documentation regarding transitions, now includes example of setting the resolution field and alternative way to specify parameters. modified:   .gitignore modified:   docs/index.rst
* Fix name typo in docs
* woopsy, deleted the pycrypto stuff on accident

0.13
----

* Add changelog and acknowledgements for 0.13 release
* Set version 0.13 for release
* Fix GreenHopper object placement (damn it mdoar :)
* Merged in dvj/jira-python/libmagic-optional (pull request #17)
* Merged in mdoar/jira-gh-python (pull request #16)
* make python-magic optional
* Fix a comment
* Change ordering of parameters for transition\_issues to maintain backwards compatibility
* Updated documentation to refer to JIRA. Ensure no TODO appears in docs
* Add optional comment parameter to transition\_issue
* Add changelog for upcoming release
* Added class for accessing GreenHopper via REST. Example use script added too
* Added class for accessing GreenHopper via REST. Example use script added too
* Remove unneeded cookie authentication when using Basic Auth
* Document new verify parameter
* Add 'verify' parameter to options dict
* Document the PyCrypto requirement for OAuth
* Update docs with the new ResultList return type
* Add ResultList class for including search metadata
* Merged bspeakmon/jira-python into master
* Clarify docs regarding add\_attachment()
* Fix broken OAuth in jirashell by switching to requests\_oauthlib
* Merged in gdw2/jira-python (pull request #15)
* fixed minor typo in docs
* Add requests\_oauthlib to dependencies
* Use requests\_oauthlib for OAuth
* Merged in markeganfuller/jira-python (pull request #8)
* Update requests requirement in docs
* Merged in vassius/jira-python (pull request #12)
* Merged in vassius/jira-python/issue-14 (pull request #13)
* Document new parameter
* Changed requests version in setup.py dependencies
* Add optional file name parameter to add\_attachment()
* Fix issue #14
* Fix issue #7 and #8
* Added content-type to Resource.update
* Updating to work with requests-1.1.0
* Merged in shawnps/jira-python (pull request #10)
* fix project URL in docs
* Fix for empty errorMessages, moved length check to main logic for deciding which error message to use and added check for 'errors' in the response
* Merged bspeakmon/jira-python into master
* Update to new address + contact info
* Merged in markeganfuller/jira-python (pull request #6)
* Added a length check on error messages. This avoids any "IndexError: list index out of range" when an empty list is returned
* Merged in ranman/jira-python (pull request #4)
* pep8 fixes
* rip off trailing slash on server urls and add auth
* update dictionary instead of adding together items

0.12
----

* Update docs for release
* Bump to version 0.12 for imminent release
* Bump to latest version of requests and ipython. Also made ranges open-ended (fixes #2)
* hardcode some access tokens for running tests with oauth (I'll move it to a file later)
* Add option to print oauth tokens as they're received
* Move tests and test resources to their own package
* Read from a config file and merge it with command line options
* prefer oauth to basic\_auth if both exist
* - refactor tests to prepare for oauth support
* - standardize content-type autodetect
* - make tests more forgiving when less-than-exact comparisons are required - fix a few other brokens
* - make error message detection more intelligent
* - improve autodetection (still not quite right)
* - auto-add content type to PUT/POST if it's not already there   (add\_attachment and friends are still broken)
* - fix broken oauth initialization
* - start doc updates

0.11
----

* - bump to version 0.11
* - fix broken oauth initialization
* - add update and delete examples

0.10
----

* don't need explicit argparse import
* use webbrowser to simplify the authorization process
* use webbrowser to simplify the authorization process
* add OAuth dance support to jirashell
* add OAuth support to client and jirashell
* make raise\_on\_error more helpful
* add tlslite to dependencies for requests\_oauth bump to beta list (oooOOOOoooo)
* incorporate private fork of requests-oauth to handle RSA-SHA1 for atlassian oauth
* - added -P option for jirashell to read password from prompt
* - refactor raise\_on\_error to exceptions.py - make \_\_str\_\_ value useful

0.9
---

* - bump to version 0.9 for summit release
* Implement decorators for handling resource arguments in JIRA client calls
* remove Comments and Dashboards resources; specify a better couple of createmeta tests
* update set\_application\_property() doc
* - spiffy up sphinx docs

0.8.0
-----

* implement issue.update(), issue.delete()
* test version.update()
* implement and test role.update()
* test worklog.update()
* implement and test RemoteLink.update()
* - test comment.update()
* - implement Resource.update() - test component.update()
* bump to version 0.8 for next release
* Merged in vitaly4uk/jira-python (pull request #2)
* package version have been updated
* \_get\_url now use api version
* fix several resource construction bugs; implement delete functionality
* kill unused import
* use standard icon test resource for avatar tests
* factor out set\_avatar logic
* implement project avatar upload and selection
* implement user avatar upload and selection
* add missing comment for search\_allowed\_users\_for\_issue()
* implement add\_attachment()
* implement transition\_issue
* kill missed pass statement
* implement create\_issue()
* - centralize version info
* - make python 2.7 requirement explicit
* - implement add\_remote\_link()
* - implement move\_version()
* - implement create\_version()
* - implement add/remove votes/watchers
* - add stubs for add/remove vote and watcher - implement create\_issue\_link()
* - implement add\_comment()
* - implement create\_component and tests
* - add basic test for add\_worklog()
* Merged in gak/jira-python (pull request #1)
* - add placeholder for add\_comment()
* - add SSL verification if the server url starts with https
* - add doc link to readme
* - first doc with sphinx pass - use jira-python for name - remove separate module doc pages
* - kill docstring warning
* - add add\_worklog method with timeSpent, adjustEstimate et al
* - include source path in sphinx sys.path
* - add rst autogen for client modules - update conf.py to find modules in source path
* - add sphinx doc skeleton

0.7.0
-----

* - bump to version 0.7.0
* - doc exception
* - update gitignore
* - removed utils; we don't seem to need it - updated ignores
* - restructure module
* - add docstrings
* - fix formatting
* - rest of docstrings for jira module - remove options argument from universal find()
* - start API docstrings

0.6.0
-----

* - convert tools to package - fix jirashell installation in setuptools - bump to version 0.6
* - make jirashell a proper module and give it an entry point
* - make jirashell a proper module and give it an entry point
* - use json from python standard library
* - raise JIRAError for \_get\_json() operations that fail
* - improve exceptions - test that invalid find throws proper exception
* - eliminate some duplication
* - update install instructions

0.5.0
-----

* - fix path to repo
* - add license
* - update README
* - update README - change project name
* - update examples
* - move resources to use session - fix warnings
* - use requests session to persist cookies/headers - add oauth placeholder
* - add cls\_for\_resource tests - correct total fields value for default test data
* - return Resource for unmatched self links
* - kill unused import
* - fix universal resource loader
* - add support for issue remote links
* - add setup.py - add README placeholder
* - rename private vars
* - session/websudo tests
* - fix wrong param order in session()
* - most of the remaining tests
* - parameter name standardization - handle passed params correctly
* - rename roles() and role() - remove expand param from versions until I can confirm it exists
* - correct my\_permissions()
* - more tests
* - support all-groups option
* - lots more tests
* - clean up application\_properties()
* - fix typo in customFieldOption Resource
* - fix REs for resource matching
* - fix wrong var name bug :/
* - start tests (YAY)
* - add expandos - promote customFieldOption to Resource
* - clean up \_get\_json uses - add expand parameters to affected resources
* - code cleanup
* - recursive resource parsing
* - fixed format bug I just introduced :/
* - clean up string formatting - remove unneeded paramter in \_get\_json
* - method refactoring - always turn raw json in resources into object attributes
* - fix searches - implement rest of reading
* - derp
* - implement remaining resources - clear up some gets
* - always create cookies (this lets us do anonymous access)
* - add server info to jirashell
* - use direct JSON get instead of search resource
* - reorganize project structure
* - implement rest of non-resource methods - move example use to its own file
* safer check for tuple coercion (thanks to dchambers)
* - help message
* - fix ipython shell
* - merge util method
* - start console
* - implement a few non-resource client methods
* Pass (auth) cookies through to resource constructors
* - implement BASIC session (need to save cookies intelligently)
* - stubbed API
* - take \*\*kw in delete() - use new string formatting
* Examples using the attribute access from the JSON response
* - augment returned object with params of json
* make resource loading more general
* - added options param to fine - search returns list of issues
* Take a raw param to build issues out of other issues
* Change save to update() and take kwargs
* Refactor issue method into clearer parts
* implement JQL search
* Implement generic find() method and clean up API
* - raise on 400-500 errors from server
* - more sketches
* - actually we can do better
* - optionally enable issue finding - move issue resource to separate module - use new-style classes
* - checkpoint work on issue-related client



