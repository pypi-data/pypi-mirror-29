0.7.0 - 2018-02-15
##################

** [NEW] Added a CRUD Base Library
** [FEAT] Added a token generation method to the user
** [CHANGE] Cleaned up the REPR for permissions entity
** [CHANGE] Only close the SA session when failure occurs
** [FIX] auth_required accepts the proper arguments


0.6.1 - 2017-12-15
##################

** [BUG] Add a req/resp to failed action functions
** [FEAT] Make ParseJWTMiddleware available at the middleware level
** [BUG] Allow setting of the get_id function


0.6.0 - 2017-12-15
##################

** [NEW] Added a global SQLAlchemy Scoped Session to facilitate testing and other items
** [CHANGE] AuthRequiredMiddleware was split into two and there is a new ParseJWTMiddleware
** [BUG] Cleaned up a number of issues with the way SQLAlchemy ORM is being used


0.5.0 - 2017-12-02
##################

+* [NEW]  A brand-spanking new permission system with users, groups, and permissions
+* [FEAT] Post-login redirect is now configurable.
+* [FEAT] Create a simple redirection resource
+* [FEAT] Jinja2 Middleware can take application globals to inject into the template
+* [FEAT] Added a mixin for testing entities

0.4.2 - 2017-10-25
==================
* Enable Auth Middleware to always run. Helpful when then entire application is
  an API that requires authentication.

0.4.1 - 2017-10-19
==================

* Fix issue with importing Marshmallow Middleware

0.4.0 - 2017-10-14
==================

* Added Marshmallow Middleware for auto schema loading (655cf76_)

.. _655cf76: https://gitlab.com/skosh/falcon-helpers/commit/655cf76


0.3.1 - 2017-10-09
==================

* [FEAT] Add a number of helpful SQLAlchemy Features

0.3.0 - 2017-10-07
==================

* [FEAT] Setup SQLAlchemy
* [BUG] Install cryptography for JWT's with RSA algo

0.2.1 - 2017-10-07
==================
* Fix issue when using HS256 tokens for authentication

0.2.0 - 2017-09-23
==================
* Release the Package and update the source location

0.1.0 - 2017-08-22
==================

* Added StaticsMiddleware
