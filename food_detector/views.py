from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from main import detect_food

def upload_image(request):
    if request.method == 'POST' and request.FILES['image']:
        file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        
        # Get food detection results
        results = detect_food(fs.path(filename))
        
        return render(request, 'food_detector/results.html', {
            'uploaded_file_url': uploaded_file_url,
            'results': results
        })
    return render(request, 'food_detector/upload.html')