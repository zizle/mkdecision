# _*_ coding:utf-8 _*_
# __Author__： zizle
from django.forms import ModelForm
from .models import MarketAnalysis, SearchReport, TopicSearch, InvestPlan, HedgePlan


# 上传市场分析的Form
class MarketAnalysisForm(ModelForm):
    class Meta:
        model = MarketAnalysis
        fields = '__all__'


# 上传调研报告的Form
class SearchReportForm(ModelForm):
    class Meta:
        model = SearchReport
        fields = '__all__'


# 上传专题研究的Form
class TopicSearchForm(ModelForm):
    class Meta:
        model = TopicSearch
        fields = '__all__'


# 上传投资方案的Form
class InvestPlanForm(ModelForm):
    class Meta:
        model = InvestPlan
        fields = '__all__'


# 上传套保方案的Form
class HedgePlanForm(ModelForm):
    class Meta:
        model = HedgePlan
        fields = '__all__'
