"""Tables for the process_manager app."""

import django_tables2 as tables

restart_column_template = (
    "<a href={href} onclick=\"return confirm('{message}')\">{text}</a>".format(
        href="\"{% url 'process_manager:restart' record.uuid%}\"",
        message="You are about to restart process {{record.uuid}}. Are you sure?",
        text="RESTART",
    )
)

kill_column_template = (
    "<a href={href} onclick=\"return confirm('{message}')\">{text}</a>".format(
        href="\"{% url 'process_manager:kill' record.uuid%}\"",
        message="You are about to kill process {{record.uuid}}. Are you sure?",
        text="KILL",
    )
)

flush_column_template = (
    "<a href=\"{% url 'process_manager:flush' record.uuid %}\">FLUSH</a>"
)

logs_column_template = (
    "<a href=\"{% url 'process_manager:logs' record.uuid %}\">LOGS</a>"
)


class ProcessTable(tables.Table):
    """Defines and Process Table for the data from the Process Manager."""

    class Meta:  # noqa: D106
        orderable = False

    uuid = tables.Column(verbose_name="UUID")
    name = tables.Column(verbose_name="Name")
    user = tables.Column(verbose_name="User")
    session = tables.Column(verbose_name="Session")
    status_code = tables.Column(verbose_name="Status Code")
    exit_code = tables.Column(verbose_name="Exit Code")
    logs = tables.TemplateColumn(logs_column_template, verbose_name="Logs")
    select = tables.CheckBoxColumn(
        accessor="uuid",
        verbose_name="Select",
        checked="checked",
        attrs={"th__input": {"onclick": "toggle(this)"}},
    )
