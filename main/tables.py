"""Tables for the main app."""

import django_tables2 as tables


class ProcessTable(tables.Table):
    """Defines and Process Table for the data from the Process Manager."""

    uuid = tables.Column(verbose_name="UUID")
    name = tables.Column(verbose_name="Name")
    user = tables.Column(verbose_name="User")
    session = tables.Column(verbose_name="Session")
    status_code = tables.Column(verbose_name="Status Code")
    exit_code = tables.Column(verbose_name="Exit Code")
    restart = tables.TemplateColumn(
        "<a href=\"{% url 'restart' record.uuid %}\" onclick=\"return confirm('You are about to restart process {{record.uuid}}. Are you sure?')\">RESTART</a>",  # noqa: E501
        verbose_name="",
    )
