from odoo import models, fields
from datetime import timedelta

class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    def _auto_close_attendance(self):
        """Clôture automatique des présences ouvertes"""

        max_hours = float(
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("attendance.max_hours", 8)
        )

        now = fields.Datetime.now()

        attendances = self.search([
            ("check_out", "=", False),
            ("check_in", "!=", False),
        ])

        for attendance in attendances:
            duration = now - attendance.check_in
            if duration >= timedelta(hours=max_hours):
                attendance.write({
                    "check_out": attendance.check_in + timedelta(hours=max_hours)
                })
