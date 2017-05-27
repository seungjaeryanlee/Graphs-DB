from wtforms import Form, RadioField, FieldList, FormField
from wtforms.validators import DataRequired

class FullForm(Form):
    filters = FieldList(RadioField())
