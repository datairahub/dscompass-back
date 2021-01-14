from rest_framework.routers import DefaultRouter

from .views import answer_view, form_answer_view, form_view, language_view


class DefendersAPIRouter:
    def __init__(self):
        self.router = DefaultRouter()

    def register_router(self) -> DefaultRouter:
        self.router.register(r'answers', answer_view.AnswerViewSet)
        self.router.register(r'form_answers', form_answer_view.FormAnswerViewSet)
        self.router.register(r'forms', form_view.FormViewSet)
        self.router.register(r'languages', language_view.LanguageViewSet)

        return self.router
