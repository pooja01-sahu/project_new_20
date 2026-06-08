from django.shortcuts import render, redirect
from service.utility.DataValidator import DataValidator
from django.http import HttpResponse
from .BaseCtl import BaseCtl
from service.models import College
from service.service.CollegeService import CollegeService

from service.service.CollegeSystemService import CollegeSystemService

from ..utility.HtmlUtility import HtmlUtility


class CollegeSystemListCtl(BaseCtl):
    count = 1

    def preload(self, request):
        semester_list = [1, 2, 3, 4, 5, 6]
        self.preload_data["semester_select"] = HtmlUtility.get_list_from_list("semester", self.form.get("semester"),
                                                                              semester_list)
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["student_name"] = request_form.get("student_name", "").strip()
        self.form["branch"] = request_form.get("branch", "").strip()
        self.form["semester"] = request_form.get("semester", "").strip()
        self.form["cgpa"] = request_form.get("cgpa", "").strip()

    def display(self, request, params={}):
        CollegeSystemListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = CollegeSystemListCtl.count

        if request.POST['operation'] == "Next":
            CollegeSystemListCtl.count += 1
            self.form['page_no'] = CollegeSystemListCtl.count
        if request.POST['operation'] == "Previous":
            CollegeSystemListCtl.count -= 1
            self.form['page_no'] = CollegeSystemListCtl.count
        if request.POST['operation'] == "Search":
            CollegeSystemListCtl.count = 1
            self.form['page_no'] = CollegeSystemListCtl.count

        self.page_list = self.get_service().search(self.form)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
            "preload_data": self.preload(request)
        })
        return res

    def get_template(self):
        return "ors/CollegeSystemList.html"

    def get_service(self):
        return CollegeSystemService()
