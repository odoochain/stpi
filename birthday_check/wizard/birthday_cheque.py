from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, date, timedelta
import requests
import json
import datetime
from dateutil.relativedelta import relativedelta

class BirthdayChequeRequest(models.TransientModel):
    _name = 'birthday.cheque.wizard'
    _description = 'Wizard of Employee Selection'


    def button_current_month(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if emp.birthday.strftime("%m") == datetime.datetime.now().strftime("%m"):
                    my_ids.append(emp.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Current Month Birthday',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'hr.employee',
                'view_id': False,
                'views': [(self.env.ref('hr.hr_kanban_view_employees').id, 'kanban'),
                          (self.env.ref('birthday_check.hr_employee_birthday_tree2').id, 'tree'),
                          (self.env.ref('hr_employee_stpi.view_add_Employee_doc_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }


    def button_previous_month(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if (datetime.datetime.now().replace(day=1) - relativedelta(months=1)).strftime("%m") == datetime.datetime.now().strftime("%m"):
                    my_ids.append(emp.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Previous Month Birthday',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'hr.employee',
                'view_id': False,
                'views': [(self.env.ref('hr.hr_kanban_view_employees').id, 'kanban'),
                          (self.env.ref('birthday_check.hr_employee_birthday_tree2').id, 'tree'),
                          (self.env.ref('hr_employee_stpi.view_add_Employee_doc_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }



    def button_next_month(self):
        if self:
            my_ids = []
            employee = self.env['hr.employee'].sudo().search([])
            for emp in employee:
                if (datetime.datetime.now().replace(day=1)+ relativedelta(months=1)).strftime("%m") == datetime.datetime.now().strftime("%m"):
                    my_ids.append(emp.id)
            print('==================my_ids========================', my_ids)
            return {
                'domain': [('id', 'in', my_ids)],
                'name': 'Employees - Next Month Birthday',
                'view_type': 'form',
                'view_mode': 'kanban,tree,form',
                'res_model': 'hr.employee',
                'view_id': False,
                'views': [(self.env.ref('hr.hr_kanban_view_employees').id, 'kanban'),
                          (self.env.ref('birthday_check.hr_employee_birthday_tree2').id, 'tree'),
                          (self.env.ref('hr_employee_stpi.view_add_Employee_doc_form').id, 'form')],
                'type': 'ir.actions.act_window'
            }
