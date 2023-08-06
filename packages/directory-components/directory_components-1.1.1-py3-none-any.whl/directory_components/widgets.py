from django.utils.safestring import mark_safe
from django.forms import widgets


class RadioSelect(widgets.RadioSelect):
    template_name = 'directory_components/radio.html'
    option_template_name = 'directory_components/radio_option.html'


class CheckboxWithInlineLabel(widgets.CheckboxInput):
    template = """
        <div class="form-field checkbox">
            {input_html}
            <label for="{id}">{label}</label>
        </div>
    """

    def __init__(self, label='', *args, **kwargs):
        self.label = label
        super().__init__(*args, **kwargs)

    def render(self, name, value, attrs=None):
        input_html = super().render(name, value, attrs)
        wrapper_html = self.template.format(
            input_html=input_html, label=self.label, id=attrs['id']
        )
        return mark_safe(wrapper_html)


class CheckboxSelectInlineLabelMultiple(widgets.CheckboxSelectMultiple):
    option_template_name = 'directory_components/checkbox_input_option.html'
    css_class_name = 'form-field checkbox multi'

    def __init__(self, attrs=None):
        super().__init__(attrs=attrs)
        self.attrs['class'] = self.attrs.get('class', self.css_class_name)
