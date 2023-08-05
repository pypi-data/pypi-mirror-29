rackspace-ticket-report
=======================

A script to gather the week over week ticket counts for the specified time
range. This was specifically created for the Rackspace Private Cloud Insights
API.

Install
*******

To install the `get_ticket_report.py` script::

    pip install rackspace-ticket-report

Run
***

The `get_ticket_report.py` script has a complete help text by running
`get_ticket_report.py -h`. Usage::

    $ get_ticket_report.py --start <start_date> --end <end_date>
    Enter auth token: <your auth token>
    date range, customer generated, employee generated, system generated, total
    ...
