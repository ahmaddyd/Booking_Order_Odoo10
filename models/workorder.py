from odoo import api, fields, models, exceptions, _
from odoo.osv import osv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import logging

_logger = logging.getLogger(__name__)


class WorkOrder(models.Model):
    _name = 'work.order'
    _description = 'Description Work Order'
    _rec_name = "work_order_number"

    work_order_number = fields.Char(string='WO Number', required=True, readonly=True, copy=False,
                                    default=lambda self: _('New'))

    booking_order_reference = fields.Many2one(comodel_name='sale.order', readonly=True)

    team = fields.Many2one(comodel_name='service.team', required=True)
    team_leader = fields.Many2one(comodel_name='res.users', string='Team Leader', required=True)
    team_members = fields.Many2many(comodel_name='res.users', string='Team Members')

    planned_start = fields.Datetime(string="Planned Start", required=True)
    planned_end = fields.Datetime(string='Planned End', required=True)
    date_start = fields.Datetime(string='Date Start', readonly=True)
    date_end = fields.Datetime(string='Date End', readonly=True)

    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')],
        string='State', default='pending', track_visibility='onchange')

    note = fields.Text(string='Note')

    @api.model
    def create(self, vals):
        if vals.get('work_order_number', _('New')) == _('New'):
            if 'company_id' in vals:
                vals['work_order_number'] = self.env['ir.sequence'].with_context(
                    force_company=vals['company_id']).next_by_code(
                    'work.order') or _('New')
            else:
                vals['work_order_number'] = self.env['ir.sequence'].next_by_code('work.order') or _('New')

        result = super(WorkOrder, self).create(vals)

        return result

    @api.multi
    def start_work(self):
        return self.write({'state': 'in_progress', 'date_start': str(datetime.now())})

    @api.multi
    def end_work(self):
        return self.write({'state': 'done', 'date_end': str(datetime.now())})

    @api.multi
    def reset(self):
        return self.write({'state': 'pending', 'date_start': ''})

    @api.multi
    def cancel(self):
        return self.write({'state': 'cancelled'})
