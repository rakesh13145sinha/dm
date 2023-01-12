from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import Person
from account.serializers import TabPersonSerializer
from django.db.models import Q

"""SEARCH BY MATRIMONY ID"""
@api_view(['GET'])
def search_by_matrimonyid(request):
    logged_matrimony_id=request.GET['matrimony_id']
    search_matrimony_id=request.GET['requeted_matrimony_id']
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
    data=request.data 
    try:
        profile=Person.objects.get(matrimony_id=logged_matrimony_id)
    except Exception as e:
        return Response({"message":"Invalid matrimony id"},status=400)
    
    # base filter query
    query=Q(~Q(gender=profile.gender) & Q(status=True))

    #location query
    location_query=Q(
        Q(city=profile.city)
        |
        Q(state=profile.state)
        |
        Q(country=profile.country)
    )
    query.add(location_query)
    
    #profession base filter
    occupation_based=Q(
        Q(occupation=profile.occupation)
               |
        Q(qualification=profile.qualification)
        |
        Q(job_sector=profile.job_sector)
        |
        Q(annual_income=profile.annual_income)
    )
    query.add(occupation_based)
    #religious base filter
    religion_base=Q(
        Q(religion=profile.religion)
               |
         Q(caste=profile.caste)
               |
        Q(dosham=profile.dosham)
               |
        Q(star=profile.star)
        
    )
        
    
    
    
        
    response={}
    r_profile=Person.objects.filter(query).order_by('-reg_date')
    for r_pro in r_profile:
        images=ProfileMultiImage.objects.filter(profile=r_pro)
        response[r_pro.id]={
            "matrimony_id":r_pro.matrimony_id,
            "image":images[0].files.url if images.exists() else None,
            "height":height(r_pro.height),
            "age":r_pro.dateofbirth,
            "gender":r_pro.gender,
            "name":r_pro.name,
            "phone_number":r_pro.phone_number
            
        }
        response[r_pro.id].update(connect_status(matrimonyid,r_pro.matrimony_id))
    
    return Response(response.values(),status=200)

    
    
   
    
    

    
    
    
    
    
    


    
    
    
    
    
   