from django.forms.widgets import (
    Input as _Input,
    PasswordInput as _PasswordInput,
    HiddenInput,
    MultipleHiddenInput,
    FileInput as _FileInput,
    ClearableFileInput as _ClearableFileInput,
    Textarea as _Textarea,
    DateInput as _DateInput,
    DateTimeInput as _DateTimeInput,
    TimeInput as _TimeInput,
    Select as _Select,
    SelectMultiple,
    NullBooleanSelect,
    ChoiceWidget,
    DateTimeBaseInput,
    RadioSelect as _RadioSelect,
    CheckboxSelectMultiple as _CheckboxSelectMultiple,
    MultiWidget,
    SplitDateTimeWidget as _SplitDateTimeWidget,
    SplitHiddenDateTimeWidget as _SplitHiddenDateTimeWidget,
    SelectDateWidget as _SelectDateWidget,
)

__all__ = (
    "Input",
    "NumberInput",
    "EmailInput",
    "URLInput",
    "PasswordInput",
    "FileInput",
    "ClearableFileInput",
    "Textarea",
    "DateInput",
    "DateTimeInput",
    "TimeInput",
    "Select",
    "RadioSelect",
    "CheckboxSelectMultiple",
    "SplitDateTimeWidget",
    "SplitHiddenDateTimeWidget",
    "SelectDateWidget",
    "HiddenInput",
    "MultipleHiddenInput",
    "SelectMultiple",
    "NullBooleanSelect",
    "ChoiceWidget",
    "DateTimeBaseInput",
    "MultiWidget",
)


class Input(_Input):
    template_name = "ui/forms/widgets/input.html"


class TextInput(Input):
    input_type = "text"
    template_name = "ui/forms/widgets/text.html"


class NumberInput(Input):
    input_type = "number"
    template_name = "ui/forms/widgets/number.html"


class EmailInput(Input):
    input_type = "email"
    template_name = "ui/forms/widgets/email.html"


class URLInput(Input):
    input_type = "url"
    template_name = "ui/forms/widgets/url.html"


class PasswordInput(_PasswordInput):
    input_type = "password"
    template_name = "ui/forms/widgets/password.html"


class FileInput(_FileInput):
    template_name = "ui/forms/widgets/file.html"


class ClearableFileInput(_ClearableFileInput):
    template_name = "ui/forms/widgets/clearable_file_input.html"


class Textarea(_Textarea):
    template_name = "ui/forms/widgets/textarea.html"


class DateInput(_DateInput):
    template_name = "ui/forms/widgets/date.html"


class DateTimeInput(_DateTimeInput):
    template_name = "ui/forms/widgets/datetime.html"


class TimeInput(_TimeInput):
    template_name = "ui/forms/widgets/time.html"


class Select(_Select):
    template_name = "ui/forms/widgets/select.html"
    option_template_name = "ui/forms/widgets/select_option.html"


class RadioSelect(_RadioSelect):
    template_name = "ui/forms/widgets/radio.html"
    option_template_name = "ui/forms/widgets/radio_option.html"


class CheckboxSelectMultiple(_CheckboxSelectMultiple):
    template_name = "ui/forms/widgets/checkbox.html"
    option_template_name = "ui/forms/widgets/checkbox_option.html"


class SplitDateTimeWidget(_SplitDateTimeWidget):
    template_name = "ui/forms/widgets/splitdatetime.html"


class SplitHiddenDateTimeWidget(_SplitHiddenDateTimeWidget):
    template_name = "ui/forms/widgets/splithiddendatetime.html"


class SelectDateWidget(_SelectDateWidget):
    template_name = "ui/forms/widgets/select_date.html"
