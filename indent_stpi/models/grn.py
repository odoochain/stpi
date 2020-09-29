from odoo import api, fields, models, _
from odoo.exceptions import ValidationError, UserError
from dateutil.relativedelta import relativedelta
from datetime import datetime, date

class EmployeeIndentGrn(models.Model):
    _name = 'grn'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Indent Grn'

    def _default_employee(self):
        return self.env['hr.employee'].sudo().search([('user_id', '=', self.env.uid)], limit=1)

    grn_sequence = fields.Char('GRN number',track_visibility='always')
    employee_id = fields.Many2one('hr.employee', string='Requested By', default=_default_employee ,track_visibility='always')
    branch_id = fields.Many2one('res.branch', string='Branch', store=True)
    job_id = fields.Many2one('hr.job', string='Functional Designation', store=True)
    department_id = fields.Many2one('hr.department', string='Department', store=True)
   
    item_ids = fields.One2many('grn.items','request_id', string='Relatives')
   
    state = fields.Selection([('draft', 'Draft'), ('to_approve', 'To Approve'), ('approved', 'Approved'), ('rejected', 'Rejected')
                               ], required=True, default='draft',track_visibility='always', string='Status')


    @api.onchange('employee_id')
    @api.constrains('employee_id')
    def onchange_emp_get_base(self):
        for rec in self:
            rec.job_id = rec.employee_id.job_id.id
            rec.department_id = rec.employee_id.department_id.id
            rec.branch_id = rec.employee_id.branch_id.id

    @api.multi
    def button_to_approve(self):
        for res in self:
            res.write({'state': 'to_approve'})
          
          
    @api.multi
    def button_approved(self):
        for res in self:
            res.write({'state': 'approved'})
            for item in res.item_ids:
                create_ledger_family = self.env['issue.request'].sudo().create(
                    {
                        'Indent_id': res.id,
                        'employee_id': res.employee_id.id,
                        'branch_id': res.branch_id.id,
                        'Indent_item_id': item.id,
                        'item_category_id': item.item_category_id.id,
                        'item_id': item.item_id.id,
                        'specification': item.specification,
                        'requested_quantity': item.requested_quantity,
                        'requested_date': item.requested_date,
                        'indent_state': res.state,
                        'state': 'to_approve',
                    }
                )



    @api.multi
    def button_reject(self):
        for rec in self:
            rec.write({'state': 'rejected'})

    @api.multi
    def button_reset_to_draft(self):
        for rec in self:
            rec.write({'state': 'draft'})

    @api.model
    def create(self, vals):
        res =super(EmployeeIndentGrn, self).create(vals)
        seq = self.env['ir.sequence'].next_by_code('grn')
        sequence = 'IR' + seq
        res.indent_sequence = sequence
        search_id = self.env['grn'].search(
            [('employee_id', '=', res.employee_id.id),
             ('state', 'not in', ['approved','rejected']), ('id', '!=', res.id)])
        for emp in search_id:
            if emp:
                raise ValidationError(
                    "One of the Indent Grn is already in process.")
        return res

    @api.multi
    @api.depends('indent_sequence')
    def name_get(self):
        res = []
        for record in self:
            if record.indent_sequence:
                name = record.indent_sequence
            else:
                name = 'IR'
            res.append((record.id, name))
        return res



class FamilyDetails(models.Model):
    _name = 'grn.items'
    _description = "Indent Item Details"


    @api.onchange('item_category_id')
    def change_item_category_id(self):
        return {'domain': {'item_id': [('child_indent_stock', '=', self.item_category_id.id)
            ]}}

    request_id = fields.Many2one('grn', string='Relative ID')
    item_category_id = fields.Many2one('indent.stock', string='Item Category')
    item_id = fields.Many2one('child.indent.stock', string='Item')
    specification = fields.Text('Specifications')
    requested_quantity = fields.Integer('Requested Quantity')
    approved_quantity = fields.Integer('Approved Quantity')
    requested_date = fields.Date('Requested Date', default=fields.Date.today())
    approved_date = fields.Date('Approved Date')


    @api.onchange('item_id')
    @api.constrains('item_id')
    def change_item_category_id(self):
        for rec in self:
            rec.specification = rec.item_id.specification