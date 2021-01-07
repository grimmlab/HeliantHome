from django.shortcuts import render

'''
Landing Page
'''
def landing_page(request):
    return render(request,'base/landingpage.html',{})
