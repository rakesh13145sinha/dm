from rest_framework import serializers
from account.models import Person


class AdminPersonSerializer(serializers.ModelSerializer):
    # profileimage=serializers.SerializerMethodField()
    # connect_status=serializers.SerializerMethodField()
    # album_status=serializers.SerializerMethodField()
   
    
    # def get_profileimage(self,obj):
    #     images=obj.profilemultiimage_set.all()
    #     return [{"image":image.files.url  if image.files else None } for image in images ] 
    # def get_connect_status(self,obj):
    #     status=connect_status(self.context['matrimony_id'],obj.matrimony_id)
    #     return status
    
    # def get_album_status(self,obj):
       
    #     try:
    #         bookmark=Bookmark.objects.get(profile__matrimony_id=self.context['matrimony_id'])
    #         bookmark.album.get(matrimony_id=obj.matrimony_id)
    #         return True
    #     except Exception as e:
    #         return False
    
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
       
    #     representation['height'] =height(instance.height)
        
    #     return representation                                   
                                
    
    class Meta:
        model=Person 
       
        exclude=('user',)