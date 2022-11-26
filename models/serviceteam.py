from odoo import api, fields, models


class ServiceTeam(models.Model):
    _name = 'service.team'
    _description = 'Description Service Team'

    name = fields.Char(string='Team Name', required=True)
    team_leader = fields.Many2one(comodel_name='res.users',
                                  string='Team Leader',
                                  required=True)
    team_members = fields.Many2many(comodel_name='res.users',
                                    string='Team Members')
