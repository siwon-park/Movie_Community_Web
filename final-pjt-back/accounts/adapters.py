# dj_rest_auth로 회원가입을 하고자 할 때,
# 회원정보를 데이터베이스에 저장하는 역할을 하는 부분은 
# all-auth의 DefaultAccountAdapter 클래스임
# 해당 클래스의 save_user 메서드에서 회원 정보 데이터를 저장해야함

from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):

    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        # 기본 저장 필드: first_name, last_name, username, email
        # super()를 사용하여 부모의 데이터(기본 데이터)를 저장
        user = super().save_user(request, user, form, False)

        # 저장하고자 하는 추가 필드를 아래와 같이 여러 개 정의한 다음 user의 속성 값에 할당
        # user의 속성 값은 우리가 지정한 데이터 필드 이름
        # 추가 저장 필드: sex (예시)
        sex = data.get("sex")
        region = data.get("region")
        birth_date = data.get("birth_date")
        
        if sex:
            user.sex = sex
        if region:
            user.region = region
        if birth_date:
            user.birth_date = birth_date

        user.save() # 저장
        return user