from django.db import models
import mimetypes
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from hashlib import md5
from .forms import UpdatePassForm, EncryptionPassForm, DecryptionPassForm
from .models import zdna
from .funcs import *
import random
import base64



def index(request):
    context = {}
    context['title'] = 'Z-DNA encryption for updates of encrypted NFT metadata'
    return render(request, 'TPZDNA.html', context)
#
def download(request):
    #fill these variables with real values
    fl_path = r'zdna/downloads/'
    if request.method == 'GET':
        filename = request.GET['md5']
        #‘downloaded_file_name.extension’

        fl = open(fl_path + filename, "rb")
        mime_type = 'application/octet-stream'
        response = HttpResponse(fl.read(), content_type=mime_type)
        response['Content-Disposition'] = "attachment; filename=" + filename + ".metadata"
        return response
#http://71.131.199.119:81/zdna/download?md5=d57147ac784ef3b713220e4e6c8587b7
#
def img(request):
    #fill these variables with real values
    fl_path = r'zdna/images/'
    if request.method == 'GET':
        filename = request.GET['name']
        #‘downloaded_file_name.extension’

        fl = open(fl_path + filename, "rb")
        mime_type = 'image/jpeg'
        response = HttpResponse(fl.read(), content_type=mime_type)
        response['Content-Disposition'] = "inline"
        return response

def encryption(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = EncryptionPassForm(request.POST, request.FILES)
        #nftdata = request.POST['file']
       # nftdata = request.FILES['file'].read()
        # check whether it's valid:
        if form.is_valid():
            nftdata = request.FILES['file'].read()
            md5pass = form.cleaned_data['md5pass']
            randNum = random.randint(0, 4294967295)
            randNum_bytes = randNum.to_bytes(4, "big")
            encrypted_nftdata = xor_l_s(nftdata, randNum_bytes)
            md5nft = md5(encrypted_nftdata).hexdigest()
            akey = zdna.objects.create(randnum=str(randNum), md5pass=md5pass, md5data=md5nft)
            akey.save()

            #write the encrypted NFT metadata to a file
            outfile = open('zdna/downloads/' + md5nft, 'wb+')
            outfile.write(encrypted_nftdata)
            outfile.close()

            # # redirect to a new URL:
            context = {}
            context['title'] = "Your NFT metadata helper data has been created!"

            context['md5'] = md5nft
            return render(request, 'encryption_download.html', context)

        else:
            # nftdata = request.FILES['file']
            # randNum = random.randint(0, 4294967295)
            # randNum_bytes = randNum.to_bytes(4, "big")
            # encrypted_nftdata = xor_l_s(nftdata, randNum_bytes)
            # md5nft = md5(encrypted_nftdata).hexdigest()
            context = {}
            context['title'] = "Something wrong with the form"
            return render(request, 'encryption_download.html', context)

            #return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = EncryptionPassForm()
        return render(request, 'encryption_form.html', {'form': form})


# Create your views here.

def update(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UpdatePassForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            md5pass = form.cleaned_data['md5pass']

            md5newpass = form.cleaned_data['md5newpass']
            md5data = form.cleaned_data['md5data']
            xor2pass = int(form.cleaned_data['xor2pass']).to_bytes(4, 'big')

            target_zdna_pass = zdna.objects.get(md5pass=md5pass, md5data=md5data)

            #update md5pass and randNum
            target_zdna_pass.randnum = str( int.from_bytes(xor(xor2pass, int(target_zdna_pass.randnum).to_bytes(4, 'big')), 'big') )
            target_zdna_pass.md5pass = md5newpass
            target_zdna_pass.save()

            context = {}
            context['title'] = 'Your NFT password has been updated!'
            context['result'] = md5data
            return render(request, 'update_form.html', context)



    # if a GET (or any other method) we'll create a blank form
    else:
        form = UpdatePassForm()
        return render(request, 'update_form.html', {'form': form})

    # context = {}
    # md5pass = request.POST.get('md5pass')
    # nftdata = request.POST.get('nftdata')
    # xor2pass = request.POST.get('xor2pass')
    #
    # if nftdata:
    #     md5data = md5(nftdata).hexdigest()
    #
    # if md5pass and md5data and xor2pass:
    #     context['title'] = 'Z-DNA encryption for updates of encrypted NFT metadata'
    #     context['md5'] = 'md5test values'
    #     context['result'] = 'Encryption updated successfully!'
    #     return render(request, 'encryption_download.html', context)
    # else:
    #     context['title'] = 'Please input your MD5 values of your password and the NFT data'
    #     return render(request, 'update_form.html', context)


def decryption(request):

    if request.method == 'POST':
    # create a form instance and populate it with data from the request:
        form = DecryptionPassForm(request.POST, request.FILES)
        # nftdata = request.POST['file']
        # nftdata = request.FILES['file'].read()
        # check whether it's valid:
        if form.is_valid():
            encrypted_nftdata = request.FILES['file'].read()
            md5data = md5(encrypted_nftdata).hexdigest()
            md5pass = form.cleaned_data['md5pass']


            randNum = random.randint(0, 4294967295)
            randNum_bytes = randNum.to_bytes(4, "big")
            # encrypted_nftdata = xor_l_s(nftdata, randNum_bytes)

            akey = zdna.objects.get(md5pass=md5pass, md5data=md5data)
            randNum = int(akey.randnum)
            randNum_bytes = randNum.to_bytes(4, "big")
            # zdna.randnum
            decrypted_nftdata = xor_l_s(encrypted_nftdata, randNum_bytes)
            md5data = md5(decrypted_nftdata).hexdigest()
            # write the encrypted NFT metadata to a file
            outfile = open('zdna/downloads/' + md5data, 'wb+')
            outfile.write(decrypted_nftdata)
            outfile.close()

            # # redirect to a new URL:
            context = {}
            context['title'] = "Your NFT metadata has been decrypted!"
            context['md5'] = md5data
            context['randNum'] = randNum
            return render(request, 'decryption_download.html', context)

        else:
            # nftdata = request.FILES['file']
            # randNum = random.randint(0, 4294967295)
            # randNum_bytes = randNum.to_bytes(4, "big")
            # encrypted_nftdata = xor_l_s(nftdata, randNum_bytes)
            # md5nft = md5(encrypted_nftdata).hexdigest()
            context = {}
            context['title'] = "Something wrong with the form"
            return render(request, 'decryption_download.html', context)

    # return HttpResponseRedirect('/thanks/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = DecryptionPassForm()
        return render(request, 'decryption_form.html', {'form': form})

#
    context = {}
    nftdata = request.POST.get('nftdata')
    md5data = ""

    if nftdata:
        md5data = md5(nftdata).hexdigest()
    if md5data:
        context['title'] = 'A demonstrating assistance server for the encrypted keyword updating of the NFT metadata without updating of the NFT metadata'
        context['md5'] = 'md5test values'
        context['result'] = 'Encryption updated successfully!'
        return render(request, 'encryption_download.html', context)

    else:
        context['title'] = 'Please upload your encrypted NFT metadata'
        return render(request, 'decryption_form.html', context)
