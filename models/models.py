 #-*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Es parte del curso de open academy'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
    resp_user_id = fields.Many2one('res.users', on_delete='set null', string='Responsible', index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")


class Session(models.Model):
    _name = 'openacademy.session'
    _description = "sessiones de los cursos"

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days") #por si el curso dura mediodia asi se puede representar
    seats = fields.Integer(string="Seat's number", required=True)

    instructor_id = fields.Many2one('res.partner', string='Instructor', domain=['|', ('is_instructor', '=', True),'|',('category_id.name', 'ilike', 'Teacher'), ('category_id.parent_id.name', 'ilike', 'Teacher')])
    course_id = fields.Many2one('openacademy.course', on_delete='cascade', string='Course', required=True)
    attendee_ids = fields.Many2many('res.partner', string="Attendees")
    taken_seats = fields.Float(digits=(6, 2), compute='_taken_seats', string='Taken seats')

    @api.depends('seats','attendee_ids')
    def _taken_seats(self):
        for record in self:
            record.taken_seats = float(len(record.attendee_ids)/record.seats) * 100  
