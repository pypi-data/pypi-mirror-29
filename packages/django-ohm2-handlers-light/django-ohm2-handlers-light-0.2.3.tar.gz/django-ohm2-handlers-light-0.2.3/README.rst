django-ohm2-handlers-light source code
=============================


Installation:

#. Create a Python +3.5 virtualenv

#. Install dependencies (optional)::

    - dateutil
    - Crypto
    - Pillow
    - unidecode
    - htmlmin
    - qrcode
    - barcode

#. Add 'ohm2_handlers_light' to installed apps::

    INSTALLED_APPS = [
      '''
      'ohm2_handlers_light',
      ...
    ]

#. Create tables::

    ./manage.py migrate




Models
------

handlers_light comes with two basic models::

  class BaseModel(models.Model):
    identity = models.CharField(max_length=settings.STRING_DOUBLE, unique = True)
    created = models.DateTimeField(default = timezone.now)
    last_update = models.DateTimeField(default = timezone.now)
    
    objects = ohm2_handlers_light_managers.OHM2HandlersLightManager()

    def __str__(self):
      return self.identity

    class Meta:
      abstract = True


  class BaseError(BaseModel):
    app = models.CharField(max_length=settings.STRING_DOUBLE)
    code = models.IntegerField(default = -1)
    message = models.TextField(default = "")
    extra = models.TextField(default = "")
    
    ins_filename = models.CharField(max_length=settings.STRING_DOUBLE, null = True, blank = True, default = "")
    ins_lineno = models.IntegerField(null = True, blank = True, default = 0)
    ins_function = models.CharField(max_length=settings.STRING_DOUBLE, null = True, blank = True, default = "")
    ins_code_context = models.TextField(null = True, blank = True, default = "")

    def __str__(self):
      return "{0}|{1}|{2}|{3}".format(self.identity, self.app, self.code, self.message)



Use 'BaseModel' as base model for every model within the project.


Context processors
------------------

Add 'ohm2_handlers_light.context_processors.context' to TEMPLATES like this::

  TEMPLATES = [
      {
          'BACKEND': 'django.template.backends.django.DjangoTemplates',
          'DIRS': [],
          'APP_DIRS': True,
          'OPTIONS': {
              'context_processors': [
                  'django.template.context_processors.debug',
                  'django.template.context_processors.request',
                  'django.contrib.auth.context_processors.auth',
                  'django.contrib.messages.context_processors.messages',
                  ...
                  'ohm2_handlers_light.context_processors.context',
                  ...
              ],
          },
      },
  ]


Then 'c_ohm2_handlers_light' will be available. This variable is controlled by 'ohm2_handlers_light.utils.get_context'.


Parsers
-------

Use 'get_as_or_get_default' like this (maps outter user variables to inner server variables)::
  
  # views.py
  from ohm2_handlers_light.parsers import get_as_or_get_default
  
  def post_view(request):

    keys = (
      ("inner-name", "outter-name", "default-value"),
    )

    cleaned_params = get_as_or_get_default(request.POST, keys)




Decorators
----------

Safe requests (ohm2_handlers_light.decorators.ohm2_handlers_light_safe_request)::
  
  Use it to wrap dispatcher's functions. Every wrapped function will be wrapped in a try-except-else. If an error occured
  a RequestException (ohm2_handlers_light.definitions.RequestException) object will be created. 

  Every requests handled using this decorator, will have this as return structure:

    (response, error)

   

Process requests (user input data)
----------------------------------


Process user input data with 'ohm2_handlers_light.utils.mix_cleaned_data' with the follow structure::

  (data type, data name, options)


Example::

  ("string", "username", 1)


Variable username will be used as string with a minumum length of one.

Available Checkers (data type -> options -> comments):

- string -> string's length -> none
- email -> none -> none
- password -> dict with validations to check -> {'lowercase' : True, 'uppercase' : True, 'digits' : True}: all values are optional
- bool -> dict to map bool variables -> {'True' : 'false', 'False' : 'false'}: this function will look for the 'True' and 'False' and convert them to True/False
- u_file -> none -> checks if uploaded file is of type InMemoryUploadedFile/TemporaryUploadedFile
- type -> variable's type -> check if the variable is of type like: type(variable) == int
- mix -> list of types to check -> [int, float, type(None)]







Usage
-----


Create django apps using::

  ./manage.py ohm2_handlers_light_startapp -a your_app



For database usage::
  
  from ohm2_handlers_light import utils as h_utils
  from app.models import Model


Now, usual queries like::
  
  entry = h_utils.db_get(Model, **kwargs) # => Models.objects.get(**kwargs)
  entry = h_utils.db_get_or_none(Model, **kwargs) # => Models.objects.get(**kwargs) wrapped in a try-except ObjectDoesNotExist-else 
  entries = h_utils.db_filter(Model, **kwargs) # => Models.objects.filter(**kwargs)
  entry = h_utils.db_create(Model, **kwargs) # => Models.objects.create(**kwargs)




You can process requests using 'cleaned' like this::
  
  # views.py
  from django.shortcuts import render
  from django.http import HttpResponse
  from ohm2_handlers_light.parsers import get_as_or_get_default
  from your_app import dispatcher as your_app_dispatcher


  def post_view(request):

    keys = (
      ("inner-integer", "outter-integer", 1),
      ("inner-string", "outter-string", "default-string"),
    )

    ret, error = your_app_dispatcher.post_view(request, get_as_or_get_default(request.POST, keys))
    if error:
      return HttpResponse(error.regroup())
    return render(request, "template.html", {"ret" : ret})

  

  #dispatcher.py
  from ohm2_handlers_light import utils as h_utils
  from ohm2_accounts_light import utils as ohm2_accounts_light_utils
  from your_app.decorators import your_app_safe_request

  @your_app_safe_request
  def post_view(request, params):
    p = h_utils.cleaned(params, (
                ("type", "inner-integer", int),
                ("string", "inner-string", 1),
              ))


    ret = {
      "p" : p,
    }
    return ret

