# 인스타 해시태그 크롤링

### 폴더 구조

└ static 폴더 (이미지, css 파일)

└ templates 폴더 (html 파일)

└ app.py 파일

## 💁‍♀️ 페이지 소개

인스타 해시태그 크롤링을 이용하여 사용자로부터 받은 단어와 연관된 단어들을 보여주는 검색 사이트 입니다.

## 🛠 기능 구현

- **로그인/회원가입**

  사용자의 관심단어 등록을 위해 로그인 기능을 추가하였습니다. 입력받은 사용자 정보를 로그인 DB에 저장합니다.

- **검색**

  사용자로부터 받은 단어를 서버로 넘겨주면 해당 단어를 인스타그램 해시태그에서 크롤링하도록 합니다.

- **검색결과**

  크롤링하여 가져온 해시태그 단어들 중 가장 많은 단어들을 가져와서 화면에 보여줍니다.