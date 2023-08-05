History of zest.emailhider package
==================================


3.1.3 (2018-02-20)
------------------

- Make 'No uids found in request.' a warning instead of an error.
  I see bots requesting this url.  [maurits]


3.1.2 (2017-03-08)
------------------

- Do not render our javascript inline.  It leads to display problems
  when it is included on a 404 page or any other non 20x page:
  an assertion in ``Products.ResourceRegistries`` fails, resulting in
  the html being returned with mimetype javascript.
  That seems a possible problem with any inline script.
  Added upgrade step for this.
  [maurits]


3.1.1 (2017-02-24)
------------------

- Fixed javascript bug that caused a request even without any emails to reveal.
  [maurits]


3.1 (2016-11-02)
----------------

- Query and reveal all emails at once.  If you have an employee
  content type that you have hooked up to zest.emailhider, and you
  have a page showing fifty employees, previously we would fire fifty
  ajax requests.  Now we gather everything into one request.
  [maurits]


3.0 (2015-10-03)
----------------

- Added Travis badge.
  [maurits]

- Support Plone 5 by reading ``plone.email_from_address`` from the
  registry.  This loses compatibility with Plone 4.0.  We try reading
  any email (also your own additional emails) from the registry first,
  with ``plone.`` prepended, and then look for a property on the
  portal root.
  [maurits]

- Use ``$`` instead of ``jq`` in our javascript.  Now it works without
  needing ``jquery-integration.js``.  This loses compatibility with
  Plone 3.
  [maurits]

- Added ``test_emailhider`` page that hides the portal
  ``email_from_address``, so you can easily test it.  When you disable
  your javascript you should not see an email address.
  [maurits]


2.7 (2012-09-12)
----------------

- Moved to github.
  [maurits]


2.6 (2011-11-11)
----------------

- Added MANIFEST.in so our generated .mo files are added to the source
  distribution.
  [maurits]

- Register our browser views only for our own new browser layer.
  Added an upgrade step for this.  This makes it easier for other
  packages to have a conditional dependency on zest.emailhider.
  [maurits]


2.5 (2011-06-01)
----------------

- Updated call to 'jq_reveal_email' to use the one at the root of the
  site to avoid security errors. [vincent]


2.4 (2011-05-10)
----------------

- Updated jquery.pyproxy dependency to at least 0.3.1 and removed the
  now no longer needed clean_string call.
  [maurits]


2.3 (2010-12-15)
----------------

- Not only look up a fake uid for email_from_address as portal
  property, but do this for any fake uid that has 'email' or 'address'
  in it.  Log warnings when no email address can be found for a fake
  or real uid.
  [maurits]


2.2 (2010-12-14)
----------------

- Added another upgrade step as we definitely need to apply our
  javascript registry too when upgrading.  Really at this point a
  plain reinstall in the portal_quickinstaller is actually fine, which
  we could also define as upgrade step, but never mind that now.
  [maurits]


2.1 (2010-12-14)
----------------

- Added two upgrade steps to upgrade from 1.x by installing
  jquery.pyproxy and running our kss step (which just removes our
  no longer needed kss file).
  [maurits]


2.0 (2010-12-09)
----------------

- Use jquery.pyproxy instead of KSS.  This makes the page load much
  less for anonymous users.
  [vincent+maurits]


1.3 (2009-12-28)
----------------

- Made reveal_email available always, as it should just work whenever
  we want to hide the glocal 'email_from_address'.  If we have a real
  uid target, then try to adapt that target to the IMailable interface
  and if that fails we just silently do nothing.
  [maurits]


1.2 (2008-11-19)
----------------

- Using kss.plugin.cacheability and added it as a dependency.  [jladage]

- Allow to set the uid to email_from_address.  [jladage]

- Changed the KSS to use the load event instead of the click event - it
  now either works transparently, or asks the user to activate JS. [simon]


1.1 (2008-10-24)
----------------

- Added translations and modified template to use them. [simon]

- Initial creation of project. [simon]


1.0 (2008-10-20)
----------------

- Initial creation of project. [simon]
