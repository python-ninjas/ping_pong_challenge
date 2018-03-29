import pygal

from .models import *

# class ScoresChart():
#     def __init__(self, **kwargs):
#         self.chart = pygal.Bar(**kwargs)
#         self.chart.title = "User Score"
#     def get_data(self):
#         data = {}
#         for user in User.objects.all():
#             data[user.username] = user.totalscore
#         return data
#     def generate(self):
#         chart_data = self.get_data()

#         for key, value in chart_data.items():
#             self.chart.add(key, value)
#         return self.chart.render_to_file('apps/login_and_register/static/login_and_register/img/barchart.svg')
####Ignore the above was for testing
##! must install pygal when deploying.
###### Bar chart for user test below works: plug code into routes where templates are rendered. Everytime route used. Graph will upate with current database info.
    user1 = User.objects.get(id=1)
    barchart = pygal.Bar()
    barchart.title = "User stats"
    for user in User.objects.all():
        barchart.add(user.username, user.totalscore)
    barchart.render_to_file('apps/login_and_register/static/login_and_register/img/barchart.svg')
    # #######