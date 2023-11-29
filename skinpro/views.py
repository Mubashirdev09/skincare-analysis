from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Imagemodel
from .api_utils import query, generate_summary
def index(request):
    return render(request,"../templates/index.html")


def upload_image(request):
    if request.method == 'POST':
        image = request.FILES['image']
        new_image = Imagemodel(image=image)
        new_image.save()
        image_PATH = new_image.image.url[1:]

        query_data = query(image_PATH)

        request.session["query_data"] = query_data
        request.session['image'] = image_PATH[7:]
        # print("results",query_data)

        return redirect('results')

def results(request):
    # Get the results from the query string or session (adjust as needed)
    query_data = request.session.get("query_data", None)
    image_path = request.session.get("image", None)
    print(image_path)

    # Generate a summary using your language model
    summary_data = generate_summary(query_data)
    print(summary_data)

    return render(request, "results.html", {'results': query_data, 'image_path': image_path, 'summary_data': summary_data})

