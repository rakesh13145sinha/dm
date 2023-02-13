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
@api_view(['POST'])
def search_test(request):
    
    logged_matrimony_id=request.GET['matrimony_id']
    
    
    #data = ast.literal_eval(request.data['nameValuePairs'])
    data = request.data['nameValuePairs']
   
    #data=request.data 
    print(">>>>>>>>>>>>>>>")
    print(data)
    print(">>>>>>>>>>>>>>>")
    try:
        profile=Person.objects.get(matrimony_id=logged_matrimony_id)
    except Exception as e:
        return Response({"message":"Invalid matrimony id"},status=400)
    
    
    _height_list=[
    "3ft 1in","3ft2in","3ft 3in","3ft 4in","3ft 5in","3ft 6in","3ft 7in","3ft 8in","3ft 9in","3ft 10in","3ft 11in","4ft", 
    "4ft 1in","4ft 2in","4ft 3in","4ft 4in","4ft 5in","4ft 6in","4ft 7in","4ft 8in","4ft 9in","4ft 10in","4ft 11in","5ft" , 
    "5ft 1in","5ft 2in","5ft 3in","5ft 4in","5ft 5in","5ft 6in","5ft 7in","5ft 8in","5ft 9in","5ft 10in","5ft 11in","6ft",
    "6ft 1in","6ft 2in","6ft 3in","6ft 4in","6ft 5in","6ft 6in","6ft 7in","6ft 8in","6ft 9in","6ft 10in","6ft 11in","7ft",
    "7ft 1in","7ft 2in","7ft 3in","7ft 4in","7ft 5in","7ft 6in","7ft 7in","7ft 8in","7ft 9in","7ft 10in","7ft 11in","8ft"
        
        ]
    
    _index={"min_height":_height_list.index(data['min_height']),
            "max_height":_height_list.index(data['max_height'])
            }
    
    #base filter query
    query=~Q(gender=profile.gender,status=False )
    #gender=~Q(gender=profile.gender,status=False )
    

    
    
   
   
    # q_list=[]
    # h_and_age=Q(
    #     height__in=[i for i in _height_list[ _index['min_height']:_index['max_height'] ] ],
    #          dateofbirth__range=(data['min_age'],data['max_age'] )
    # )
    query=~Q(gender=profile.gender,status=False)  & Q(
                height__in=[i for i in _height_list[ _index['min_height']:_index['max_height'] ] ],
                dateofbirth__range=(data['min_age'],data['max_age'] )
                )
                
               
                
                
               
            
    # q_list.append(gender)
    # q_list.append(h_and_age)
    
    if data['country']!="Any":
        country=Q(country__in=data['country'].split(","),)
        #query=query & country 
        query=query.add(country,Q.AND)
        #q_list.append(country)
    if data['state']!="Any":
        state=Q(state__in=data['state'].split(","))
        #q_list.append(state)
        #query=query & state
        query=query.add(state,Q.AND)
    if data['city']!="Any":
        city=Q(city__in=data['city'].split(","))
        #q_list.append(city)
        #query=query & city
        query=query.add(city,Q.AND)
        
        
        
    #for any field
   
    
    
    #matrital status
    if data['marital_status']!="Any":
        marital_status=Q(marital_status__in=data['marital_status'].split(","))
        query=query & marital_status  #(country,Q.AND)
    if data['mother_tongue']!="Any":
        mother_tongue=Q(mother_tongue__in=data['mother_tongue'].split(","))
        query=query & mother_tongue
    if data['physical_status']!="Any":
        physical_status=Q(physical_status__in=data['physical_status'].split(","))
        query=query & physical_status
       
    # #profession base filter
    
    if data['occupation']!="Any":
        occupation=Q(occupation__in=data['occupation'].split(","))
        query=query & occupation
    if data['qualification']!="Any":
        qualification=Q(qualification__in=data['qualification'].split(","))
        query=query & qualification
    
    if data['min_income']!="Any":
        annual_income=Q(annual_income__startswith=data['min_income'])
        #query.add(annual_income,Q.AND)
        query=query & annual_income
        
    if data['max_income']!="Any":
        annual_income=Q(annual_income__startswith=data['max_income'])
        #query.add(annual_income,Q.AND)
        query=query & annual_income
    
    #religious base filter
    
    if data['religion']!="Any":
        religion=Q(religion__in=data['religion'].split(","))
        query=query & religion
    if data['caste']!="Any":
        caste=Q(caste__in=data['caste'].split(","))
        query=query & caste
    if data['dosham']!="Any":
        dosham=Q(dosham__in=data['dosham'].split(","))
        query=query & dosham
    if data['star']!="Any":
        star=Q(star__in=data['star'].split(","))
        query=query & star
    
    
    
    # #profession base filter
    
    if data['occupation']=="Any":
        occupation=Q(occupation__isnull=False)& ~Q(gender=profile.gender)
        query=query & occupation
        #query.add(occupation,Q.AND)
    if data['qualification']=="Any":
        qualification=Q(qualification__isnull=False)& ~Q(gender=profile.gender)
        query=query & qualification
    if data['min_income']=="Any":
        annual_income=Q(annual_income__isnull=False)& ~Q(gender=profile.gender)
        query=query & annual_income
    
    #religious base filter
    
    if data['religion']=="Any":
        religion=Q(occupation__isnull=False)& ~Q(gender=profile.gender)
        query=query & religion
    if data['caste']=="Any":
        caste=Q(caste__isnull=False)& ~Q(gender=profile.gender)
        query=query & caste
    if data['dosham']=="Any":
        dosham=Q(dosham__isnull=False)& ~Q(gender=profile.gender)
        query=query & dosham
    if data['star']=="Any":
        star=Q(star__isnull=False)& ~Q(gender=profile.gender)
        query=query & star#(star,Q.AND)
  
    if data['marital_status']=="Any":
        marital_status=Q(marital_status__isnull=False)& ~Q(gender=profile.gender)
        query=query & marital_status
    if data['mother_tongue']=="Any":
        mother_tongue=Q(mother_tongue__isnull=False)& ~Q(gender=profile.gender)
        query=query & mother_tongue
    if data['physical_status']=="Any":
        physical_status=Q(physical_status__isnull=False) & ~Q(gender=profile.gender)
        query=query & physical_status

    if data['country']=="Any":
        country=Q(country__isnull=False)& ~Q(gender=profile.gender)
        query=query & country
    if data['state']=="Any":
        state=Q(state__isnull=False)& ~Q(gender=profile.gender)
        query=query & state
    if data['city']=="Any":
        city=Q(city__isnull=False)& ~Q(gender=profile.gender)
        query=query & city
    
    
    
    
     
    response={}
    
    #print(query)
   
    # r_profile=Person.objects.filter(reduce(operator.and_, q_list))
    r_profile=Person.objects.filter(query).only('id').order_by('-reg_date')
    #print(r_profile)
    for r_pro in r_profile:
       
        response[r_pro.id]={
            "matrimony_id":r_pro.matrimony_id,
            "profileimage":[{"image":r_pro.profilemultiimage_set.latest('id').files.url if r_pro.profilemultiimage_set.all() else None}],
            "height":r_pro.height,
            "dateofbirth":r_pro.dateofbirth,
            "gender":r_pro.gender,
            "name":r_pro.name,
            "phone_number":r_pro.phone_number,
            "occupation" :r_pro.occupation,
            "city":r_pro.city,
            "state":r_pro.state,
            "qualification":r_pro.qualification ,
            "active_plan":r_pro.active_plan
            
        }
        response[r_pro.id].update(connect_status(logged_matrimony_id,r_pro.matrimony_id))
    
    
    return Response(response.values(),status=200)    
    
    

    



    