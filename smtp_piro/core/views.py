from django.shortcuts import render
from accounts.decorator import check_permission

# Create your views here.


@check_permission
def checkbyFunction(request):
    return render(request, 'checkbyFunction.html')


def checkbyHTML(request):
    user = request.user
    return render(request, 'checkbyHTML.html', {'user': user})


def listofLink(request):
    return render(request, 'listofLink.html')