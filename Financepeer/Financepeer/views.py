from .basefunctions import *


# def login(request):
#     return render(request, "login.html")

def default(request):
    response = {}
    try:
        dbcursor.users.insert_one({"userName":"Nayak", "password":"45f238b0ebc278486948ab92322d412b4f91ed17ee80fc9ad13433dc6c7ce035","mailId":"plprupesh@gmail.com", "status":"Active"})
        response.update({"message":"Success"})
    except Exception as e:
        response.update({"message":"Internal Server Error", "error":str(e)})
    return JsonResponse(response)

class Login(View):
    def get(self, request):
        return render(request, "login.html")
        # return redirect("login.html", permanent=True)


    def post(self,request):
        response={"message":"","callback":type(self).__name__,"status":"failed","code":400}
        try:
            response.update({"message":"please enter userName"})
            if "userName" in request.POST and request.POST['userName'] !='':
                response.update({"message":"please enter password"})
                if "password" in request.POST and request.POST['password'] !='':
                    response.update(self.user_Login(request.POST['userName'],request.POST['password'],response, request))

        except KeyboardInterrupt as error: response.update({"message":"Internal Server Error", "error":str(error), "code": 500})          
        except Exception as error: 
            response.update({"message":"Internal Server Error","error":str(error), "code":501})
        # records_logs(request, response)
        return JsonResponse(response)

    def user_Login(self,userName,password,response, request):
        userName= userName.strip("")
        print("user_name", userName)
        
        user_Details=loads(dumps(dbcursor.users.find_one({"$or":[{"userName":userName.title(),"password":hash_password(password)},{"mailId":userName,"password":hash_password(password)}]},{"_id":0})))      
        print("user_Details", user_Details)  
        response.update({"message":"Incorrect User Name or Password", "code":401, "status":"failed"})
        if user_Details:
            response.update({"message":"Statuc Inactive", "code":401, "status":"failed"})
            if user_Details['status'] == "Active":
                print("True")
                session_key = str(uuid4()).replace("-","")
                dbcursor.users.update_one({"userName":user_Details['userName']},{"$set":{"token":""}})
                dbcursor.users.update_one({"userName":user_Details['userName']},{"$set":{"token":session_key}})
                response.update({"message": "Successfully Login","status": "success","code":200, "token":session_key}) 
        return response

########################### file upload render ######################

def file_upload(request):
    print("hiii")
    fileData = loads(dumps(dbcursor.fileData.find({},{"_id":0})))
    return render(request, "fileUpload.html",{"fileData":fileData})

##################### file upload ################
class FileUpload(View):
    def post(self, request):
        response = {"status":"failed", "code":400, "callback":'FileUplod'}
        print(request.META['HTTP_TOKEN'])
        # print(request.FILES)
        try:
            response.update({"message":"Enter token"})
            if 'HTTP_TOKEN' in request.META and request.META['HTTP_TOKEN']:
                tokenCheck = verifyToken(request.META['HTTP_TOKEN'], response)
                print("tokenCheck", tokenCheck)
                if tokenCheck['code']==200:
                    response.update({"message":"Upload File"})
                    if 'file' in request.FILES and request.FILES['file'] != "":
                        response.update(self.processData(request.META['HTTP_TOKEN'], request.FILES['file'], response))
        except Exception as e:
            response.update({"message":"Internal Server Error", "error":str(e)})
        return JsonResponse(response)
    
    def processData(self, token, file1, response):
        # print("sfhsdjkhgsdkjb", file1.read())
        # f = open(file, "r")
        
        a = file1.read()
        data = json.loads(a)
        # print("dataa", data)
        print("dataa", data[0])
        # print(f.read())
        dbcursor.fileData.insert_many(data)
        # fileData = pd.read_json(file1.read())
        # print("fileData", fileData)
        # data = pd.DataFrame(fileData)
        # print("data",data)
        response.update({"message":"success"})
        return response


    