from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.contrib.staticfiles import finders
from .utils import convert
from PIL import Image

def index(request):
    return render(request, 'index.html')

def process_image(request):
    if request.method == 'POST':

        palette = [
                    [31, 36, 10],
                    [57, 87, 28],
                    [165, 140, 39],
                    [239, 172, 40],
                    [239, 216, 161],
                    [171, 92, 28],
                    [24, 63, 57],
                    [239, 105, 47],
                    [239, 183, 117],
                    [165, 98, 67],
                    [119, 52, 33],
                    [114, 65, 19],
                    [42, 29, 13],
                    [57, 42, 28],
                    [104, 76, 60],
                    [146, 126, 106],
                    [39, 100, 104],
                    [239, 58, 12],
                    [60, 159, 156],
                    [155, 26, 10],
                    [54, 23, 12],
                    [85, 15, 10],
                    [48, 15, 10]
                ]
        
        if 'image' in request.FILES:

            uploaded_file = request.FILES['image']
            
            img = Image.open(uploaded_file)
            img_name = uploaded_file.name

            processed_img = convert(img, palette, img_name)

            response = HttpResponse(content_type="image/png")
            processed_img.save(response, "PNG")

            return render(request, 'index.html')
       
        else:
            placeholder_path = finders.find('img_proc/img/placeholder.JPG')

            img = Image.open(placeholder_path)
            img_name = 'placeholder.JPG'
            processed_img = convert(img, palette, img_name)

            response = HttpResponse(content_type="image/png")
            processed_img.save(response, "PNG")

            return render(request, 'index.html')


    return HttpResponse('Please upload an image.')