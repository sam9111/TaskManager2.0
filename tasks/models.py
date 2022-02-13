from django.db import models

from django.contrib.auth.models import User


class Task(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    completed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now=True)
    deleted = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    priority = models.IntegerField()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        priority = self.priority
        tasks = Task.objects.filter(deleted=False, user=self.user, completed=False)
        bulk_update_list = []
        while (qs := tasks.filter(priority=priority)).exists():
            task = qs[0]
            priority += 1
            task_obj = Task.objects.get(id=task.id)
            task_obj.priority = priority
            bulk_update_list.append(task_obj)
        if len(bulk_update_list) > 0:
            Task.objects.bulk_update(bulk_update_list, ["priority"])
        super(Task, self).save(*args, **kwargs)
