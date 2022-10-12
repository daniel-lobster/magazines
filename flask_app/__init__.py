from flask import Flask, render_template, redirect, request, session, flash
app = Flask(__name__)

app.secret_key = 'e9b6b6e2eca499173a8821a392550dc972ee1ce0882c2c5f1c38e36f8e917735'