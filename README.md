---
#### 항해99 8기 A반 11조 - 미니프로젝트1  
# 오겜무(오늘 게임 뭐하지?)  
---
![main_page](https://user-images.githubusercontent.com/15075501/178900303-f1bff205-cea4-4c9d-9be4-7f099c54cf6b.png)  

[시연영상 바로가기](https://youtu.be/_wJ3j0TnJjs)
---
## 1. 프로젝트 소개

게임 리뷰를 작성하고 모아볼 수 있는 웹 사이트를 만들었습니다.
구글링을 통해 swipe 기능을 찾아 구현해봤습니다.
본인이 직접 플레이한 게임을 url를 찾아 크롤링하여 리뷰하고, 다른사람이 리뷰한 게임을 볼 수 있어 다양한 게임을 고르실 수 있습니다.
중복 없이 num을 부여하여 리뷰삭제중복을 방지하였습니다.
동영상 배경화면을 추가하여 역동감을 부여했습니다.
게임리뷰 URL을 입력시 해당 게임 내용이 디스플레이 되도록 구현하였습니다.

## 2. 팀 소개
- 김  훈(spring) : 리뷰작성페이지 구현
- 김휘림(spring) : 로그인 페이지, 회원가입, 마이페이지 구현
- 권용준(react) : 리뷰페이지 스와이프 기능구현 및 CSS 디자인
- 손원철(spring) :웹페이지 크롤링, 로그인페이지 CSS

## 3. 작업 기간
- 2022년 7월 11일 ~ 2022년 7월 14일 (총 4일)

## 4. 사용 기술
`Back-end`  
- Python
- Flask
- MongoDB
- BS4
- JWT

`Front-end`
- JQuery
- Bootstrap
- Jinja2
- swipe
- bulma

## 5. 구현 기능
+ 메인 페이지  
  - 등록 리뷰 스와이프
  - 새 탭으로 오픈크래틱url로 이동
  - 게임 리뷰하기 페이지 이동
  - 게임 상세정보 페이지 이동
  - 마이페이지 이동
  - 로그아웃 기능 구현
  
+ 마이 페이지 
   - 내가 작성한 리뷰 확인
   - 내가 작성한 리뷰 삭제
   - 회원정보 수정
   - 로그아웃 기능 구현
   - 아이콘 클릭하여 메인페이지로 이동

+ 리뷰 페이지  
  - 게임리뷰 작성
  - 게임url 크롤링 기능 구현
  - 평가 점수 구현
  
+ 로그인 페이지  
  - 로그인 기능 구현
  - 회원가입 페이지 이동
  - 백그라운드 영상css
  

+ 회원가입 페이지  
  - 아이디 중복 확인  
  - 아이디, 비밀번호 양식 확인  
  - 비밀번호 일치 확인
  - 닉네임, 생일 입력값 확인
  - 회원정보 등록
  
## 6. page list

login page

![login_page](https://user-images.githubusercontent.com/15075501/178900126-27357ec9-b5c1-448c-81c3-2cf418670d0a.png) 


signup page

![signup page](https://user-images.githubusercontent.com/15075501/178900268-3079f37c-0dd1-45ea-94bb-3361a0239ee9.png)



main page

![main_page](https://user-images.githubusercontent.com/15075501/178900303-f1bff205-cea4-4c9d-9be4-7f099c54cf6b.png) 


reviewpage

![review page](https://user-images.githubusercontent.com/15075501/178900348-41a8b521-e556-484b-ab99-7cf1b0c0707b.png)


my page

![my page](https://user-images.githubusercontent.com/15075501/178900400-5a34a969-b4a7-43d3-84dd-6bd3f196fee2.png)
![my page2](https://user-images.githubusercontent.com/15075501/178900438-487ac03f-af14-456f-bfa6-640a915dfa6b.png)


## 7. Troubleshooting  
1. swiper-container에 temp_html.append로 card-box를 넣을때 append 오류
->swiper를 const로 주고 ajax 기능중에 swiper.removeAllSlides(); swiper.appendSlide(res); swiper.update();
를 참고하여 먼저 remove후에 container에 append해주고, update하면 카드박스가 잘 나옴

```javascript
const swiper = new Swiper ~~~~ 생략
 
$.ajax({
        생략
        success: function(res) {
                swiper.removeAllSlides();
                swiper.appendSlide(res);
                swiper.update();
        }
});
```
2. num 부여시 중복num 문제 > num db 따로 저장하여 해결 

3. 배경 CSS 적용 문제 > absolute 적용 및 작업 후 해결
  ```css
position: absolute;
          left: 50%;
          transform: translateX(-50%);
```

 4. swiper button 모양을 원하는 모양으로 바꾸기
 
->swiper-button-next,prev에         image URL을 따와서 넣어주고 !important;가 나중에 설정한값이 오도록 해준다는것을 알았다.
```css
.swiper-button-prev {
  background-image: url("") !important;
}

.swiper-button-next {
  background-image: url("") !important;

}
```
5. 마이페이지 로그아웃 button 위치변경
->button position 이라는 구글링을 통해 positon 속성에 static, absolute, relative, fixed 각각 다르다는걸 알았고

먼저,absolute 로 부모요소 혹은 가장 가까운 상위요소로 움직이고

relative 로 자신의 상대적 위치를 기준으로 움직여서 설정을 했다.

```css
 .logout {
            position: absolute;
            top: 70px;
            left: 850px;
        }



  .logout > button {
            position: relative;
            top:-40px;
        }
```

6. jinja로 넘겨준 사용자 정보 데이터를 html에서 인식하지 못하는 문제
-> mongoDB에서 사용자 정보를 조회하는 코드를 수정하여 해결함

```python
# 전
user_info = db.user.find_one({"user_id": payload['user_id']}), {'id': False, 'user_name': False}
# 후
user_info = db.user.find_one({"user_id": payload['user_id']}, {'_id': False, 'user_pw': False})
```

7. 다른 사용자의 마이페이지 접근시 하단 여백이 너무 좁은 문제
-> {% else %} 를 활용하여 해결함

```html
{% if status %}
        …
{% else %}
        <div class="mb-5"></div>
{% endif %}
```

8. 배경 색상이 화면 전체에 표시되지 않는 문제
-> body 태그에 min-height를 100vh로 설정하여 해결함

```css
body {
        …
        min-height: 100vh
}
```

9. 로그아웃 기능이 제대로 작동하지 않는 문제
-> 헤더에 제이쿼리 쿠키를 추가하여 해결
```html
<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery-cookie/1.4.1/jquery.cookie.js"></script>
```
