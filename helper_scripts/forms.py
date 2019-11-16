from flask_wtf import FlaskForm
from wtforms import SubmitField,StringField, IntegerField
from flask_wtf.file import FileField,FileAllowed
from wtforms.validators import DataRequired, Length 

class Submit(FlaskForm):
    submit = SubmitField('Record')

class TestMic(FlaskForm):
    submit = SubmitField('testMic')

class StopRecording(FlaskForm):
    submit = SubmitField('Stop')

class CheckConfiguredDevice(FlaskForm):
    submit = SubmitField('CheckConfiguredDevice')

class SelectMicrophoneDevice(FlaskForm):
    deviceId = IntegerField('Device Id',validators=[DataRequired(message="Only accepts Number"), Length(min=0, max=2)])
    submit = SubmitField('Save')  