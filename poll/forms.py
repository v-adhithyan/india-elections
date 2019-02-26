from django import forms

from .models import OpinionPoll, Constituency


class OpinionPollForm(forms.ModelForm):

    class Meta:
        model = OpinionPoll
        fields = ('email', 'age', 'gender', 'state', 'place', 'choices')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['place'].queryset = Constituency.objects.none()

        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.fields['place'].queryset = Constituency.objects.filter(state_union_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['place'].queryset = self.instance.state.constituency_set.order_by('name')
