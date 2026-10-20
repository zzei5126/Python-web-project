from django.shortcuts import render


def error_400(request, exception=None):
    return render(request, "error.html", {"status": 400, "message": "Yêu cầu không hợp lệ."}, status=400)


def error_403(request, exception=None):
    return render(request, "error.html", {"status": 403, "message": "Truy cập bị từ chối."}, status=403)


def error_404(request, exception=None):
    return render(request, "error.html", {"status": 404, "message": "Không tìm thấy trang bạn yêu cầu."}, status=404)


def error_500(request):
    return render(request, "error.html", {"status": 500, "message": "Có lỗi hệ thống. Vui lòng thử lại sau."}, status=500)
