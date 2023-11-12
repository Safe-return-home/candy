from django.shortcuts import render, redirect, get_object_or_404
import requests
from .models import Marker, Comment
from django.core.paginator import Paginator
from django.utils import timezone

def marker_view(request):
    # 기본 페이지
    if request.method == 'GET':
        return render(request, 'marker/marker.html', {})
    # 지도 클릭 (마커 리스트 + 기본 페이지)
    if request.method == 'POST':
        status = int(request.POST.get('status', 1))
        latitude = float(request.POST.get('latitude', 33.450701))
        longitude = float(request.POST.get('longitude', 126.570667))
        filtered_markers = Marker.objects.filter(
            latitude__range=(latitude - 0.002, latitude + 0.002),
            longitude__range=(longitude - 0.002, longitude + 0.002)
        )

        paginator = Paginator(filtered_markers, 3)  # 한 페이지당 3개의 마커 표시
        page_number = request.GET.get('page')  # 현재 페이지 번호 가져오기
        page_markers = paginator.get_page(page_number)  # 해당 페이지에 해당하는 마커 가져오기

        return render(request, 'marker/marker.html', {"markers": page_markers, "status": status})


# 지도 상세
def marker_detail_view(request, pk):
    marker = Marker.objects.get(pk=pk)
    # 댓글 작성
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return redirect('marker:marker_detail', pk=pk)
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
    # 미인증 유저 예외처리
    if not request.user.is_authenticated:
        return redirect('marker:markers')
    # 기본 페이지
    if request.method == 'GET':
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        address = request.GET.get('address')
        print(address)
        data = {
            'lat': lat,
            'lng': lng,
            'address': address,
        }
        return render(request, './marker/marker-edit.html', data)

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
        address = data['documents'][0]['address']['address_name']
        print(address)
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

# 지도 마커 삭제
def marker_detail_delete(request, pk):
    # marker_delete=get_object_or_404(Marker, pk=pk)
    # marker_delete = Marker.objects.get(pk=pk)
    try:
        marker_delete = Marker.objects.get(pk=pk)
        if not request.user.pk == marker_delete.user.pk:
            redirect('marker:marker_detail', pk=pk)
        marker_delete.delete()
    except Marker.DoesNotExist:
        marker_delete = None
    return redirect('marker:markers')

# 지도 마커 수정 (get)
def marker_detail_update_page(request, pk):
    try:
        marker_update = get_object_or_404(Marker, pk=pk)
        if not request.user.pk == marker_update.user.pk:
            redirect('marker:marker_detail', pk=pk)
    except Marker.DoesNotExist:
        marker_update=None
    return render(request,'marker/update.html', {'marker':marker_update})

# 지도 마커 수정 (post)
def marker_detail_update(request,pk):
    marker_update=get_object_or_404(Marker, pk=pk)
    # marker_update.address = request.POST['address']
    marker_update.street_lamp=request.POST['street_lamp']
    marker_update.population=request.POST['population']
    marker_update.rating=request.POST['rating']
    marker_update.body=request.POST['body']
    marker_update.image=request.POST.get('image')
    marker_update.regTime=timezone.now()
    marker_update.save()
    return redirect('marker:marker_detail', pk=pk)
