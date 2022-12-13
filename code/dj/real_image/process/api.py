#from website.models import Video #需要建立api的文章模型数据
from rest_framework import serializers #系列化器
from rest_framework.response import Response #构建视图，返回JSON
from rest_framework.decorators import api_view

# class Video(models.Model):
#     title = models.CharField(null=True, blank=True, max_length=300)
#     content = models.TextField(null=True, blank=True)
#     url_image = models.URLField(null=True, blank=True)
#     cover = models.FileField(upload_to='cover_image', null=True)
#     editors_choice = models.BooleanField(default=False)
#     owner = models.ForeignKey(to=UserProfile, related_name='videos', default=1)

#     def __str__(self):
#         return self.title

# class VideoSerializer(serializers.ModelSerializer):
#     title = serializers.CharField(min_length=1)
#     class Meta:
#         model = Video #代表上面的Video模型数据
#         fields = '__all__'
#         # fields = ('title',  'content',)
        # depth = 3

@api_view(['GET', 'POST'])  #装饰器
def video(request):
    video_list = Video.objects.order_by('-id')
    if request.method == 'GET':
    	return "1111111111"
        # serializer = VideoSerializer(video_list, many=True)
        # return Response(serializer.data)