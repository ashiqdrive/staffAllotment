from reportlab.pdfgen import canvas
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.units import inch

def generatePdf:
	myCanvas = Canvas('myfile.pdf', pagesize=letter)
	mycanvas.translate(inch,inch)



