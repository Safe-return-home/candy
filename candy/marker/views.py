from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Marker, Comment

# 지도 기본


def marker_view(request):
    # 기본 페이지
    if request.method == 'GET':
        return render(request, 'marker/marker.html', {})
    # 지도 클릭 (마커 리스트 + 기본 페이지)
    elif request.method == 'POST':
        status = int(request.POST.get('status', 0))
        latitude = float(request.POST.get('latitude', 33.450701))
        longitude = float(request.POST.get('longitude', 126.570667))
        filtered_markers = Marker.objects.filter(
            latitude__range=(latitude - 0.001, latitude + 0.001),
            longitude__range=(longitude - 0.001, longitude + 0.001)
        )
        return render(request, 'marker/marker.html', {"markers": filtered_markers, "status": status})

# 지도 상세


def marker_detail_view(request, pk):
    marker = Marker.objects.get(pk=pk)
    # 댓글 작성
    if request.method == 'POST':
        user = request.user
        body = request.POST.get('body')
        Comment.objects.create(
            marker=marker,
            user=user,
            body=body
        )
        return redirect('marker:marker_detail', pk=pk)
    # 기본 페이지
    comments = marker.comments.all()
    print(comments)
    return render(request, 'marker/marker-detail.html', {"marker": marker, "comments": comments})

# 지도 작성 (미완성)


def marker_edit_view(request):
    # 기본 페이지
    if request.method == 'GET':
        return render(request, './marker/marker-edit.html', {})
    # 작성 클릭 시
    if request.method == 'POST':
        user = request.user
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        street_lamp = request.POST.get('street_lamp')
        population = request.POST.get('population')
        rating = request.POST.get('rating')
        body = request.POST.get('body')
        image = request.POST.get('image')

        # 도로명 주소 추출
        url = f"https://dapi.kakao.com/v2/local/geo/coord2address.json?x={longitude}&y={latitude}"
        headers = {'Authorization': f'KakaoAK 1301c1e0e19f2a3c5b9ee4a72d7b83ef'}
        data = requests.get(url, headers=headers).json()
        address = data['documents'][0]['road_address']['address_name']

        Marker.objects.create(
            user=user,
            address=address,
            latitude=latitude,
            longitude=longitude,
            street_lamp=street_lamp,
            population=population,
            rating=rating,
            body=body,
            image=image
        )
        return redirect('marker:markers')

# police 조회


def marker_police_view(request):
    return render(request, 'marker/police.html')

def marker_detail_delete(request, pk):
    #marker_delete=get_object_or_404(Marker, pk=pk)
    #marker_delete = Marker.objects.get(pk=pk)
    try:
        marker_delete = Marker.objects.get(pk=pk)
        marker_delete.delete()
    except Marker.DoesNotExist:
        marker_delete = None
    return redirect('marker:markers')

