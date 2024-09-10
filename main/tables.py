"""Tables for the main app."""

import django_tables2 as tables

restart_column_template = (
    "<a href={href} onclick=\"return confirm('{message}')\">{text}</a>".format(
        href="\"{% url 'restart' record.uuid%}\"",
        message="You are about to restart process {{record.uuid}}. Are you sure?",
        text="RESTART",
    )
)


class ProcessTable(tables.Table):
    """Defines and Process Table for the data from the Process Manager."""

    uuid = tables.Column(verbose_name="UUID")
    name = tables.Column(verbose_name="Name")
    user = tables.Column(verbose_name="User")
    session = tables.Column(verbose_name="Session")
    status_code = tables.Column(verbose_name="Status Code")
    exit_code = tables.Column(verbose_name="Exit Code")
    restart = tables.TemplateColumn(restart_column_template, verbose_name="Restart")
