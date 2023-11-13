from django.urls import path
from .views import index , upload_image , results
# from .api_utils import query

urlpatterns = [

    path('',index, name= 'index'),
    path('upload_image/',upload_image , name='upload_image'),
    # path('query/',query , name='query_endpoint'),
    path('results/', results, name='results'),
    
]