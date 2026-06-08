from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.utility.DataValidator import DataValidator
from ..utility.HtmlUtility import HtmlUtility
from service.service.CollegeSystemService import CollegeSystemService
from service.models import CollegeSystem


class CollegeSystemCtl(BaseCtl):

    def preload(self, request):
        semester_list = [1,2,3,4,5,6]
        self.preload_data["semester_select"] = HtmlUtility.get_list_from_list("semester",self.form.get("semester"),semester_list)
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["student_name"] = request_form.get("student_name", "").strip()
        self.form["branch"] = request_form.get("branch", "").strip()
        self.form["semester"] = request_form.get("semester", "").strip()
        self.form["cgpa"] = request_form.get("cgpa", "").strip()

    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.student_name = self.form.get("student_name", "")
        obj.branch = self.form.get("branch", "")
        obj.semester = self.form.get("semester", "")
        obj.cgpa = self.form.get("cgpa", "")
        return obj

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["student_name"] = obj.student_name
        self.form["branch"] = obj.branch
        self.form["semester"] = obj.semester
        self.form["cgpa"] = obj.cgpa

    def input_validation(self):
        super().input_validation()
        input_error = self.form.get("input_error", {})

        if DataValidator.isNull(self.form.get("student_name")):
            input_error["student_name"] = "Student Name can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("branch")):
            input_error["branch"] = "Branch can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("semester")) or self.form.get("semester") == "0":
            input_error["semester"] = "Semester can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("cgpa")):
            input_error["cgpa"] = "cgpa can not be null"
            self.form["error"] = True

        return self.form.get("error", False)

    def display(self, request, params={}):
        college_id = int(params.get("id", 0))

        if college_id > 0:
            college = self.get_service().get(college_id)
            self.model_to_form(college)

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        pk = int(self.form.get('id', 0))

        duplicate = self.get_service().get_model().objects.filter(student_name=self.form.get('student_name', ''))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form['error'] = True
            self.form['message'] = "College already exist"
        else:
            college = self.form_to_model(CollegeSystem())
            self.get_service().save(college)
            self.form['id'] = college.id
            self.form['error'] = False

            if pk > 0:
                self.form['message'] = "College updated successfully"
            else:
                self.form['message'] = "College added successfully..!!"

        res = render(request, self.get_template(), {
            "form": self.form,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "ors/CollegeSystem.html"

    def get_service(self):
        return CollegeSystemService()
