from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import Person
from account.serializers import TabPersonSerializer


"""SEARCH BY MATRIMONY ID"""
@api_view(['GET'])
def delete_all_items(request):
    logged_matrimony_id=request.GET['matrimony_id']
    search_matrimony_id=request.GET['mid']
    try:
        logged_user=Person.objects.get(matrimony_id=logged_matrimony_id)
    except Exception as e:
        return Response({"message":"Invalid matrimony id"},status=400)
    try:
        search_mid=Person.objects.get(matrimony_id=search_matrimony_id)
    except Exception as e:
        return Response({"message":"Invalid matrimony id"},status=400)
    if logged_user.gender!=search_mid.gender:
        serializer=TabPersonSerializer(search_mid, context={'matrimony_id':logged_matrimony_id},many=False)                         
        return Response(serializer.data)
    else:
        return Response({},status=200)
    
    
    
"""SEARCH BY ANY THING"""   
@api_view(['GET'])
def search_by_matrimonyid(request):
    logged_matrimony_id=request.GET['matrimony_id']
    search_matrimony_id=request.GET['mid']
    try:
        logged_user=Person.objects.get(matrimony_id=logged_matrimony_id)
    except Exception as e:
        return Response({"message":"Invalid matrimony id"},status=400)
    try:
        search_mid=Person.objects.get(matrimony_id=search_matrimony_id)
    except Exception as e:
        return Response({"message":"Invalid matrimony id"},status=400)
    if logged_user.gender!=search_mid.gender:
        serializer=TabPersonSerializer(search_mid, context={'matrimony_id':logged_matrimony_id},many=False)                         
        return Response(serializer.data)
    else:
        return Response({},status=200)
   
