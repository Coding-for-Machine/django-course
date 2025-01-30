from django.contrib import admin
from .models import Category, Quiz, Topic, Question, Answer, UserScore, UserAnswer
from django.contrib.contenttypes.models import ContentType
from .models import Varyant, Savol
from django import forms
from django.contrib.contenttypes.models import ContentType

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = '__all__'

    # content_type maydonini tanlash uchun ModelChoiceField
    content_type = forms.ModelChoiceField(
        queryset=ContentType.objects.filter(model__in=['quiz', 'topic']),
        required=True
    )

    # object_id ni tanlash uchun dynamic queryset
    object_id = forms.ChoiceField(
        required=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # content_type ni tanlashdan keyin, object_id ni dinamik ravishda sozlash
        if 'content_type' in self.data:
            content_type_id = self.data.get('content_type')
            if content_type_id:
                content_type = ContentType.objects.get(id=content_type_id)
                if content_type.model == 'quiz':
                    self.fields['object_id'].choices = [(quiz.id, quiz.title) for quiz in Quiz.objects.all()]
                elif content_type.model == 'topic':
                    self.fields['object_id'].choices = [(topic.id, topic.title) for topic in Topic.objects.all()]
        else:
            self.fields['object_id'].choices = []

# Register your models here.
class VaryantItem(admin.TabularInline):
    model = Varyant
    raw_id_fields = ['savol']

@admin.register(Savol)
class OSavolAdmin(admin.ModelAdmin):
    
    list_display = ['id', "description", "quizes_types", "updated","created"]
    list_filter = ['id', 'created', 'updated']
    inlines = [VaryantItem]



# ==========================
# 1. Category admin
# ==========================
from django.contrib import admin
from .models import Category

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_created_at', 'get_updated_at')

    def get_created_at(self, obj):
        return obj.created_at
    get_created_at.admin_order_field = 'created_at'  # Bu maydonni tartiblash imkoniyatini beradi
    get_created_at.short_description = 'Created At'

    def get_updated_at(self, obj):
        return obj.updated_at
    get_updated_at.admin_order_field = 'updated_at'
    get_updated_at.short_description = 'Updated At'

admin.site.register(Category, CategoryAdmin)



# ==========================
# 2. Quiz admin
# ==========================
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'time_limit', 'is_active', 'created_at', 'updated_at')
    list_filter = ('category', 'is_active')
    prepopulated_fields = {'slug': ('title',)}  # Slugni avtomatik to'ldirish
    search_fields = ('title', 'description')

admin.site.register(Quiz, QuizAdmin)


# ==========================
# 3. Topic admin
# ==========================
class TopicAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'category', 'is_active', 'created_at', 'updated_at')
    list_filter = ('category', 'is_active')
    prepopulated_fields = {'slug': ('title',)}  # Slugni avtomatik to'ldirish
    search_fields = ('title', 'description')

admin.site.register(Topic, TopicAdmin)


# ==========================
# 4. Question admin
# ==========================
class QuestionAdmin(admin.ModelAdmin):
    form = QuestionForm
    list_display = ('text', 'content_type', 'object_id', 'created_at')

admin.site.register(Question, QuestionAdmin)


# ==========================
# 5. Answer admin
# ==========================
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('question', 'text', 'is_correct')
    list_filter = ('is_correct',)
    search_fields = ('text',)

admin.site.register(Answer, AnswerAdmin)


# ==========================
# 6. UserScore admin
# ==========================
class UserScoreAdmin(admin.ModelAdmin):
    list_display = ('user', 'quiz', 'score', 'completed_at')
    list_filter = ('quiz', 'user')
    search_fields = ('user__username', 'quiz__title')

admin.site.register(UserScore, UserScoreAdmin)


# ==========================
# 7. UserAnswer admin
# ==========================
class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'answer', 'answered_at')
    list_filter = ('user', 'question')
    search_fields = ('user__username', 'question__text')

admin.site.register(UserAnswer, UserAnswerAdmin)
