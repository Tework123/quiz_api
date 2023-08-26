from rest_framework import serializers

from quiz.models import Quiz, Question, Answer, ResultAnswer


# ''
class QuizListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'


# <slug:slug>/
class QuizDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'
        lookup_field = 'slug'


# <slug:slug>/questions
class QuestionListSerializerFirst(serializers.ModelSerializer):
    class Meta:
        model = ResultAnswer
        fields = ['id', 'user_id']


# <slug:slug>/questions
class QuestionListSerializerSecond(serializers.ModelSerializer):
    result_answer_list = QuestionListSerializerFirst(many=True, read_only=True)

    class Meta:
        model = Answer
        fields = ['id', 'description', 'result_answer_list']


# <slug:slug>/questions
class QuestionListSerializerThird(serializers.ModelSerializer):
    answer_list = QuestionListSerializerSecond(many=True, read_only=True)

    class Meta:
        model = Question
        fields = ['id', 'description', 'answer_list']


# statistics/
class QuizListStatisticsSerializer(serializers.Serializer):
    name = serializers.CharField()
    description = serializers.CharField()
    questions = serializers.IntegerField()


# statistics/<slug:slug>/
class QuizDetailStatisticsSerializer1(serializers.ModelSerializer):
    class Meta:
        model = ResultAnswer
        fields = ['user_id']


# statistics/<slug:slug>/
class QuizDetailStatisticsSerializer2(serializers.ModelSerializer):
    result_answer_list = QuizDetailStatisticsSerializer1(many=True, read_only=True)

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['sum_one_answer'] = len(data['result_answer_list'])

        # result_answer_list = Quiz1(many=True, read_only=True)
        return data

    class Meta:
        model = Answer
        fields = ['id', 'description', 'result_answer_list']


# statistics/<slug:slug>/
class QuizDetailStatisticsSerializer(serializers.ModelSerializer):
    answer_list = QuizDetailStatisticsSerializer2(many=True, read_only=True)

    # считывает информацию из внутренних сериализаторов и выдает проценты
    def to_representation(self, instance):  # noqa
        data = super().to_representation(instance)
        sum_question = 0
        for i in data.items():
            if i[0] == 'answer_list':
                for j in i:
                    if isinstance(j, list):
                        for k in j:
                            sum_question += k['sum_one_answer']
        data['sum_question'] = sum_question

        for i in data.items():
            if i[0] == 'sum_question':
                sum_question = i[1]
            if i[0] == 'answer_list':
                for j in i:
                    if isinstance(j, list):
                        for k in j:
                            percent = k['sum_one_answer'] / sum_question
                            k['percent'] = round(percent * 100, 2)
        return data

    class Meta:
        model = Question
        fields = ['id', 'description', 'answer_list']


# create_quiz/
class CreateQuizSerializer(serializers.ModelSerializer):
    # автоматически связывает модель с юзером, который ее создал, только без def create работает
    # creator = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # этот класс отвечает только за поля, которые показываются для ввода пользователю
    # если переопределен create, то с добавляемыми полями он не связан
    class Meta:
        model = Quiz
        fields = ['name', 'slug', 'date_stop', 'description', 'group']


# create_question/<slug:slug>/
class CreateQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'pk', 'description']


# create_answer/<int:pk>/
class CreateAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['id', 'pk', 'description']
