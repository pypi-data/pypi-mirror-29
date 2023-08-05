Workfront for Python (SDK)
==========================
.. image:: https://img.shields.io/pypi/v/workfront-sdk.svg
    :target: https://pypi.python.org/pypi/workfront-sdk
    :alt: [Latest Release Version]

SDK for managing Workfront tasks

Installation
------------

Install via ``pip``:

.. code-block:: console

  $ pip install workfront-sdk

Install from source:

.. code-block:: console

  $ git clone git://github.com/BridgeMarketing/workfront-sdk.git
  $ cd workfront-sdk
  $ python setup.py install


Examples
--------

How to create a Workfront Service object
----------------------------------------

Create the Workfront object and login:

.. code-block:: pycon

  >>> from workfront import Workfront
  >>> wf = Workfront("ay.caramba@thebridgecorp.com", "1234wfpass")
  >>> wf.login()

Then you can use it.

How to create a user object
---------------------------

With a Workfront service object, you can create a user by email or by id:

.. code-block:: pycon

  >>> from workfront.objects import user
  >>> user_by_email = user.from_email(wf, "ay.caramba@thebridgecorp.com")
  >>> user_by_id = user.from_id(wf, "<WORKFRONT_USER_ID>")

You can then access some fields of the users:

.. code-block:: pycon

  >>> print user_by_email.wf_id # print the workfront id
  >>> print user_by_email.name # print the name of the user
  >>> print user_by_email.emailAddr # print the email of the user

How to create and interact with a Task
--------------------------------------

Create the task by it's workfront id and giving a Workfront service

.. code-block:: pycon

  >>> from workfront.objects.task import WFTask
  >>> task = WFTask(wf, "<WF_TASK_ID>")

Change the status of a task
---------------------------

.. code-block:: pycon

  >>> from workfront.objects.status import WFTaskStatus
  >>> task.set_status(WFTaskStatus.in_progress)

Assign a task to a different user
---------------------------------

Once you have a WF user and a task you can:

.. code-block:: pycon

  >>> from workfront.objects import user
  >>> from workfront.objects.task import WFTask
  >>> user_by_email = user.from_email(wf, "ay.caramba@thebridgecorp.com")
  >>> task = WFTask(wf, "<WF_TASK_ID>")
  >>> task.assign_to_user(user_by_email)

Get and set custom fields
-------------------------

You can use the methods **set_param_values** and **get_param_values** to modify and access task custom fields.

.. code-block:: pycon

  >>> task = WFTask(wf, "<WF_TASK_ID>")
  >>> task.get_param_values()
  >>> {"custom_field": "value", "list_field": ["value1", "value2"]}
  >>> task.set_param_values({"custom_field": "other_value"})
  >>> task.get_param_values()
  >>> {"custom_field": "other_value", "list_field": ["value1", "value2"]}

How to use projects
-------------------

You can load a project from the id, and access the template id:

.. code-block:: pycon

  >>> from workfront.objects import project
  >>> p = project.WFProject(wf, "<WF_PROJECT_ID>")
  >>> project_template_id = p.get_template_id()

With the template id, you can create another project:

.. code-block:: pycon

  >>> from workfront.objects import project
  >>> new_project = project.crt_from_template(wf, project_template_id, "NEW PROJECT NAME")
  >>> new_project.wf_id
