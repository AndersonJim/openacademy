 #-*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Es parte del curso de open academy'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()

class Session(models.Model):
    _name = 'openacademy.session'
    _description = "sessiones de los cursos"

    name = fields.Char(required=True)
    start_date = fields.Date()
    duration = fields.Float(digits=(6, 2), help="Duration in days") #por si el curso dura mediodia asi se puede representar
    seats = fields.Integer(string="Seat's number")