from django import forms


def test_boot_form():
    """Test for the BootForm."""
    from main.forms import BootForm

    form = BootForm()
    assert not form.is_bound
    assert len(form.fields) == 4
    assert type(form.fields["session_name"]) is forms.CharField
    assert type(form.fields["n_processes"]) is forms.IntegerField
    assert type(form.fields["sleep"]) is forms.IntegerField
    assert type(form.fields["n_sleeps"]) is forms.IntegerField
