from django.shortcuts import render

# Create your views here.
def handle_not_found(request, exception):
    
    return render(request, 'not-found.html')


def handle_server_error(request):
    return render(request, 'server-error.html')


def handle_file_not_found(request):
    return render(request, 'file-not-found.html')



