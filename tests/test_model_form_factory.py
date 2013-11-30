from wtforms import Form
from wtforms_alchemy import model_form_factory, FormGenerator
from tests import ModelFormTestCase

try:
    from wtforms.meta import DefaultMeta
    has_wtforms2 = True
except ImportError:
    has_wtforms2 = False


class TestModelFormFactory(ModelFormTestCase):
    def test_supports_parameter_overriding(self):
        self.init()

        class MyFormGenerator(FormGenerator):
            pass

        defaults = {
            'assign_required': False,
            'all_fields_optional': True,
            'only_indexed_fields': True,
            'include_primary_keys': True,
            'include_foreign_keys': True,
            'strip_string_fields': True,
            'include_datetimes_with_default': True,
            'form_generator': True,
            'date_format': '%d-%m-%Y',
            'datetime_format': '%Y-%m-%dT%H:%M:%S',
        }
        ModelForm = model_form_factory(Form, **defaults)
        for key, value in defaults.items():
            assert getattr(ModelForm.Meta, key) == value

    def test_supports_custom_base_class_with_model_form_factory(self):
        self.init()

        class SomeForm(Form):
            pass

        class TestCustomBase(model_form_factory(SomeForm)):
            class Meta:
                model = self.ModelTest

        assert isinstance(TestCustomBase(), SomeForm)

    def test_class_meta_wtforms2(self):
        if not has_wtforms2:
            return  # Not running on wtforms2

        self.init()

        class SomeForm(Form):
            class Meta:
                locales = ['fr']
                foo = 9

        class OtherForm(SomeForm):
            class Meta:
                pass

        class TestCustomBase(model_form_factory(SomeForm)):
            class Meta:
                model = self.ModelTest

        form = TestCustomBase()
        other_form = OtherForm()
        assert isinstance(form.meta, DefaultMeta)
        assert form.meta.locales == ['fr']
        assert hasattr(form.meta, 'model')
        assert hasattr(form.meta, 'csrf')

        assert form.meta.foo == 9
        # Create a side effect on the base meta.
        SomeForm.Meta.foo = 12
        assert other_form.meta.foo == 12
        assert form.meta.foo == 12
