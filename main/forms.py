from django import forms
from .models import Product
from django.utils.html import strip_tags

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'price', 'description', 'thumbnail', 'category', 'is_featured']
        
        widgets = {
            "name": forms.TextInput(attrs={
                "class": "w-full px-4 py-3 rounded-[12px] border border-[var(--silver)] "
                        "focus:outline-none focus:border-[var(--leaf)] "
                        "focus:ring-4 focus:ring-[rgba(13,52,5,.15)]",
                "placeholder": "Enter product name",
            }),
            "price": forms.NumberInput(attrs={
                "class": "w-full px-4 py-3 rounded-[12px] border border-[var(--silver)] "
                        "focus:outline-none focus:border-[var(--leaf)] "
                        "focus:ring-4 focus:ring-[rgba(13,52,5,.15)]",
                "placeholder": "Enter product price",
            }),
            "description": forms.Textarea(attrs={
                "class": "w-full px-4 py-3 rounded-[12px] border border-[var(--silver)] "
                        "focus:outline-none focus:border-[var(--leaf)] "
                        "focus:ring-4 focus:ring-[rgba(13,52,5,.15)]",
                "rows": 4,
                "placeholder": "Enter product description",
            }),
            "thumbnail": forms.URLInput(attrs={
                "class": "w-full px-4 py-3 rounded-[12px] border border-[var(--silver)] "
                        "focus:outline-none focus:border-[var(--leaf)] "
                        "focus:ring-4 focus:ring-[rgba(13,52,5,.15)]",
                "placeholder": "Enter image URL",
            }),
            "category": forms.Select(attrs={
                "class": "w-full px-4 py-3 rounded-[12px] border border-[var(--silver)] "
                        "focus:outline-none focus:border-[var(--leaf)] "
                        "focus:ring-4 focus:ring-[rgba(13,52,5,.15)]",
            }),
            "is_featured": forms.CheckboxInput(attrs={
                "class": "rounded border-gray-300 text-[var(--leaf)] focus:ring-[var(--leaf)]",
            }),
        }

    def clean_name(self):
        name = self.cleaned_data.get('name')
        return strip_tags(name)
    
    def clean_description(self):
        description = self.cleaned_data.get('description')
        return strip_tags(description)