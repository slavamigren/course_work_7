from django.urls import path
from rest_framework import routers

from habits.apps import HabitsConfig
from habits.views import HabitViewSet, NiceHabitViewSet, PublicHabitListView, PublicNiceHabitListView

app_name = HabitsConfig.name

urlpatterns = [
    path('public/useful/', PublicHabitListView.as_view(), name='public_useful_habit_list'),
    path('public/nice/', PublicNiceHabitListView.as_view(), name='public_nice_habit_list'),
]

router_useful_habits = routers.SimpleRouter()
router_useful_habits.register(r'useful', HabitViewSet, basename='useful')

router_nice_habits = routers.SimpleRouter()
router_nice_habits.register(r'nice', NiceHabitViewSet, basename='nice')

urlpatterns += router_useful_habits.urls
urlpatterns += router_nice_habits.urls
