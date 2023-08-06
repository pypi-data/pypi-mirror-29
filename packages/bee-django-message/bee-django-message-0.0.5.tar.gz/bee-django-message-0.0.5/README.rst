=====
message
=====

Quick start
-----------

1. Add "message" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = (
        ...
        'bee_django_message.apps.BeeDjangoMessageConfig',
    )

2. Include the crm URLconf in your project urls.py like this::

    from django.conf.urls import include, url
    ...
    url(r'^message/', include('bee_django_message.urls', namespace='bee_django_message')),

3.settings.py like this::

    MESSAGE_USER_TABLE = None  # 用户表
    MESSAGE_USER_NAME_FIELD = 'first_name'  # 用户表的姓名字段名

3. Run `python manage.py makemigrations`,`python manage.py migrate` to create the crm models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a message (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/message/ to participate in the message.