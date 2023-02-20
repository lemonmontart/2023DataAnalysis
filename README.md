# 2023DataAnalysis

### 네이버 지도 크롤링 -> 어떤 내용을 가져올 것인가?
* 지도에서 사용되는 코드 
   * 각자 고유 번호이기 때문에 인덱스로 사용함
* 가게 이름
* 어떤 업종인지
* 평점(5점 만점)
* 주소
* 좌표
* 주변 지하철 노선
* 가까운 역으로부터 떨어져있는 거리
* 네이버 지도 리뷰 시, 키워드 선택 비율
  * (키워드별 채택 횟수/전체 네이버 지도 리뷰 횟수)
* 네이버 지도에서 바로 리뷰 한 사람들의 수
* 블로그 리뷰 한 사람들의 수
  * 블로그를 작성 할 정도라면 그 가게에 대해 코어 팬일 가능성이 높다 생각.
  * 혹은 블로그 리뷰를 작성할 정도의 화제성이 있는 가게

### 문제점 및 임시 해결 방안 - 필요시 수정 예정
* 데이터 프레임의 한정적 자료형
  * 딕셔너리나 리스트 등의 형태는 입력 실패(아마도 2차원 배열이기 때문에? 원인은 아직 불명)
  * 임시 해결: 하나의 문자열로 다룸. 때문에 나중에 데이터 분석 시 다시 처리 작업이 필요함
  * 문자열로 바꿔둔 애들: 주변 지하철 노선, 선택형 리뷰
  * 좌표는 위도, 경도를 따로 작성
* 별점 None 자료형 불가능
  * 좀만 더 하면 해결 가능 할 듯 하나 0.0이 불가능 한 점수이기 때문에, 단순히 0점 주는것으로 처리함.
