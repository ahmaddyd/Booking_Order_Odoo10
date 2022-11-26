from odoo import api, fields, models, exceptions, _
from odoo.osv import osv
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import logging

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_booking_order = fields.Boolean(string='Is Booking Order')

    team = fields.Many2one(comodel_name='service.team', string='Team')
    team_leader = fields.Many2one(comodel_name='res.users', string='Team Leader')
    team_members = fields.Many2many(comodel_name='res.users', string='Team Members')

    bo_start = fields.Datetime(string='Booking Start')
    bo_end = fields.Datetime(string='Booking End')

    work_order_count = fields.Integer(string='Work Order', compute='_compute_work_order_count')

    def _compute_work_order_count(self):
        work_order_data = self.env['work.order'].sudo().read_group([('booking_order_reference', 'in', self.ids)],
                                                                   ['booking_order_reference'],
                                                                   ['booking_order_reference'])

        result = dict(
            (data['booking_order_reference'][0], data['booking_order_reference_count']) for data in work_order_data)

        for wo in self:
            wo.work_order_count = result.get(wo.id, 0)

    @api.onchange('team')
    def _onchange_team(self):
        search = self.env['service.team'].search([('id', '=', self.team.id)])

        team_members = []

        for team in search:
            for members in team.team_members:
                team_members.append(members.id)
            self.team_leader = team.team_leader.id
            self.team_members = team_members

    @api.multi
    def action_check(self):
        for check in self:
            wo = self.env['work.order'].search(['|', '|', '|', ('team_leader', 'in', [g.id for g in self.team_members]),
                                                ('team_members', 'in', [self.team_leader.id]),
                                                ('team_leader', '=', self.team_leader.id),
                                                ('team_members', 'in', [g.id for g in self.team_members]),
                                                ('state', '!=', 'cancelled'), ('planned_start', '<=', self.bo_end),
                                                ('planned_end', '>=', self.bo_start)], limit=1)

            if wo:
                raise osv.except_osv(_('Warning!'), _('Team already has work order during that period on SOXX'))
            else:
                raise osv.except_osv(_('Warning!'), _('Team is available for booking'))

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            wo = self.env['work.order'].search(['|', '|', '|', ('team_leader', 'in', [g.id for g in self.team_members]),
                                                ('team_members', 'in', [self.team_leader.id]),
                                                ('team_leader', '=', self.team_leader.id),
                                                ('team_members', 'in', [g.id for g in self.team_members]),
                                                ('state', '!=', 'cancelled'), ('planned_start', '<=', self.bo_end),
                                                ('planned_end', '>=', self.bo_start)], limit=1)

            if wo:
                raise osv.except_osv(_('Warning!'), _('Team is not available during this period, already booked on '
                                                      'SOXX. Please book on another date.'))
            order.action_work_order_create()

        return res

    @api.multi
    def action_work_order_create(self, grouped=False, final=False):
        work_order_object = self.env['work.order']
        for order in self:
            work_order = work_order_object.create({'booking_order_reference': order.id,
                                                   'team': order.team.id,
                                                   'team_leader': order.team_leader.id,
                                                   'team_members': [(4, order.team_members.ids)],
                                                   'planned_start': order.bo_start,
                                                   'planned_end': order.bo_end, })
