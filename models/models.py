 #-*- coding: utf-8 -*-

from odoo import models, fields, api

class Course(models.Model):
    _name = 'openacademy.course'
    _description = 'Es parte del curso de open academy'

    name = fields.Char(string='Title', required=True)
    description = fields.Text()
