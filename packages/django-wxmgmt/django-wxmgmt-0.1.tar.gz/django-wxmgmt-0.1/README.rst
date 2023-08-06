=====
wxmgmt
=====

简单的Django应用，配置管理微信公众号，包括用户的管理、消息模板的管理，自定义菜单的管理
tenant：公众号信息，
account：关注用户的信息

Quick start
-----------

1. Add "wxmgmt" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'wxmgmt',
    ]

2. Include the polls URLconf in your project urls.py like this::

    path('wxmgmt/', include('wxmgmt.urls')),

3. Run `python manage.py migrate` to create the wxmgmt models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a tenant (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/wxmgmt/ to participate in the poll.
