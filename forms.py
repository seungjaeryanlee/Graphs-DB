from wtforms import Form, RadioField
from wtforms.validators import DataRequired

class FilterForm(Form):
    planarity = RadioField('Planarity', choices=[('both','Both'), ('planar', 'Planar'), ('nonplanar', 'Nonplanar')], 
                                        default='both',
                                        validators=[DataRequired()])
    directedness = RadioField('Directedness', choices=[('both','Both'), ('directed', 'Directed'), ('undirected', 'Undirected')], 
                                        default='both',
                                        validators=[DataRequired()])
