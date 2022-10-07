states=["Andhra Pradesh","Telangana","Odisa",'Bihar','Madhay Pradesh','Manipur','Assam','West Bangal',
       'Jharkhand','Gujrat','Maharashtra','Kerala','Tamil Nadu','Sikim','Jammu & Kashmir','Delhi','Rajsthan',
       'Goa','Nagaland','Uttar Padesh','Panjab','Himacha Pradesh','Chhatishgarh']

telangana=["Hyderabad","Ranga Reddy","Nizamabad","Khammam","Karimnagar","Adilabad",
        "Mahbubnagar","Medak","Nalgonda","Warangal","Ramagundam","Suryapet","Miryalaguda","Jagtial"]
andhara=['Visakhapatnam', 'Vijayawada', 'Krishna', 'Guntur', 'Nellore', 'Kurnool', 'Kadapa', 'Rajahmundry', 'East Godavari', 
        'Kakinada', 'Tirupati', 'Chittor', 'Eluru', 'West GodavariVisakhapatnam']

# from account.models import Country,State,City
# try:
#     india=Country.objects.get(name="India")
# except Exception as e:
#     india=Country.objects.create(name="India")
# for state in states:
#     get,create=State.objects.get_or_create(name=state,country=india)
#     if get.name=="Telangana":
#         for town in telangana:
            
#             City.objects.get_or_create(name=town,state=get)
#     elif get.name=="Andhra Pradesh":
#         for town in andhara:
#             City.objects.get_or_create(name=town,state=get)
#     else:
#         pass
        