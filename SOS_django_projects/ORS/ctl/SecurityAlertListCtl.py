from django.shortcuts import render
from .BaseCtl import BaseCtl
from service.service.SecurityAlertService import SecurityAlertService


class SecurityAlertListCtl(BaseCtl):
    count = 1


    def request_to_form(self, request_form):
        self.form["threat_level"] = request_form.get("threat_level",None)
        self.form["source_ip"] = request_form.get("source_ip",None)
        self.form["detected_time"] = request_form.get("detected_time",None)
        self.form["status"] = request_form.get("status",None)

    def display(self, request, params={}):

        SecurityAlertListCtl.count = self.form['page_no']
        self.page_list = self.get_service().search(self.form)
        print("pagelisttttttttttttt",self.page_list)
        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def submit(self, request, params={}):

        self.form['page_no'] = SecurityAlertListCtl.count

        if request.POST['operation'] == "Next":
            SecurityAlertListCtl.count += 1
            self.form['page_no'] = SecurityAlertListCtl.count

        if request.POST['operation'] == "Previous":
            SecurityAlertListCtl.count -= 1
            self.form['page_no'] = SecurityAlertListCtl.count

        if request.POST['operation'] == "Search":
            SecurityAlertListCtl.count = 1
            self.form['page_no'] = SecurityAlertListCtl.count

        if request.POST['operation'] == "Reset":
            SecurityAlertListCtl.count = 1

            self.form["threat_level"] = None
            self.form["source_ip"] = None
            self.form["detected_time"] = None
            self.form["status"] = None

            self.form['page_no'] = 1

        self.page_list = self.get_service().search(self.form)

        res = render(request, self.get_template(), {
            "form": self.form,
            "page_list": self.page_list,
        })
        return res

    def get_template(self):
        return "ors/SecurityAlertList.html"

    def get_service(self):
        return SecurityAlertService()
