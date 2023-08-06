Django-Rester
=============

|build| |codacy| |pypi| |license|

Package for creating API with built-in validation and authentication
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This product is designed to build API endpoints of varying complexity
and nesting.

The core is a view class - BaseApiView (the inheritor of the standard
django view)

--------------

1. requirements
'''''''''''''''

1. Python 3+

2. Django 1.11+

--------------

2. settings
'''''''''''

DEFAULT settings (may be overridden):

.. code:: python

    DJANGO_RESTER = {
        'AUTH_BACKEND': 'django_rester.rester_jwt', 
        'RESPONSE_STRUCTURE': False,
        'CORS_ACCESS': False,
        'FIELDS_CHECK_EXCLUDED_METHODS': ['OPTIONS', 'HEAD'],
        'SOFT_RESPONSE_VALIDATION': False, 
    }

    DJANGO_RESTER_JWT: {
        'SECRET': 'secret_key',
        'EXPIRE': 60 * 60 * 24 * 14,  # seconds
        'AUTH_HEADER': 'Authorization',
        'AUTH_HEADER_PREFIX': 'jwt',
        'ALGORITHM': 'HS256',
        'PAYLOAD_LIST': ['username'],
        'USE_REDIS': False,  # here can be an int value (redis db number)
        'LOGIN_FIELD': 'username', # as default django login field
    }

**DJANGO\_RESTER** - django-rester settings:

     **AUTH\_BACKEND** - authentication backend\*

     **RESPONSE\_STRUCTURE** - False or can be a dict with 'success',
'message' and 'data' as a values

     **CORS\_ACCESS** - CORS control, True, False, "\*", hosts\_string

     **FIELDS\_CHECK\_EXCLUDED\_METHODS** - methods, which will not be
processed with body structure checks

     **SOFT\_RESPONSE\_VALIDATION** - if True, response will not be cut
off if it will contain additional to response\_structure fields

**DJANGO\_RESTER\_JWT** - JWT authentication settings (in case of
'RESTER\_AUTH\_BACKEND' = 'django\_rester.rester\_jwt')\*:

     **SECRET** - JWT secret key

     **EXPIRE** - token expiration time (datetime.now() +
RESTER\_EXPIRATION\_DELTA)

     **AUTH\_HEADER** - HTTP headed, which will be used for auth token.

     **AUTH\_HEADER\_PREFIX** - prefix for auth token
("Authorization:<prefix> <token>")

     **ALGORITHM** - cypher algorithm

     **PAYLOAD\_LIST** - payload list for token encode (will take
specified **user** attributes to create token)

     **USE\_REDIS** - use redis-server to store tokens or not

     **LOGIN\_FIELD** - user login field (default is 'username' as in
django) \*\*\*

3. built-in statuses
''''''''''''''''''''

``from django_rester.status import ...`` slightly modified status.py
from `DRF <http://www.django-rest-framework.org/>`__, it's simple and
easy to understand.

Any statuses used in this documentation are described in that file.
\*\*\* ##### 4. built-in exceptions:

``from django_rester.exceptions import ...`` Exceptions, which will help
you to recognise errors related to django-rester

**class ResterException(Exception)**

    base django-rester exception, standard Exception inheritor

**class ResponseError(Exception)**

    ResponseError inheritor, added response status -
HTTP\_500\_INTERNAL\_SERVER\_ERROR

**class ResponseBadRequest(ResponseError)**

    ResponseError inheritor, response status changed to
HTTP\_400\_BAD\_REQUEST

**class ResponseServerError(ResponseError)**

    ResponseError inheritor

**class ResponseAuthError(ResponseError)**

    ResponseError inheritor, response status changed to
HTTP\_401\_UNAUTHORIZED

**class ResponseOkMessage(ResponseError)**

    ResponseError inheritor

    acceptable arguments: \*, message='', data=None,
status=HTTP\_200\_OK

**class ResponseFailMessage(ResponseError)**

    ResponseError inheritor

    acceptable arguments: \*, message='', data=None,
status=HTTP\_500\_INTERNAL\_SERVER\_ERROR

**class ResponseBadRequestMsgList(ResponseError)**

    ResponseError inheritor

    acceptable arguments: \*, messages=None,
status=HTTP\_400\_BAD\_REQUEST

    messages could be list, tuple or string.

**class JSONFieldError(ResterException)**

    ResterException inheritor, base JSONField exception

**class JSONFieldModelTypeError(JSONFieldError)**

    JSONField exception, raises when type of model parameter is not
valid

**class JSONFieldModelError(JSONFieldError)**

    JSONField exception, raises when value of model parameter is not
valid

**class JSONFieldTypeError(JSONFieldError)**

    JSONField exception, simple TypeError inside JSONField class

**class JSONFieldValueError(JSONFieldError)**

    JSONField exception, simple ValueError inside JSONField class

**class BaseAPIViewException(Exception)**

    BaseAPIView exception class

**class RequestStructureException(BaseAPIViewException)**

    raise if request structure is invalid

**class ResponseStructureException(RequestStructureException)**

    raise if response structure is invalid \*\*\* ##### 5. permission
classes

``from django_rester.permission import ...`` Permission classes created
to interact wih **@permissions()** decorator (good example of usage), or
in any other way you want

All permission classes accepts only one argument on **init** - django
view **request** object.

All permission classes has 2 attributes, defined on **init**:

**check**: Bool - returns **True** or **False** if request.user may or
may not access endpoint method

**message**: could be a string or list of messages **class
BasePermission**

    contains all base permission methods, it is not recommended to use
it directly in projects

**class IsAuthenticated(BasePermission)**

    check = **True** if user authenticated and active, else **False**

**class IsAdmin(BasePermission)**

    check = **True** if user authenticated and active and is\_superuser,
else **False**

**class AllowAny(BasePermission)**

    check = **True** for any user (even anonymous)

--------------

6. built-in decorators
''''''''''''''''''''''

``from django_rester.decorators import ...`` **@permissions()**

    accepts permission class or list, tuple of classes.

    if check is passed, then user will be allowed to use endpoint

example:

::

    class Example(BaseApiView):

        @permissions(IsAdmin)
        def post(request, request_data, *args, **kwargs):
            pass

--------------

7. built-in views
'''''''''''''''''

``from django_rester.views import ...`` **class BaseApiView(View)**

inherits from standard django view.

class attributes:

    **auth** - authentication backend instance

    **request\_fields** - request validator (use JSONField to build this
validator)

    **response\_fields** - response validator (use JSONField to build
this validator)

class HTTP methods (get, post, put, etc...) accepts next arguments:
request, request\_data, \*args, \*\*kwargs

    **request** - standard django view request object

    **request\_data** - all received request parameters as json
serialized object

User authentication with selected authentication backend **class
Login(BaseApiView)**

Could be used to authenticate user with selected authentication backend.

    Allowed method is 'POST' only.

    Requires username and password in request parameters (username
fieldname parameter may be set in settings)

    Returns token and HTTP\_200\_OK status code if authentication
success, error message and HTTP\_401\_UNAUTHORIZED if failed **class
Logout(BaseApiView)**

Could be used to logout (with redis support) or just to let know
frontend about logout process. Any view could be used the same way, here
is a **simple example**:

    **app/views.py:**

.. code:: python

    from django_rester.views import BaseAPIView
    from django_rester.decorators import permissions
    from django_rester.exceptions import ResponseOkMessage
    from django_rester.permission import IsAdmin
    from django_rester.status import HTTP_200_OK
    from app.models import Model # import Model from your application
    from django_rester.fields import JSONField

    class TestView(BaseAPIView):

        request_fields = {"POST": {
            "id": JSONField(field_type=int, required=True, ),
            "title": JSONField(field_type=str, required=True, default='some_title'),
            "fk": [{"id": JSONField(field_type=int, required=True)}],
        }}

        response_fields = {"POST": {
            "id": JSONField(field_type=int, required=True, ),
            "title": JSONField(field_type=str, required=True, default='some_title'),
            # ...
        }}

        def retrieve_items():
            return Model.objects.all()

        def create_item(title):
            item, cre = Model.objects.get_or_create(title=title)
            return item, cre

        @permissions(AllowAny)
        def get(self, request, request_data, *args, **kwargs):
            items = self.retrieve_items()
            response_data = {...here we should build some response structure...}***
            return response_data, HTTP_200_OK

        @permissions(IsAdmin)
        def post(self, request, request_data, *args, **kwargs):
            title = request_data.get('title', None)
            # no need to check 'if title', because it is allready validated by 'available_fields'
            # ... here we will do some view magic with the rest request_data
            item, cre = self.create_item(title)
            if not cre:
                raise ResponseOkMessage(message='Item allready exists', data={'title': title})
            response_data = {...here we should build some response structure...}***

            return response_data

    **app/urls.py:**

.. code:: python

    from django.conf.urls import url
    from .views import TestView

    urlpatterns = [
        url(r'^test/', TestView.as_view()),
    ]

--------------

8. built-in fields
''''''''''''''''''

``from django_rester.fields import ...`` **class JSONField**

class attributes:

    **field\_type** - data type (int, float, str, bool)

    **required** - field is required

    **default** - default value if not specified

    **blank** - may or may not be blank

    **model** - model for foreign relations

    **field** - field for foreign relations

methods (public), with normal usage, you won't need them in your code:

    **check\_type** - validate type of JSONField value

    **validate** - validate field value with parameters \*\*\*

\*- There is only one authentication backend available for now -
RESTER\_JWT

\*\*- BaseApiView is on active development stage, other attributes and
methods could be added soon

\*\*\*- automatic response structure build - one of the nearest tasks

.. |build| image:: https://travis-ci.org/lexycore/django-rester.svg?branch=develop
   :target: https://travis-ci.org/lexycore/django-rester
.. |codacy| image:: https://api.codacy.com/project/badge/Grade/dee291831b0b43158e2d2301726e2c00
   :target: https://www.codacy.com/app/lexycore/django-rester/dashboard
.. |pypi| image:: https://img.shields.io/pypi/v/django-rester.svg
   :target: https://pypi.python.org/pypi/django-rester
.. |license| image:: https://img.shields.io/pypi/l/django-rester.svg
   :target: https://github.com/lexycore/django-rester/blob/master/LICENSE


