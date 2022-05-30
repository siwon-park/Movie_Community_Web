from dataclasses import field
from rest_framework import serializers
from community.models import Question, Vote

from django.contrib.auth import get_user_model

User = get_user_model()

# 주제등록
class QuestionRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Question
        fields = '__all__'

# 주제와 전체 응답 수 조회
class QuestionSerializer(serializers.ModelSerializer):

    question_answer_count = serializers.IntegerField() # 응답 인원 수

    class Meta:
        model = Question
        fields = '__all__'

# 주제와 특정 응답 수 조회
class QuestionVoteSerializer(serializers.ModelSerializer):

    class VoteSerializer(serializers.ModelSerializer):
        class Meta:
            model = Vote
            fields = '__all__'

    new_question_answer_count = serializers.IntegerField() # 응답 인원 수
    
    class Meta:
        model = Question
        fields = '__all__'


# 투표 등록 및 해제
class VotePickSerializer(serializers.ModelSerializer):

    class QuestionSerializer(serializers.ModelSerializer):
        class Meta:
            model = Question
            fields = '__all__'

    class UserSerializer(serializers.ModelSerializer):
        class Meta:
            model = User
            fields = ('pk', 'username',)

    vote_user = UserSerializer(read_only=True)
    vote_question = QuestionSerializer(read_only=True)

    class Meta:
        model = Vote
        # 투표 번호, 투표한 사용자 정보, 투표한 주제, 응답 내용, 작성 의견
        fields = ('id', 'vote_user', 'vote_question', 'vote_answer', 'vote_content')