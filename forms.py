from wtforms import Form, RadioField, FieldList, FormField
from wtforms.validators import DataRequired

class FilterForm(Form):
    req = RadioField('Planarity', choices=[('both','Both'), ('planar', 'Planar'), ('nonplanar', 'Nonplanar')], 
                                  default='both',
                                  validators=[DataRequired()])

class FullForm(Form):
    filters = FieldList(RadioField('label', choices=[('both','Both'), ('directed', 'Directed'), ('undirected', 'Undirected')], 
                                            default='both'))