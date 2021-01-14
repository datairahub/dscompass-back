def update_form_length(instance, **kwargs):
    if instance.is_active is True:
        length = instance.form.question_related.count()
        form = instance.form
        form.questions_length = length
        form.save()
