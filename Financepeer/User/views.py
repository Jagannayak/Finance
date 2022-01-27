from django.shortcuts import render
from Financepeer.basefunctions import *
# Create your views here.
class LogOut(View):	
    def post(self,request): 
        return HttpResponse(dumps({"message": "post method not allowed", "status": "failed", "code": 405, "callback": type(self).__name__}))
    def get(self, request):
        user_name = ""
        response = {"status": "failed", "code":401, "callback":type(self).__name__}
        try:
            response.update({"message":"Enter token"})
            if 'HTTP_TOKEN' in request.META and request.META['HTTP_TOKEN'] != "":
                response.update(self.userLogout(request.META['HTTP_TOKEN'],response))
        except Exception as e:
            response.update({"message":"Internal Server Error", "error":str(e)})
        return JsonResponse(response)

    def userLogout(self, token, response):
        dbcursor.users.update_one({"token":token},{"$set":{"token":""}})
        response.update({"message":"Successfully updated", "code":200, "status":"success"})
        return response 