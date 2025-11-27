document.addEventListener('DOMContentLoaded', function() {

  // ---------------- CSRF Token 가져오기 ----------------
  function getCookie(name) {
      let cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          const cookies = document.cookie.split(';');
          for (let i=0; i<cookies.length; i++) {
              const cookie = cookies[i].trim();
              if (cookie.substring(0, name.length+1) === (name+'=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length+1));
                  break;
              }
          }
      }
      return cookieValue;
  }
  const csrftoken = getCookie('csrftoken');

  // ---------------- 지도 초기화 ----------------
  const mapContainer = document.getElementById('map');
  const mapOption = {
      center: new kakao.maps.LatLng(37.5665, 126.9780), // 서울 기준
      level: 5
  };
  const map = new kakao.maps.Map(mapContainer, mapOption);

  // 커스텀 마커 이미지
  const IMAGE_SRC = '/static/equipment/img/pin.png'; 
  const IMAGE_SIZE = new kakao.maps.Size(32, 48);   
  const IMAGE_OPTION = {offset: new kakao.maps.Point(16, 48)}; 
  const markerImage = new kakao.maps.MarkerImage(IMAGE_SRC, IMAGE_SIZE, IMAGE_OPTION);

  // 클릭한 위치를 표시할 마커
  let selectMarker = null;

  // 지도 클릭 이벤트
  kakao.maps.event.addListener(map, 'click', function(mouseEvent){
      const latlng = mouseEvent.latLng;

      if(!selectMarker){
          selectMarker = new kakao.maps.Marker({
              map: map,
              position: latlng,
              image: markerImage
          });
      } else {
          selectMarker.setPosition(latlng);
      }

      document.getElementById('latitude').value = latlng.getLat().toFixed(6);
      document.getElementById('longitude').value = latlng.getLng().toFixed(6);
      console.log(`좌표 자동 입력: ${latlng.getLat().toFixed(6)}, ${latlng.getLng().toFixed(6)}`);
  });

  // ---------------- DB 마커 가져오기 ----------------
  fetch('/restaurants/')
      .then(res => res.json())
      .then(data => {
          data.forEach(r => {
              const lat = parseFloat(r.latitude);
              const lng = parseFloat(r.longitude);
              if(!isNaN(lat) && !isNaN(lng)){
                  const marker = new kakao.maps.Marker({
                      map: map,
                      position: new kakao.maps.LatLng(lat, lng)
                  });
                  kakao.maps.event.addListener(marker, 'click', function(){
                      const infoWindow = new kakao.maps.InfoWindow({
                          content: `<div><strong>${r.name}</strong><br>${r.memo || ''}</div>`
                      });
                      infoWindow.open(map, marker);
                  });
              }
          });
      })
      .catch(err => console.error('Fetch Error:', err));

  // ---------------- 폼 제출 ----------------
  const form = document.getElementById('restaurantForm');
  if(form){
      form.addEventListener('submit', function(e){
          e.preventDefault();

          const name = document.getElementById('name').value.trim();
          const menu = document.getElementById('menu').value.trim();
          const price = parseFloat(document.getElementById('price').value) || 0;
          const location = document.getElementById('location').value.trim();
          const memo = document.getElementById('memo').value.trim(); // 빈 문자열 허용
          const latitude = parseFloat(document.getElementById('latitude').value) || null;
          const longitude = parseFloat(document.getElementById('longitude').value) || null;

          // 최소 필수 체크
          if(!name || !menu || !location){
              alert("이름, 메뉴, 위치는 필수 입력입니다.");
              return;
          }

          const data = {name, menu, price, location, memo, latitude, longitude};
          console.log("POST 데이터:", data);

          fetch('/restaurants/', {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json',
                  'X-CSRFToken': csrftoken
              },
              body: JSON.stringify(data)
          })
          .then(async res => {
              let responseData = null;
              try {
                  responseData = await res.json();
              } catch (e) {
                  console.error("서버 응답이 JSON이 아님:", e);
              }

              if (!res.ok) {
                  console.error("❌ 서버 응답 오류:", responseData);
                  throw new Error('등록 실패');
              }

              return responseData;
          })
          .then(res => {
              alert('등록 완료!');
              window.location.href = '/saved/';
          })
          .catch(err => {
              console.error(err);
              alert('등록 중 오류가 발생했습니다.');
          });

      });
  }

});
