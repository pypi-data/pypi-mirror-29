This is a PyPI mirror client according to `PEP 381
<http://www.python.org/dev/peps/pep-0381/>`_.


.. contents::

Build status
============

bandersnatch
    .. image:: https://builds.flyingcircus.io/job/bandersnatch/badge/icon
       :target: https://builds.flyingcircus.io/job/bandersnatch/

Packaging and PIP install
    .. image:: https://builds.flyingcircus.io/job/bandersnatch-packaging-pip/badge/icon
       :target: https://builds.flyingcircus.io/job/bandersnatch-packaging-pip/


Installation
============

The following instructions will place the bandersnatch executable in a
virtualenv under ``bandersnatch/bin/bandersnatch``.

.. note::

    bandersnatch requires Python 3.5


pip
---

This installs the latest stable, released version.

::

  $ virtualenv --python=python3.5 bandersnatch
  $ cd bandersnatch
  $ bin/pip install -r https://bitbucket.org/pypa/bandersnatch/raw/stable/requirements.txt


zc.buildout
-----------

This installs the current development version. Use 'hg up <version>' and run
buildout again to choose a specific release.

::

  $ hg clone https://bitbucket.org/pypa/bandersnatch
  $ cd bandersnatch
  $ ./bootstrap.sh

Configuration
=============

* Run ``bandersnatch mirror`` - it will create an empty configuration file
  for you in ``/etc/bandersnatch.conf``.
* Review ``/etc/bandersnatch.conf`` and adapt to your needs.
* Run ``bandersnatch mirror`` again. It will populate your mirror with the
  current status of all PyPI packages - roughly 500GiB (2017-02-12).
  Expect this to grow substantially over time.
* Run ``bandersnatch mirror`` regularly to update your mirror with any
  intermediate changes.

Webserver
---------

Configure your webserver to serve the ``web/`` sub-directory of the mirror.
For nginx it should look something like this::

    server {
        listen 127.0.0.1:80;
        server_name <mymirrorname>;
        root <path-to-mirror>/web;
        autoindex on;
        charset utf-8;
    }

* Note that it is a good idea to have your webserver publish the HTML index
  files correctly with UTF-8 as the carset. The index pages will work without
  it but if humans look at the pages the characters will end up looking funny.

* Make sure that the webserver uses UTF-8 to look up unicode path names. nginx
  gets this right by default - not sure about others.


Cron jobs
---------

You need to set up one cron job to run the mirror itself.

Here's a sample that you could place in ``/etc/cron.d/bandersnatch``::

    LC_ALL=en_US.utf8
    */2 * * * * root bandersnatch mirror |& logger -t bandersnatch[mirror]

This assumes that you have a ``logger`` utility installed that will convert the
output of the commands to syslog entries.


Maintenance
===========

bandersnatch does not keep much local state in addition to the mirrored data.
In general you can just keep rerunning ``bandersnatch mirror`` to make it fix
errors.

If you delete the state files then the next run will force it to check
everything against the master PyPI::

* delete ``./state`` file and ``./todo`` if they exist in your mirror directory
* run ``bandersnatch`` mirror to get a full sync

Be aware, that full syncs likely take hours depending on PyPIs performance and
your network latency and bandwidth.

Operational notes
=================

Case-sensitive filesystem needed
--------------------------------

You need to run bandersnatch on a case-sensitive filesystem.

OS X natively does this OK even though the filesystem is not strictly
case-sensitive and bandersnatch will work fine when running on OS X. However,
tarring a bandersnatch data directory and moving it to, e.g. Linux with a
case-sensitive filesystem will lead to inconsistencies. You can fix those by
deleting the status files and have bandersnatch run a full check on your data.

Many sub-directories needed
---------------------------

The PyPI has a quite extensive list of packages that we need to maintain in a
flat directory. Filesystems with small limits on the number of sub-directories
per directory can run into a problem like this::

  2013-07-09 16:11:33,331 ERROR: Error syncing package: zweb@802449
  OSError: [Errno 31] Too many links: '../pypi/web/simple/zweb'

Specifically we recommend to avoid using ext3. Ext4 and newer does not have the
limitation of 32k sub-directories.

Client Compatibility
--------------------

A bandersnatch static mirror is compatible only to the "static",  cacheable
parts of PyPI that are needed to support package installation. It does not
support more dynamic APIs of PyPI that maybe be used by various clients for
other purposes.

An example of an unsupported API is PyPI's XML-RPC interface, which is used
when running ``pip search``.

Contact
=======

If you have questions or comments, please submit a bug report to
http://bitbucket.org/pypa/bandersnatch/issues/new.


Code of Conduct
===============

Everyone interacting in the bandersnatch project's codebases, issue trackers,
chat rooms, and mailing lists is expected to follow the
`PyPA Code of Conduct`_.

.. _PyPA Code of Conduct: https://www.pypa.io/en/latest/code-of-conduct/


Kudos
=====

This client is based on the original pep381client by Martin v. Loewis.

Richard Jones was very patient answering questions at PyCon 2013 and made the
protocol more reliable by implementing some PyPI enhancements.



2.1.3 (unreleased)
------------------

- Change version from using pkg_resources and set it in package __init__.py. 
  Fixes #98.
- Add ability to blacklist packages to sync via conf file. Fixes #100.


2.1.2 (unreleased)
------------------

- Add saving of JSON metadata grabbed from pypi.facebook.com for syncing (#91)
-- Can be disabled via config and disabled by default
-- bandersnatch symlinks WEB_ROOT/pypi/PKG_NAME/json to WEB_ROOT/json/PKG_NAME


2.1.0 (unreleased)
------------------

- Fix proxy usage. A bug in the usage of requests on our XMLRPC client
  caused this to break. You can now set *_proxy environment variables
  and get them picked up properly. Fixes #59.

- Add a dict returned from mirror.synchronize() to show deleted
  and added files from the last run

- Fix sorting of releases to use filename and not url

- Tweak atomic file writes in utils.rewrite() to prefix the temporary
  file with the 'hidden' filename of the destination adding more
  support for hashed POSIX filesystems like GlusterFS.


2.0.0 (2017-04-05)
------------------

- Move to Python 3.

  Official support starts with Python 3.5 but might get away with using an
  earlier version of Python 3 (maybe 3.3 or so). However, we plan to start
  using Python 3.5 features (like asyncio) in the near future, so please
  be advised that running with an older version of Python 3 is not
  a supported option for the long term.

- General update of our dependencies to pave the road for Python 3 support.

- Remove residual references to the old "statistics" script that isn't in
  use any longer.

- Fix return code -- we accidentally returned 1 on successful runs
  as debugging code was mixed in the main call. Fixes #67.

- Make the package-specific simple pages human-readable again. Fixes #71.


1.11 (2016-05-18)
-----------------

- Add option to dir-hash index files. See
  https://bitbucket.org/pypa/bandersnatch/pull-requests/22/add-option-to-dir-hash-index-files for a lot more information. Thanks
  @iwienand!

- Fix an edge case: IO errors while marking off packages as "done"
  could result in crashing workers that would result in bandersnatch
  getting stuck. Thanks @wjjt!


1.10.0.1 (2016-05-11)
---------------------

- Brownbag release for re-upload. My train's Wifi broke while uploading
  ending up with a partial file on PyPI. Can your train service do better
  than mine?


1.10 (2016-05-11)
-----------------

This is release is massively supported by @dstufft getting bandersnatch
back in sync with current packaging ecosystem changes. All clap your hands
now, please.

- Refactor the generation update code to avoid weird update paths
  due to, well, my personal kink: overcomplication.

- Generate the simple index ourselves instead of copying it from PyPI.

- Support files hosted on a separate domain.

- Implement PEP 503 normalization rules while also providing support
  for legacy and very legacy clients.


1.9 (2016-04-21)
----------------

- Fix a long standing, misunderstood bug: a non-deleting mirror would
  delete packages if they were fully removed from PyPI. (#61)


1.8 (2015-03-16)
----------------

- Don't require a X-PyPI-Last-Serial header on file downloads.
  (Thanks to @dstufft.)

- Increase our generation to help mirrors recover potential
  setuptools corruption after some data bug on PyPI.


1.7 (2014-12-14)
----------------

- Fix #54 by reordering the simple index page and file fetching
  parts. Thanks @dstufft for the inspiration.

- Stop syncing serversig files and even start removing them.


1.6.1 (2014-09-24)
------------------

- Create a new generation to enforce a full sync when upgrading.
  This is required to get the canonical names for all packages.

1.6 (2014-09-24)
----------------

- Implement canonical package directory names to support an upcoming PIP
  release and other tools. (Thanks to @dstufft)

- Fix a race condition where workers could get stuck indefinitely waiting for
  another item in a depleted queue. (Thanks to hongqn)

1.5 (2014-07-21)
----------------

- Delete broken tests that I forgot to remove.

- Reduce the officially sanctioned maximum number of connections.

1.4 (2014-04-15)
----------------

- Move towards replacing the XMLRPC API with JSON to make our requests
  cacheable. Also reduces the amount of requests needed dramatically.

- Remove apache stats script as this information is no longer being used anyway.

1.3 (2014-02-16)
----------------

- Move to xmlrpc2 to get SSL verification on XML-RPC calls, too. (Fixes #40 and
  big thanks to @ewdurbin)

1.2 (2014-01-08)
----------------

- Potential performance improvement: use requests' session object to allow HTTP
  pipelining. Thanks to Wouter Bolsterlee for the recommendation in #39.


1.1 (2013-11-26)
----------------

- Made code Python 2.6 compatible. Thanks to @ewdurbin for the pull request.


1.0.5 (2013-07-25)
------------------

- Refactor lock acquisition to avoid shadowing exceptions when creating the
  lockfile vs. acquiring the lock.

- Move from distribute back to setuptools.


1.0.4 (2013-07-10)
------------------

- Slight brownbag release: the requirements.txt accidentally included a
  development version of py.test due to my usage of mr.developer.

1.0.3 (2013-07-08)
------------------

- Fix brownbag release with broken 'stable' tag and missing requirements.txt
  update.


1.0.2 (2013-07-08)
------------------

- Generate the index simple page ourselves: its not signed anyway and helps
  PyPI caching more aggressively.

- Add a py.test plugin to actually show a green bar. Hopefully will be
  integrated into py.test in the near future.

- Fix dealing with inconsistent todo files: empty files or with an incorrect
  header will just be deleted and processing resumes at the last known good
  state.

- Mark up requirement of Python 2.7 (#19)

- Fix dealing with new CDN cache issues. Thanks to @dstufft for making PyPI
  support mirrors again.

- Improve test coverage.

1.0.1 (2013-04-18)
------------------

- Fix packaging: include default config file. (Thanks to Jannis Leidel)


1.0 (2013-04-09)
----------------

- Update pip install documentation to use the a URL for referring to the
  requirements.txt directly.

- Adjust buildout and jenkins job to stop fighting over the distribute version
  to install.

1.0rc6 (2013-04-09)
-------------------

- Hopefully fixed updating the stable tag when releasing.


1.0rc5 (2013-04-09)
-------------------

- Experiment with zest.releaser integration to automatically generate
  requirements.txt during release process.


1.0rc4 (2013-04-09)
-------------------

- Experiment with zest.releaser integration to automatically generate
  requirements.txt during release process.


1.0rc3 (2013-04-09)
-------------------

- Experiment with zest.releaser integration to automatically generate
  requirements.txt during release process.


1.0rc2 (2013-04-09)
-------------------

- Experiment with zest.releaser integration to automatically generate
  requirements.txt during release process.


1.0rc1 (2013-04-09)
-------------------

- Initial release. Massive rewrite of pep381client.


