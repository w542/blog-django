from django import forms


# 实现摘要 以textarea(多行多列)展示
# 还不懂，需要加强
class PostAdminForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.Textarea, label='摘要', required=False)