crdist
=========

.. image:: https://travis-ci.org/solvo/crdist.svg
    :target: https://travis-ci.org/solvo/crdist

Costa Rican Geografic distribution for model admin in Django.

Now django 1.11 compatible.

.. note:: 
    The data is in Spanish.
    
    All source code is in English and of course it is spanish translated.

Installation
-------------

Install crdist in your python environment

1- Download and install package:

.. code:: bash

    $ pip install crdist

Through Github:

.. code:: bash

    $ pip install git+https://github.com/solvo/crdist.git


Put crdist in your INSTALLED_APPS

.. code:: python

    INSTALLED_APPS = (
        ...
        'crdist',
        )

Include crdist in your urls.py

.. code:: python

	from django.conf.urls import url, include
	urlpatterns = [
		url(r'^crdist/', include("crdist.urls")),
	]


Run migration 

.. code:: bash

    $ python manage.py migrate    


Usage
---------

In your models create a Foreign relation to District in your *models.py* file.

.. code:: python
    
    from crdist.models import District
    class Test(models.Model):
        name = models.CharField(max_length=64)
        location = models.ForeignKey(District) 
    

We provide a form widget specially for choose Province, Canton and District in the same widget. eg.

.. code:: python

    from crdist.widgets import DistrictSelect
    from crdist.models import District
    
    class CRForm(forms.Form):
        district = forms.ModelChoiceField(queryset=District.objects.all(),
                                      widget=DistrictSelect)


It's also ok use with admin interface, you can add some code in your *admin.py* file.

.. code:: python

    class TestAdminForm(forms.ModelForm):
        class Meta:
            model = Test
            fields = '__all__'
            widgets = {
              'district': DistrictSelect(attrs={"class": "form-control"}),
            }
    
    
    class TestAdmin(admin.ModelAdmin):
        form = TestAdminForm

    admin.site.register(Test, TestAdmin)
    
We also support multiple relations in the same model, so you can display several widgets in the same page.

Javascrit triggers 
-------------------------

- load_canton   { "dist": 'div_district_' + name, "canton": 'div_canton_' + name }
- load_district   { "dist": 'div_district_' + name }

.. code:: javascript

    document.addEventListener("load_canton", function(e) {
	  console.log(document.cantoncrdist.dist); 
	  console.log(document.cantoncrdist.canton);   // id of divs
	});
    
