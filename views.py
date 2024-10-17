from django.shortcuts import render
import sklearn
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier
import pandas as pd

def ml(request):
    if request.method == "POST":
        data = request.POST
        satisfaction_level = float(data.get('satisfaction_level', 0.0))
        last_evaluation = float(data.get('last_evaluation', 0.0))
        number_project = int(data.get("number_project", 0))
        average_monthly_hours = int(data.get("average_monthly_hours", 0.0))
        time_spend_company = float(data.get("time_spend_company", 0.0))
        Work_accident = float(data.get("work_accident", 0.0))
        promotion_last_5years = float(data.get("promotion_last_5years", 0.0))
        Department = data.get("Department_n", "")  
        salary= data.get("salary_n", "")  

        if 'submitbutton' in request.POST:
            path = "C:\\Users\\jayas\\OneDrive\\Desktop\\project\\GUI\\basics\\employeeretention.csv"
            data = pd.read_csv(path)
            
            le_Department = LabelEncoder()
            data['Department_n'] = le_Department.fit_transform(data['Department'])
            le_salary = LabelEncoder()
            data['salary_n'] = le_salary.fit_transform(data['salary'])

            inputs = data.drop(['left', 'Department', 'salary'], axis=1)
            output = data['left']

            model = DecisionTreeClassifier()
            model.fit(inputs, output)

            # Assuming Department and salary need to be transformed using the LabelEncoders
            Department_n = le_Department.fit_transform([Department])
            salary_n = le_salary.fit_transform([salary])

            res = model.predict([[satisfaction_level, last_evaluation, number_project, average_monthly_hours,
                                  time_spend_company, Work_accident, promotion_last_5years, Department_n[0], salary_n[0]]])
            if res == 1:
                res="Employee has not left"
            else:
                res="Employee has left"
                
            return render(request, 'ml.html', context={'result': res})

    return render(request, 'ml.html')

