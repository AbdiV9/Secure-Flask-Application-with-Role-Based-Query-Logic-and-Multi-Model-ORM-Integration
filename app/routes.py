from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from sqlalchemy import text
from datetime import datetime
from . import db
from .models import User, Post
import logging

main = Blueprint('main', __name__)

logging = basicConfig(
     filename='app.log',
     level=logging.DEBUG,
     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
 )

 @main.route('/', methods=['GET','POST'])
 def login():
     if request.method == 'POST':
         username = request.form.get('username')
         password = request.form.get('password')
         ip_address = request.form.get('ip')

