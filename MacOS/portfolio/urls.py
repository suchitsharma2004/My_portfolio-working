from django.urls import path
from .views import home, projects, contact, llm_chat, llm_test, gemini_chat

urlpatterns = [
    path('', home, name='home'),
    path('projects/', projects, name='projects'),
    path('contact/', contact, name='contact'),

    path('api/llm-chat/', llm_chat, name='llm_chat'),
    path('api/llm-test/', llm_test, name='llm_test'),
    path('api/gemini-chat/', gemini_chat, name='gemini_chat'),
]
