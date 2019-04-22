from django.shortcuts import render
import json
from django.core.paginator import Paginator

# Our App imports:
from core.forms import PleaseSearchForm, CityFilterForm, CountyFilterForm, CategoryFilterForm, SecondaryFilterForm, LuckySearchForm
from core.models import PleaseSearch, LuckySearch
from simple_salesforce import SalesforceAPI
from .super_salesforce import supersf

from pprint import pprint
from django.shortcuts import redirect

from .super_detail_salesforce import superDetailsf

# Create your views here.


def index(request):
    """View function for home page of site."""
    """ url = "/services/data/v45.0/" """
    a = "query?q=SELECT+ID,+Name,+CEF_Category__c,+Website,+Eligibility_Criteria__c,+Imported_Phone__c,+Company_Email__c,+Description_Short__c+FROM+Account"
    b = "+WHERE+"
    x = "Deactivated__c=FALSE"
    y= "+ORDER+BY+Website+NULLS+LAST"
    #+LIMIT+3"

    if request.method == 'GET':

        city_form = CityFilterForm(request.GET)
        if city_form.is_valid():
            city_string = city_form.ingest()
            print("printing city string")
            print(city_string)

        #if 'clear' in request.GET:
            #county_form = CountyFilterForm(request.GET)
            #category_form = CategoryFilterForm(request.GET)
            #city_form = CityFilterForm()
        
        county_form = CountyFilterForm(request.GET)
        if county_form.is_valid():
                county_string = county_form.ingest()
                print("printing county string")
                print(county_string)
        
        # if 'clear' in request.GET:
        #     #category_form = CategoryFilterForm(request.GET)
        #     #city_form = CityFilterForm(request.GET)
        #     county_form = CountyFilterForm()    

        category_form = CategoryFilterForm(request.GET)
        if category_form.is_valid():
            category_string = category_form.ingest()
            print("printing category string")
            print(category_string)

        #if 'clear' in request.GET:
            #city_form = CityFilterForm(request.GET)
            #county_form = CountyFilterForm(request.GET)
            #category_form = CategoryFilterForm()
        
        secondary_form = SecondaryFilterForm(request.GET)
        if secondary_form.is_valid():
            secondary_string = secondary_form.ingest()
            print("printing secondary string")
            print(secondary_string)

        #if 'clear' in request.GET:
            #city_form = CityFilterForm(request.GET)
            #county_form = CountyFilterForm(request.GET)
            #secondary_form = SecondaryFilterForm()

        lucky_form = LuckySearchForm(request.GET)
        if lucky_form.is_valid():
            lucky_string = lucky_form.ingest()
            print("printing lucky string")
            print(lucky_string)


        
        soqlkv = a+b+county_string+city_string+category_string+secondary_string+lucky_string+x+y
        

    data1 = supersf(soqlkv)
    pprint(data1)
    data1 = data1['records'] # this is now a list
    
#printable = data1["records"][1]["Name"]



    context = {
        #'printable': printable,
        'records': data1,
        'county_form': county_form,
        'city_form': city_form,
        'category_form': category_form,
        'secondary_form': secondary_form,
        'lucky_form': lucky_form
        }   

    # Render the HTML template index.html with the data in the context variable
    response = render(request, 'index.html', context=context)
    return response


def city_search(request):
    
    if request.method == 'GET':
        city_form = PleaseSearchForm(request.GET)
        city_form.initial={'Cities': 'Any city'}
        
        
        if city_form.is_valid():
            # city = city_form.save(commit=False)
            cities = str(city_form.cleaned_data.get('Cities'))[1:-1]
            categories = str(city_form.cleaned_data.get('Categories'))[1:-1]
            counties = str(city_form.cleaned_data.get('Counties'))[1:-1]
            a = "/services/data/v45.0/query?q=SELECT+ID,+CEF_Category__c,+Name,+Website,+Imported_Phone__c,+Company_Email__c,+Description_Short__c+FROM+Account"
            b = "+WHERE+"
            c = "City_Served__c+includes("
            d = ")+AND+"
            e = "CEF_Category__c+includes("
            f = ")+AND+"
            g = "County_Served__c+includes("
            h = ")+AND+"
            x = "Deactivated__c=FALSE"


            if 'Any city' in city_form.cleaned_data.get('Cities'):
                print ("Don't limit by city!")
                c = ""
                cities = ""
                d = ""
            if 'Any category' in city_form.cleaned_data.get('Categories'):
                print ("Don't limit by category!")
                e = ""
                categories = ""
                f = ""
            if 'Any county' in city_form.cleaned_data.get('Counties'):
                print ("Don't limit by county!")
                g = ""
                counties = ""
                h = ""
 
            print(a+b+c+cities+d+e+categories+f+g+counties+h+x)
            #print(a+b+c+cities+d+e+categories+f+g+counties+h+x)
            print(cities, categories, counties)
            return render(request, 'city-search.html', {
                 'city_form': city_form,
            })
    
    

    else:
        city_form = PleaseSearchForm()
            
    return render(request, 'city-search.html', {
        'city_form': city_form,
    })

def json_call(request):
    soqlkv = 'q=SELECT+Name,+Eligibility_Criteria__c,+CEF_Category__c,+Website,+Imported_Phone__c,+Company_Email__c,+Description_Short__c,+ID,+Secondary_Tags__c+FROM+Account+WHERE+Deactivated__c+=+FALSE+ORDER+BY+Website+NULLS+LAST'
    #+AND+CreatedDate>2019-04-15T00:00:00Z'
    
    data1 = supersf(soqlkv)

    pprint(data1["records"][1]["Name"])

    printable = data1["records"][1]["Name"]


    data1 = data1['records'] # this is now a list
    paginator = Paginator(data1, 20)

    page = request.GET.get('page')
    pdata1 = paginator.get_page(page)
    context = {
        'records': pdata1,
    }

    return render(request, 'json-call.html', context=context)

def json_detail(request, id):
    soqlkv = id

    detail1 = superDetailsf(soqlkv)

    context = {
        'details': detail1,
    }
    return render(request, 'json-detail.html', context=context)