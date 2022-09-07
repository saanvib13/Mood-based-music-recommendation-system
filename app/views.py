from multiprocessing import context
from django.shortcuts import render
from django.http import HttpResponse
import pickle
from tqdm import tqdm
import numpy as np
from datetime import datetime
from app.models import Contact
from django.contrib import messages

# Create your views here.

def index(req):
    #if we want to add context to our templates from views
    # context={
    #     # "var1":"my name is saanvi"
    #     # here we'll send values fetched from our model
    # }
    # return render(req,'index.html',context)
    return render(req,'index.html')
    # return HttpResponse("<h1>home page</h1>") #initial



def about(req):
    # return HttpResponse("<h1>This is about page</h1>")
    return render(req,'about.html')

def contact(req):
    if req.method =="POST":
        name=req.POST.get('name')
        email=req.POST.get('email')
        desc=req.POST.get('desc')
        contact=Contact(name=name,email=email,desc=desc,date=datetime.today())
        contact.save()
        messages.success(req,'Your message has been sent!')
    return render(req,'contact.html')

def output(req):
    name=req.GET.get('sname')
    with open(r'C:\Users\Del\cpython-summer training\training project\model1.pkl' , 'rb') as f:
        lr = pickle.load(f)

    def recommend(dataset, songs, amount=10):
        distance = []
        song = dataset[(dataset.name.str.lower() == songs.lower())].head(1).values[0]
        rec = dataset[dataset.name.str.lower() != songs.lower()]
        for songs in tqdm(rec.values):
            d = 0
            for col in np.arange(len(rec.columns)):
                if not col in [1, 6, 12, 14, 18]:
                    d = d + np.absolute(float(song[col]) - float(songs[col]))
            distance.append(d)
        rec['distance'] = distance
        rec = rec.sort_values('distance')
        columns = ['artists', 'name']
        return rec[columns][:amount]

    recommendations=recommend(lr,name, 10)

    artists=recommendations["artists"].values
    name_s=recommendations["name"].values

    return render(req,'index.html',{"artist":artists, "name":name_s})
    