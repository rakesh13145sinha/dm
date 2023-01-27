from rest_framework.decorators import api_view
from rest_framework.response import Response
from account.models import FriendRequests, Person
from account.serializers import TabPersonSerializer
from django.db.models import Q



"""check request status"""       
def connect_status(matrimonyid,requestid):
    # assert matrimonyid is None ,"matrimony id can't be None"
    # assert requestid is None ," requested matrimony id can't be None"
    query=Q(
        Q(profile__matrimony_id=matrimonyid,requested_matrimony_id=requestid)
        |
        Q(profile__matrimony_id=requestid,requested_matrimony_id=matrimonyid)
    )
    send_friend_request=FriendRequests.objects.filter(query)
    if send_friend_request.exists():
        return {"connect_status":send_friend_request[0].request_status} 
    else:
        return {"connect_status":"connect"} 





"""SEARCH BY MATRIMONY ID"""
@api_view(['GET'])
def search_by_matrimonyid(request):
    logged_matrimony_id=request.GET['matrimony_id']
    search_matrimony_id=request.GET['requeted_matrimony_id']
    try:
        logged_user=Person.objects.get(matrimony_id=logged_matrimony_id)
    except Exception as e:
        return Response({"message":"Invalid matrimony id"},status=200)
    try:
        search_mid=Person.objects.get(matrimony_id=search_matrimony_id)
    except Exception as e:
        return Response({"message":"Invalid requested matrimony id"},status=200)
    if logged_user.gender!=search_mid.gender:
        serializer=TabPersonSerializer(search_mid, context={'matrimony_id':logged_matrimony_id},many=False)                         
        return Response(serializer.data)
    else:
        return Response({"matrimony_id":None},status=200)
    
    
    
"""SEARCH BY ANY THING"""   
@api_view(['GET'])
def search_test(request):
    logged_matrimony_id=request.GET['matrimony_id']
    data=request.data 
    try:
        profile=Person.objects.get(matrimony_id=logged_matrimony_id)
    except Exception as e:
        return Response({"message":"Invalid matrimony id"},status=400)
    
    _height_list=[
    "3'1''","3'2''","3'3''","3'4''","3'5''","3'6''","3'7''","3'8''","3'9''","3'10''","3'11''","4'0''" , 
    "4'1''","4'2''","4'3''","4'4''","4'5''","4'6''","4'7''","4'8''","4'9''","4'10''","4'11''","5'0''" , 
    "5'1''","5'2''","5'3''","5'4''","5'5''","5'6''","5'7''","5'8''","5'9''","5'10''","5'11''","6'0''",
    "6'1''","6'2''","6'3''","6'4''","6'5''","6'6''","6'7''","6'8''","6'9''","6'10''","6'11''","7'0''",
    "7'1''","7'2''","7'3''","7'4''","7'5''","7'6''","7'7''","7'8''","7'9''","7'10''","7'11''","8'0''"
        
        ]
    
    _index={"min_height":_height_list.index(data['min_height']),"max_height":_height_list.index(data['max_height'])}
    
    

    
    
    
    
    
    
    # base filter query
    query=Q(~Q(gender=profile.gender) & Q(status=True))

    #location query
    location_query=Q(
        Q(city=data['city'])
        &
        Q(state=data['state'])
        &
        Q(country=data['country'])
    )
    query.add(location_query)
    
    #height and age query
    age_and_height=Q( 
                     
        Q(height__in=[i for i in _height_list.range(_index['max_height'],_index['min_height'])])
        &
        Q(dateofbirth__range=(data['min_age'],data['max_age'] ))
        
        
    
                     
                     
                     )
    
    
    query.add(age_and_height)
    #profession base filter
    occupation_based=Q(
        Q(occupation=data['occupation'])
        &
        Q(qualification=data['qualification'])
        &
        Q(job_sector=data['job_sector'])
        &
        Q(annual_income=data['annual_income'])
        
    )
    query.add(occupation_based)
    #religious base filter
    religion_base=Q(
        Q(religion=data['religion'])
               &
         Q(caste=data['caste'])
               &
        Q(dosham=data['dosham'])
               &
        Q(star=data['star'])
        
    )
    query.add(religion_base)
    extrainfo=Q(
        
        Q(physical_status=data['religion'])
               &
         Q(mother_tongue=data['caste'])
               &
        Q(marital_status=data['dosham'])
               
    )
    query.add(extrainfo)
        
    
    
    
        
    response={}
    r_profile=Person.objects.filter(query).order_by('-reg_date')
    for r_pro in r_profile:
        #images=r_pro.profilemultiimage_set.all()
        response[r_pro.id]={
            "matrimony_id":r_pro.matrimony_id,
            "image":r_pro.profilemultiimage_set.latest('id').files.url if r_pro.profilemultiimage_set.all() else None,
            "height":r_pro.height,
            "age":r_pro.dateofbirth,
            "gender":r_pro.gender,
            "name":r_pro.name,
            "phone_number":r_pro.phone_number
            
        }
        response[r_pro.id].update(connect_status(logged_matrimony_id,r_pro.matrimony_id))
    
    return Response(response.values(),status=200)

    

    
    
   
    
    

    
    
    
    
    
    


    
    
    
    
    
   