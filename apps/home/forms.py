# _*_ coding:utf-8 _*_
# __Author__： zizle
from django.forms import ModelForm, ModelChoiceField
from .models import NewsBulletin, Advertisement, NormalReport
from user.models import User


# 新闻公告文件类型上传的Form
class NewsBulletinForm(ModelForm):
    creator = ModelChoiceField(queryset=User.objects.all(), empty_label=None)

    class Meta:
        model = NewsBulletin
        fields = '__all__'


# 广告轮播数据上传的Form
class AdvertisementForm(ModelForm):
    creator = ModelChoiceField(queryset=User.objects.all(), empty_label=None)

    class Meta:
        model = Advertisement
        fields = '__all__'


# 上传常规报告的Form
class NormalReportForm(ModelForm):
    class Meta:
        model = NormalReport
        fields = '__all__'
