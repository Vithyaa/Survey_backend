from typing import Union
import io
from io import BytesIO
from app.models import User,Answer
from app.send_email import send_email_with_attachment
from fastapi import FastAPI, Depends
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Dict
from pydantic import BaseModel 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from email import encoders
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = FastAPI()

@app.get("/")
def read_root():
    return {"Success": "Survey_backend"}

class UserCreate(BaseModel):
    email: str
    name: str
    language: int
    age: int
    response_data: List[Dict[str, int]]

def process_and_concatenate_strings(answer: Answer, language: int) -> str:
    result = ""
    if language == 1:
        result += answer.english_text
    elif language == 2:
        result += answer.japanese_text

    # Remove only integers and add a line break between each string
    result = '\n'.join([''.join([''.join(filter(lambda x: not x.isdigit() or (x.isdigit() and x == '.'), char)) for char in word]) for word in result.split('\n')])

    return result

def generate_pretty_pdf(concatenated_text):
    pdf_buffer = BytesIO()

    # Create a PDF document
    pdf = canvas.Canvas(pdf_buffer, pagesize=letter)
    
    # Set font and size
    pdf.setFont("Helvetica", 12)

    # Add title
    pdf.drawCentredString(letter[0] / 2, letter[1] - 50, "User Registration Details")

    # Add content
    y_position = letter[1] - 100
    for line in concatenated_text.split(','):
        pdf.drawString(100, y_position, line.strip())
        y_position -= 20

    # Save the PDF to the buffer
    pdf.save()

    # Get the PDF bytes
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_bytes

@app.post("/test")
async def test_read_root(user_data: UserCreate, db: Session = Depends(get_db)):
    # Check if there are records in the answers table that match the provided response_data
    concatenated_text = ""
    
    for response_item in user_data.response_data:
        question_id = response_item.get("question_id")
        response_one_id = response_item.get("response_one_id")
        response_two_id = response_item.get("response_two_id", None)  # Add this line

        answer = (
            db.query(Answer)
            .filter(
                and_(
                    Answer.questioned_id == question_id,
                    Answer.response_one_id == response_one_id,
                    Answer.response_two_id == response_two_id,
                    Answer.deleted == 0,
                    Answer.record_status == 1,
                )
            )
            .first()
        )

        if answer:
            concatenated_text += process_and_concatenate_strings(answer, user_data.language) + " ,"

    # Save concatenated_text to the user table
    new_user = User(
        email=user_data.email,
        name=user_data.name,
        language_id=user_data.language,
        age=user_data.age,
        answer=concatenated_text.strip(),
        # Add other fields from the user_data if needed
    )
    db.add(new_user)
    db.commit()

    # Generate a pretty PDF
    pdf_content = generate_pretty_pdf(concatenated_text)

    # Attach the PDF to the email and send it
    send_email_with_attachment(user_data.email, pdf_content)

    return {"Hello": "Data saved and email sent"}
