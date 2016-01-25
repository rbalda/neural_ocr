import datetime
import simplejson
from PIL import Image
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from neural_network import neural_ocr

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from neural_network.neural_ocr import predict
import re

default_folder = "media"

def generate_name():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S")

def convert_to_jpeg(file):
    png = Image.open(file)
    png.load()
    background = Image.new("RGB", png.size, (255, 255, 255))
    background.paste(png, mask=png.split()[3]) # 3 is the alpha channel
    background.save(file, 'PNG', quality=80)

@csrf_exempt
def home(request):
    if request.method == "GET":
        return render(request,'index.html')
    else:
        datauri = request.body
        imgstr = re.search(r'base64,(.*)', datauri).group(1)
        name = generate_name()
        output = open("%s/%s.png"%(default_folder,generate_name()), 'wb')
        output.write(imgstr.decode('base64'))
        output.close()
        convert_to_jpeg(output.name)
        p,list = neural_ocr.predict(output.name)
        list = simplejson.dumps(list.tolist())
        response = JsonResponse({'prediccion': p,'porcentajes':list})
        return response

