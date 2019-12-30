# _*_ coding:utf-8 _*_
# __Author__： zizle
from django.forms import ModelForm
from .models import MarketAnalysis


# 上传市场分析的Form
class MarketAnalysisForm(ModelForm):
    class Meta:
        model = MarketAnalysis
        fields = '__all__'
