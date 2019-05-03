from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from .models import *
import time

def index(request):
    # form = ImageForm()

    timestamp = int(time.time())            # мне надо придать вес
    three_month = 60*60*24*30*3
    three_month_ago= timestamp-three_month

    concept1 = Concept.objects.get(pk=13)
    print (concept1)
    connection = Connection.objects.filter(concept=concept1)
    print(connection[0].connectionfilm)




    concepts = Concept.objects.all()
    concepts_ext = {}
    for concept in concepts:
        print (concept)
        c = {}
        c['rating'] = 0
        connections = Connection.objects.filter(concept=concept)
        # print (connections)
        for connection in connections:
            #к каждому концепту я прикладываю словарь
            try:
                print (connection.connectionfilm)
                c['rating'] += (connection.connectionfilm.film.year) # год
            except:
                pass
            try:
                vk = (connection.connectionvkpost.post)
                print (vk.date)
                if (vk.date>three_month_ago):
                    c['rating']*=0
                print ('here date')
                # print (datetime.time)
                c['published'] = vk.date
            except:
                pass
            print()
        c['rating']*=concept.k10
        concepts_ext[concept] = c
        # print(concepts_ext[concept]['rating'])
    for s in sorted(concepts_ext.items(),
                    key = lambda k_v: k_v[1]['rating'], reverse = True):
        print (concepts_ext[s[0]], s[0])
        print()




        # concepts_ext[concept] = connections
    # print (concepts_ext)
    # connections = Connection.objects.all()
    # for c in connections:
    #     print (c.strname)

    # print (connections.strname)

    return render(request, 'concept/index.html', {'concepts': concepts})
    # return render(request, 'vkgrab/vkgrab.html',{'len': len_base, 'vk_posts':vk_posts})

