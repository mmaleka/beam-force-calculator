from django import forms
from .models import Beamlength, BeamSupport, PointLoad, MomentLoad, DistributedLoad


class beam_lengthForm(forms.ModelForm):
    class Meta:
        model = Beamlength
        fields = ['beam_length']

    def clean_beam_length(self):
        beam_length = self.cleaned_data.get('beam_length')

        if beam_length <= 0:
            print("beam_length: ", beam_length)
            raise forms.ValidationError("Enter a valid beam length")

        return beam_length


class beam_supportForm(forms.ModelForm):
    class Meta:
        model = BeamSupport
        widgets = {
            'beamLength': forms.HiddenInput(),
            'support': forms.RadioSelect(),
        }
        fields = ['beamLength','support', 'support_distance']


class beam_pointLoadForm(forms.ModelForm):
    class Meta:
        model = PointLoad
        widgets = {
            'beamLength': forms.HiddenInput(),
        }
        fields = ['beamLength', 'point_load', 'point_load_distance']


class beam_momentLoadForm(forms.ModelForm):
    class Meta:
        model = MomentLoad
        widgets = {
            'beamLength': forms.HiddenInput(),
        }
        fields = ['beamLength', 'moment_load', 'moment_load_distance']


class beam_distributedLoadForm(forms.ModelForm):
    class Meta:
        model = DistributedLoad
        widgets = {
            'beamLength': forms.HiddenInput(),
        }
        fields = ['beamLength', 'start_distributed_load', 'end_distributed_load', 'start_distributed_load_location', 'end_distributed_load_location']


    def clean_start_distributed_load(self):
        print("self.clea", self.cleaned_data)
        q1 = self.cleaned_data.get('start_distributed_load')
        q2 = self.cleaned_data.get('end_distributed_load')

        print(q1, q2)
        #
        if q1:
            print("testing")
            # raise forms.ValidationError("You have forgotten about Fred!")
        #     print("Validaton")
            # raise forms.ValidationError('Emails must match')

        return q1
