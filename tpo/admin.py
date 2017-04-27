from django.contrib import admin

from .models import TPO, ReadingQuestion, ListeningQuestion
from .models import Passage
from .models import Paragraph
from .models import QuestionType
from .models import Question
from .models import Option
from .models import Answer
from .models import Conversation
from .models import SpeakingResponse
# Register your models here.
admin.site.register(TPO)
admin.site.register(Passage)
admin.site.register(Paragraph)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Answer)
admin.site.register(Conversation)
admin.site.register(SpeakingResponse)
admin.site.register(ReadingQuestion)
admin.site.register(ListeningQuestion)
# Register your models here.
