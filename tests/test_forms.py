from django import forms

from main.forms import BootForm


def test_boot_form_empty():
    """Test for the BootForm."""
    form = BootForm()
    assert not form.is_bound
    assert len(form.fields) == 4
    assert type(form.fields["session_name"]) is forms.CharField
    assert type(form.fields["n_processes"]) is forms.IntegerField
    assert type(form.fields["sleep"]) is forms.IntegerField
    assert type(form.fields["n_sleeps"]) is forms.IntegerField


def test_boot_form_with_data(dummy_session_data):
    """Test for the BootForm."""
    form = BootForm(data=dict())
    assert form.is_bound
    assert not form.is_valid()
    assert len(form.errors) == 4
    for message in form.errors.values():
        assert message == ["This field is required."]

    form = BootForm(data=dummy_session_data)
    assert form.is_bound
    assert form.is_valid()
    assert form.cleaned_data["session_name"] == "sess_name"
    assert form.cleaned_data["n_processes"] == 1
    assert form.cleaned_data["sleep"] == 5
    assert form.cleaned_data["n_sleeps"] == 4
