from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
import re
from datetime import datetime

class RecruitmentRoster(models.Model):
    _name = "recruitment.roster"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Recruitment Roster"
    _rec_name = 'name'

    @api.onchange('job_id')
    def get_roster_line_item(self):
        return {'domain': {'roster_line_item': [('job_id', '=', self.job_id.id), ('employee_id', '=', False)]}}



    name = fields.Char(string="Name",track_visibility='always')
    job_id = fields.Many2one('hr.job', string='Utilised By')
    employee_id = fields.Many2one('hr.employee', string='Employee')
    category_id = fields.Many2one('employee.category', string='Category')
    state = fields.Many2one('res.state', string='State')
    emp_code = fields.Char('Emp Code')
    Name_of_person = fields.Char('Name of the Person')
    Hired_category = fields.Char('Hired Category')
    date_of_apointment = fields.Date('Date of Appointment')
    remarks = fields.Text('Remarks')


    position_number = fields.Integer('Position Number')
    sc = fields.Boolean('SC')
    st = fields.Boolean('ST')
    general = fields.Boolean('General')


class Employee(models.Model):
    _inherit = "hr.employee"

    @api.onchange('job_id')
    def get_roster_line_item(self):
        return {'domain': {'roster_line_item': [('job_id', '=', self.job_id.id),('employee_id', '=', False)]}}

    roster_line_item = fields.Many2one('recruitment.roster', string="Roster line item",track_visibility='always')


    @api.constrains('roster_line_item')
    def putinto_roster_line_item(self):
        for rec in self:
            rec.roster_line_item.employee_id = rec.id
            rec.emp_code.Name_of_person = rec.identify_id
            rec.roster_line_item.Name_of_person = rec.name
            rec.roster_line_item.date_of_apointment = rec.date_of_join