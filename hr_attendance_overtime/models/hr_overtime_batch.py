import toolz as T
import toolz.curried as TC
from datetime import datetime, time
import pytz
from odoo import _, api, fields, models
from odoo.addons.resource.models.resource import Intervals


class HrOvertimeBatch(models.Model):
  _name = 'hr.overtime.batch'
  _description = 'Hr  Overtime Batch'
  _rec_name = 'overtime_batch_sequence'

  date_from = fields.Date('Date From')
  date_to = fields.Date('Date To')
  name = fields.Char('Batch Name')
  overtime_ids = fields.One2many(
      'hr.overtime',
      'overtime_batch_id',
      string='overtime',
  )
  misstime_ids = fields.One2many(
      'hr.misstime',
      'overtime_batch_id',
      string='misstime',
  )
  overtime_batch_sequence = fields.Char(
      string='Batch Number',
      required=False,
      copy=False,
      readonly=True,
      default='new',
  )

  # ==========================================================================
  def _actual_attendances_intervals_batch(self, employee_ids):

    batch_start_date = datetime.combine(self.date_from, time.min)
    batch_end_date = datetime.combine(self.date_to, time.max)

    attendances = self.env['hr.attendance'].search([
        ('check_in', '>=', batch_start_date),
        ('check_in', '<=', batch_end_date),
        ('check_out', '<=', batch_end_date),
        ('check_out', '>=', batch_start_date),
        ('employee_id', 'in', employee_ids),
    ])
    return T.pipe(
        attendances,
        TC.groupby(lambda att: att.employee_id.id),
        TC.valmap(
            TC.map(lambda attendance_record: (
                pytz.utc.localize(attendance_record.check_in),
                pytz.utc.localize(attendance_record.check_out),
                attendance_record,
            )),),
        TC.valmap(Intervals),
    )

  # ==========================================================================
  def claculate_employees_overtimes(self, employees_data):
    self.overtime_ids.unlink()

    def _get_employee_overtime_by_day(overtime_intervals):
      return T.pipe(
          overtime_intervals,
          TC.map(
              lambda overtime_interval: {
                  "date":
                      overtime_interval[1].date(),
                  "overtime_minutes":
                      (overtime_interval[1] - overtime_interval[0]).total_seconds() / 60,
                  "notes":
                      f"from {overtime_interval[0]} to {overtime_interval[1]}"
              }),
          TC.groupby('date'),
          TC.valmap(
              lambda overtimes: {
                  "duration": sum([overtime.get("overtime_minutes") for overtime in overtimes]),
                  "notes": '\n'.join([overtime.get("notes") for overtime in overtimes])
              }),
      )

    employees_grouped_by_caledar = T.pipe(
        employees_data,
        TC.groupby("resource_calendar_id"),
    )

    for calendar, employees in employees_grouped_by_caledar.items():
      overtime_intervals_batch = self.get_overtime_intervals(
          calendar,
          employees,
      )
      for emp_id, overtime_intervals in overtime_intervals_batch.items():
        overtimes = _get_employee_overtime_by_day(overtime_intervals,)
        for date, overtime in overtimes.items():
          self.env['hr.overtime'].create({
              "employee_id": emp_id,
              "date": date,
              "duration": overtime.get('duration'),
              "notes": overtime.get('notes'),
              "overtime_batch_id": self.id,
          })

  def get_overtime_intervals(self, calendar, employees):
    """"
        get difference between employees_actual_attendance_hours and employees_official_working_hours
        he work from 10:00 to 12 but he should be exist from 10:00 to 11:00 , so he has 1 hour overtime

        """
    date_from = datetime.combine(self.date_from, time.min)
    date_to = datetime.combine(self.date_to, time.max)
    user_tz = pytz.timezone(self.env.user.tz)

    employees_official_working_hours = calendar._work_intervals_batch(
        user_tz.localize(date_from),
        user_tz.localize(date_to),
        resources=[emp.resource_id for emp in employees],
    )

    employees_actual_attendance_hours = self._actual_attendances_intervals_batch(
        [emp.id for emp in employees])

    return {
        emp.id: employees_actual_attendance_hours.get(emp.id, Intervals([])) -
        employees_official_working_hours.get(emp.id, Intervals([])) for emp in employees
    }

  # ==========================================================================
  # ==========================================================================

  def get_misstime_intervals(self, calendar, employees):
    """"
        get difference between employees_actual_attendance_hours and employees_official_working_hours
        he work from 10:00 to 12 but he should be exist from 10:00 to 11:00 , so he has 1 hour overtime

        """
    date_from = datetime.combine(self.date_from, time.min)
    date_to = datetime.combine(self.date_to, time.max)
    user_tz = pytz.timezone(self.env.user.tz)

    employees_official_working_hours = calendar._work_intervals_batch(
        user_tz.localize(date_from),
        user_tz.localize(date_to),
        resources=[emp.resource_id for emp in employees],
    )

    employees_actual_attendance_hours = self._actual_attendances_intervals_batch(
        [emp.id for emp in employees])

    return {
        emp.id: employees_official_working_hours.get(emp.id, Intervals([])) -
        employees_actual_attendance_hours.get(emp.id, Intervals([])) for emp in employees
    }

  def claculate_employees_misstimes(self, employees_data):
    self.misstime_ids.unlink()

    def _get_employee_misstime_by_day(misstime_intervals):
      return T.pipe(
          misstime_intervals,
          TC.map(
              lambda misstime_interval: {
                  "date":
                      misstime_interval[1].date(),
                  "misstime_minutes":
                      (misstime_interval[1] - misstime_interval[0]).total_seconds() / 60,
                  "notes":
                      f"from {misstime_interval[0]} to {misstime_interval[1]}"
              }),
          TC.groupby('date'),
          TC.valmap(
              lambda misstimes: {
                  "duration": sum([misstime.get("misstime_minutes") for misstime in misstimes]),
                  "notes": '\n'.join([misstime.get("notes") for misstime in misstimes])
              }),
      )

    employees_grouped_by_caledar = T.pipe(
        employees_data,
        TC.groupby("resource_calendar_id"),
    )

    for calendar, employees in employees_grouped_by_caledar.items():
      misstime_intervals_batch = self.get_misstime_intervals(
          calendar,
          employees,
      )
      for emp_id, overtime_intervals in misstime_intervals_batch.items():
        misstimes = _get_employee_misstime_by_day(overtime_intervals,)
        for date, misstime in misstimes.items():
          self.env['hr.misstime'].create({
              "employee_id": emp_id,
              "date": date,
              "duration": misstime.get('duration'),
              "notes": misstime.get('notes'),
              "overtime_batch_id": self.id,
          })

  # ==========================================================================
  # ==========================================================================
  def overtime_batch(self):
    employees = self.env['hr.employee'].search([])

    self.claculate_employees_overtimes(employees_data=employees)
    self.claculate_employees_misstimes(employees_data=employees)

  @api.model
  def create(self, value_list):
    value_list['overtime_batch_sequence'] = self.env['ir.sequence'].next_by_code(
        'code.overtime_batch.seq')
    obj = super().create(value_list)
    return obj
