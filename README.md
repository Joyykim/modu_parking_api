# parking_api

## Introduction 
- cloning modu parking api project 

## apps
- users
- lots
- parkings

## requirments
Project is created with:
* python 3.8.2
* django 3.0.7
* djangorestframework 3.11.0
* haversine 2.2.0

## urls
- users

POST /users/ 
: 사용자 등록

PUT /users/id 
: 사용자 정보수정

GET /users/id 
: 사용자 세부정보

POST /users/login 
: 사용자 로그인

DELETE /users/logout 
: 사용자 로그인

DELETE /users/deactivate
: 사용자 계정삭제 

GET /bookmark/
: 북마크 리스트

POST /bookmark/
: 북마크 등록 

- lots

POST /lots/
: 주차장 등록

PUT /lots/id
: 주차장 정보수정

GET /lots/id
: 주차장 세부정보

GET /lots/map(action) 
: 주차장 맵뷰역(예: 서울시)

GET /lots/distance_odr
: 주차장 목록 거리순 정렬

GET /lots/price_odr 
: 주차장 목록 가격순 정렬

DELETE /lots/id 
: 주차장 삭제


- parkings

POST /parkings/ 
: 주차 이벤트 생성(주인의 사용내역만)

GET  /parkings/
: 유저의 주차 내역 목록(총비용, 주차장 정보)

GET  /parkings/id
: 주차세부정보 (총비용, 주차장 정보) 

PUT  /parkings/id/
: 주차시간을 추가(추가결제)


## features
- GPS 트래킹 (GPS tracking)<br>
: 사용자의 위치를 찾고 가까운 주차장까지의 위치를 보여줍니다.<br>
: This technology allows to find the location of the car and determine the distance to the nearest parking lot.<br>

- 예약 시스템 (Booking)<br>
: 주차 공간을 예약할 수 있다. 사용자는 예산에 맞는 장소를 찾을 수 있으며, 충전된 포인트로 주차요금을 선지급한다. 주차시간 연장가능. <br>
: This feature allows reserving a parking spot. The user can find a place that fits the budget and pre-pay it by points.<br>

- 가격 비교 시스템 (Price Comparison)<br>
: 주차장 가격을 비교할 수 있도록 한다. 사용자들은 가까운 주차장중에서 가장 가격이 싼곳을 쉽게 찾을 수 있다.<br>
: This feature provides an opportunity to compare prices. So, it’s easy for users to find the cheapest place nearby.<br>

- 거리 비교 시스템 (Price Comparison)<br>
: 주차장 거리를 비교할 수 있도록 한다. 사용자들은 자신의 위치에서 가장 가까운 주차장을 쉽게 찾을 수 있다.<br>
: This feature provides an opportunity to compare distance between user and parking lot. So, it’s easy for users to find the nearest place.<br>

- 즐겨찾기 시스템 (Bookmark location)<br>
: 즐겨찾을 주차장을 사용자의 즐겨찾기에 추가할 수 있는 기능 <br>
: This feature allows users to save the place on their bookmark. <br>



## contributors
- Joyykim
- Jamie-Cheon
- taehyu
- bunnycast
