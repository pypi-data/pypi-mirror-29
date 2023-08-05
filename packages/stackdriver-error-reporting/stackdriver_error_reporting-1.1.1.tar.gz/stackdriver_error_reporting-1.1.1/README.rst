stackdriver-error-reporting
===========================

This module formats information into a JSON payload that will be read
and interpreted by Stackdriver Logging and Stackdriver Error Reporting
to make sure it appears in Stackdriver Error Reporting.

As yet, it makes no external requests and relies fully on the existence
of `logging agents <https://cloud.google.com/logging/docs/agent/>`__
that scrape the ``stdout`` and ``stderr`` for system logs.

Installation
============

``pip install stackdriver-error-reporting``

Usage
=====

::

    from stackdriver_error_reporting import StackdriverReporter

    logger = StackdriverReporter(service_name='some-python-service', service_version='1.0.0')

    # Report just the error
    try:
        raise ValueError("Wrong value!!")
    except ValueError:
        logger.log_error()

    # Report a request-related error:
    import requests

    API = 'http://some-api-endpoint'
    try:
        resp = requests.get(API)
    except HTTPError:
        context = {'httpRequest':{'responseStatusCode':500, 'method':'post', 'url': API}}
        logger.log_error(context=context)

logger.log\_error(context={}, additional\_fields={}, severity='error')
----------------------------------------------------------------------

+----------------------+-------------+-------------+-----------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+
| Parameter            | Required?   | Default     | Example                                                                     | Note:                                                                                                                       |
+======================+=============+=============+=============================================================================+=============================================================================================================================+
| context              | No          |             | See the subsection ``context``                                              |                                                                                                                             |
+----------------------+-------------+-------------+-----------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+
| additional\_fields   | No          |             | Any ``dict`` containing additional information for troubleshooting errors   | Make sure not to override any of the properties described in ``More on reporting errors to Stackdriver Error Reporting``.   |
+----------------------+-------------+-------------+-----------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+
| severity             | No          | ``error``   | ``error``, or ``critical`` for breaking errors                              |
+----------------------+-------------+-------------+-----------------------------------------------------------------------------+-----------------------------------------------------------------------------------------------------------------------------+

context
~~~~~~~

\| Key \| Description \| \|----------------\|---------\| \| httpRequest
\| Object with HTTP request-related fields \| \| reportLocation \|
Object with [manual] description. Use if you don't have a proper
exception context \| \| user \| Integer or string identifying the user
triggering the error \| For more info, refer to
``More on reporting errors to Stackdriver Error Reporting``

Service context
---------------

The name and version of the service. You can pass them yourself as an
object (see example) or by setting the ``SERVICE_VERSION`` and
``SERVICE_NAME`` environment variables.

In `Stackdriver Error
Reporting <https://console.cloud.google.com/errors>`__, these values
will be reflected in the ``Seen in`` column. This also facilitates the
automatic grouping of errors.

Payload validation
==================

You can use the ``gcloud`` CLI to push a JSON payload to Stackdriver
Logging if you wish to validate its structure and that it properly ends
up in Error Reporting:

::

    gcloud beta logging write --payload-type=json test-errors-log '{"serviceContext": {"version": "1.1.4", "service": "recommender"}, "message": "Traceback (most recent call last):\n  File \"Logger.py\", line 36, in <module>\n    int(\"a\")\nValueError: invalid literal for int() with base 10: 'a'\n", "severity": "error"}'

You might have to install some beta tools for Google Cloud SDK (in which
case you'll be prompted to do so anyway).

More on reporting errors to Stackdriver Error Reporting
=======================================================

`Stackdriver Logging <https://console.cloud.google.com/logs/viewer>`__
picks up almost everything that is printed to ``stdout`` and ``stderr``
within the cluster by default, but not every error ends up in
`Stackdriver Error
Reporting <https://console.cloud.google.com/errors>`__ by default.

In order to enforce this behaviour, we need to log messages according to
a certain structure (`read more
here <https://cloud.google.com/error-reporting/docs/formatting-error-messages>`__):

::

    {
      "eventTime": string, // Seems superfluous, is inferred by the logging agents
      "serviceContext": {
        "service": string,     // Required
        "version": string
      },
      "message": string,       // Required. Should contain the full exception
                               // message, including the stack trace.
      "context": {
        "httpRequest": {
          "method": string,
          "url": string,
          "userAgent": string,
          "referrer": string,
          "responseStatusCode": number,
          "remoteIp": string
        },
        "user": string,
        "reportLocation": {    // Required if no stack trace in 'message'.
          "filePath": string,
          "lineNumber": number,
          "functionName": string
        }
      }
    }

**Note:** Log JSON payloads without any pretty printing and unnecessary
whitespaces/newlines as Stackdriver cannot handle this properly.
