from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Employee, Task

# Inline for Tasks in Employee detail view
class TaskInline(admin.TabularInline):
    model = Task
    extra = 1
    fields = ('title', 'status', 'due_date')
    max_num = 5  # Optional visual hint, but validation still needed in model

# Admin for Task
@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'assigned_employee_name', 'status', 'due_date', 'days_remaining')
    list_filter = ('status',)
    search_fields = ('title',)

    def assigned_employee_name(self, obj):
        return obj.assigned_to.name
    assigned_employee_name.short_description = 'Assigned To'

    def days_remaining(self, obj):
        return obj.days_left
    days_remaining.short_description = 'Days Left'
    days_remaining.admin_order_field = 'due_date'

# Admin for Employee
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'department', 'joining_date')
    inlines = [TaskInline]

    def get_form(self, request, obj=None, **kwargs):
        # Override form to add help text or enforce limits (optional)
        form = super().get_form(request, obj, **kwargs)
        return form