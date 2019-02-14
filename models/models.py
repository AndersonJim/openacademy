 #-*- coding: utf-8 -*-

from datetime import timedelta
from odoo import models, fields, api, exceptions, _


class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Es parte del curso de open academy'

    name = fields.Char(string=_('Title'), required=True)
    description = fields.Text()
    resp_user_id = fields.Many2one('res.users', on_delete='set null', string='Responsible', index=True)
    session_ids = fields.One2many('openacademy.session', 'course_id', string="Sessions")

    #_sql_constraints  es un array de constraint 
    #estructura de un contraint (nombre del constraint, sentencia sql, mensaje de error)
    #when a field is unique cant use duplicated
    _sql_constraints = [('name_course_unique', 'UNIQUE(name)', 'This course title is in use.'), 
                        ('name_desc_must_diff', 'CHECK(name != description)', 'Title must not be in description.')]

    @api.multi
    def copy(self, default=None):
        default = dict(default or {})

        copied_count = self.search_count(
            [('name', '=like', _("Copy of {}%").format(self.name))])
        if not copied_count:
            new_name = _("Copy of {}").format(self.name)
        else:
            new_name = _("Copy of {} ({})").format(self.name, copied_count)

        default['name'] = new_name
        #llama al metodo copy de la clase padre, y le pasa el diccionario con el campo a cambiar y retorna
        return super(Course, self).copy(default)


class Session(models.Model):
    _name = 'openacademy.session'
    _description = "sessiones de los cursos"

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), string=_('duration'), help=_("Duration in days")) #por si el curso dura mediodia asi se puede representar
    end_date = fields.Date(string=_('End date'),compute='_end_date')
    seats = fields.Integer(string=_("Seat's number"), required=True)

    instructor_id = fields.Many2one('res.partner', string='Instructor', domain=['|', ('is_instructor', '=', True),'|',('category_id.name', 'ilike', 'Teacher'), ('category_id.parent_id.name', 'ilike', 'Teacher')])
    course_id = fields.Many2one('openacademy.course', on_delete='cascade', string='Course', required=True)
    attendee_ids = fields.Many2many('res.partner', string=_("Attendees"))
    taken_seats = fields.Float(digits=(6, 2), compute='_taken_seats', string=_('Taken seats'))
    
    color = fields.Integer()

    
    #en un computed field el onchange esta por default
    #self es en este caso es un recordset -> [row,row,rows]
    @api.depends('seats','attendee_ids')
    def _taken_seats(self):
        for record in self:
            if record.seats > 0:
                record.taken_seats = float(len(record.attendee_ids)/record.seats) * 100  

    @api.depends('duration', 'start_date')
    def _end_date(self):
        for record in self:
            if not (record.start_date and record.duration):
                record.end_date = record.start_date
                continue

            start = fields.Datetime.from_string(record.start_date)
            duration = timedelta(days=record.duration, seconds=-1)
            record.end_date = str(start + duration)

    
    @api.onchange('seats','attendee_ids')
    def _verify_valid_seats(self):
        for rec in self:
            if rec.seats < 0:
                return {
                    'warning': {
                        'title': _("Incorrect 'seats' value"),
                        'message': _("The number of available seats may not be negative"),
                    },
                }
            if rec.seats < len(rec.attendee_ids):
                return {
                    'warning': {
                        'title': _("Too many attendees"),
                        'message': _("Increase seats or remove excess attendees"),
                    },
                }