from django import forms


class EntryForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        label="Tên của bạn",
        strip=True,
        widget=forms.TextInput(attrs={
            "maxlength": 100,
            "placeholder": "Nhập tên của bạn",
            "autocomplete": "name",
        }),
        error_messages={
            "required": "Vui lòng nhập tên của bạn.",
            "max_length": "Tên không được vượt quá 100 ký tự.",
        },
    )
    message = forms.CharField(
        max_length=2000,
        label="Lời nhắn",
        strip=True,
        widget=forms.Textarea(attrs={
            "rows": 5,
            "maxlength": 2000,
            "placeholder": "Bạn muốn để lại điều gì?",
        }),
        error_messages={
            "required": "Vui lòng nhập lời nhắn.",
            "max_length": "Lời nhắn không được vượt quá 2000 ký tự.",
        },
    )
