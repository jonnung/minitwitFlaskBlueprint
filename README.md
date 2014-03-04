# Minitwit
----

#### 소개
'Minitwit'는 위키북스 출판사의 '파이썬 웹프로그래밍 플라스크를 이용한 쉽고 빠른 웹개발' 4장에 실린 '작은 트위터, 미니트윗('minitwit')' 예제코드의 구조를 변경해서 만든 웹앱 입니다.

Flask에서 제공하는 Blueprint의 개념을 이해하기 위함이 주목적이며, MVC 형태의 구조로 분리하기 위해 재작성 하였으나 90% 이상의 코드는 책에 예제와 동일합니다.


#### 어플리케이션 구조
    application
    |\
    | app
    |  \
    |   __init__.py
    |   minitwit
    |    \
    |     __init__.py
    |     minitwit_app.py
    |
    config
    |\
    |  __init__.py
    |  settings.py
    |
    model
    |\
    |  __init__.py
    |  minitwit_model.py
    |  schema.sql
    |
    view
    |\
    |  __init__.py
    |  minitwiy
    |   \
    |    __init__.py
    |    minitwit_view.py
    |
    template
    |\
    |  404.html
    |  500.html
    |  layout.html
    |  login.html
    |  register.html
    |  timeline.html
    |  user.html
    |
    static
    |\
    | style.css
    |
    __init__.py
    run.py

#### 추가 정보
데이터베이스는 sqlite를 사용했으며, 앱의 정상 동작을 위해 '** /tmp/minitiwit.db **' 파일을 미리 생성해 둬야 한다.




