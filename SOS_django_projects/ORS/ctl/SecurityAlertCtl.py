from datetime import datetime

from django.shortcuts import render
from service.models import SecurityAlert
from .BaseCtl import BaseCtl
from ..utility.DataValidator import DataValidator
from service.service.SecurityAlertService import SecurityAlertService

from ..utility.HtmlUtility import HtmlUtility


class SecurityAlertCtl(BaseCtl):

    def preload(self, request):
        status_list = ["Active", "Inactive"]

        self.preload_data["status_list"] = HtmlUtility.get_list_from_list(
            "status",
            self.form.get("status"),
            status_list
        )
        return self.preload_data

    def request_to_form(self, request_form):
        self.form["id"] = request_form.get("id", 0)
        self.form["threat_level"] = request_form.get("threat_level")
        self.form["source_ip"] = request_form.get("source_ip")
        self.form["detected_time"] = request_form.get("detected_time")
        self.form["status"] = request_form.get("status")

    def form_to_model(self, obj):
        obj.id = int(self.form.get("id", 0) or 0)
        obj.threat_level = self.form.get("threat_level")
        obj.source_ip = self.form.get("source_ip")
        obj.detected_time = (datetime.strptime(self.form.get("detected_time"), "%Y-%m-%d").date() if self.form.get(
            "detected_time") else None)
        obj.status = self.form.get("status")
        return obj

    def model_to_form(self, obj):
        if obj is None:
            return
        self.form["id"] = obj.id
        self.form["threat_level"] = obj.threat_level
        self.form["source_ip"] = obj.source_ip
        self.form["detected_time"] = obj.detected_time.strftime("%Y-%m-%d") if obj.detected_time else ""
        self.form["status"] = obj.status

    def input_validation(self):
        super().input_validation()
        input_error = self.form.get("input_error", {})

        if DataValidator.isNull(self.form.get("threat_level")):
            input_error["threat_level"] = "Threat Level can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("detected_time")):
            input_error["detected_time"] = "Detected Time can not be null"
            self.form["error"] = True

        if DataValidator.isNull(self.form.get("status")):
            input_error["status"] = "Status can not be null"
            self.form["error"] = True

    def display(self, request, params={}):
        security_id = int(params.get("id", 0))
        print("security id", security_id)
        if security_id > 0:
            security = self.get_service().get(security_id)
            print("Security Object =", security)
            self.model_to_form(security)

        res = render(request, self.get_template(), {"form": self.form, "preload_data": self.preload(request)})
        return res

    def submit(self, request, params={}):
        pk = int(self.form.get('id', 0))

        duplicate = self.get_service().get_model().objects.filter(threat_level=self.form.get("threat_level", ""))

        if pk > 0:
            duplicate = duplicate.exclude(id=pk)

        if duplicate.exists():
            self.form["error"] = True
            self.form["message"] = "Secrity Alert already exist"
        else:
            security = self.form_to_model(SecurityAlert())
            self.get_service().save(security)
            self.form["id"] = security.id
            self.form["error"] = False

            if pk > 0:
                self.form["message"] = "Security Updated Successfully"
            else:
                self.form["message"] = "Security Added Successfully"

        res = render(request, self.get_template(), {"form": self.form, "preload_data": self.preload(request)})

        return res

    def get_template(self):
        return "ors/SecurityAlert.html"

    def get_service(self):
        return SecurityAlertService()
