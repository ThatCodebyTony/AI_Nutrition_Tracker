from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from main import detect_food

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        
        # Get food detection results
        results = detect_food(fs.path(filename))
        
        return JsonResponse({
            'uploaded_file_url': uploaded_file_url,
            'results': results
        })
    return render(request, 'food_detector/upload.html')