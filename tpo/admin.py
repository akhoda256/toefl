from django.contrib import admin

from .models import TPO
from .models import Passage
from .models import Paragraph
from .models import QuestionType
from .models import Question
from .models import Option
from .models import Answer
# Register your models here.
admin.site.register(TPO)
admin.site.register(Passage)
admin.site.register(Paragraph)
admin.site.register(QuestionType)
admin.site.register(Question)
admin.site.register(Option)
admin.site.register(Answer)

# Register your models here.
