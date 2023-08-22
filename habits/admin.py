from django.contrib import admin

from habits.models import Habit, NiceHabit


@admin.register(Habit)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', )
    search_fields = ('title', )


@admin.register(NiceHabit)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title', )
    search_fields = ('title', )
