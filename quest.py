from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector

# Connect to your MySQL database
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="password",
  database="AI_STG"
)

# Create a cursor object using the cursor() method
mycursor = mydb.cursor()

# Example database models
class MasterQuestionnaireModel(BaseModel):
    question_id: int
    question_type: str
    description: str
    multiple_selection_allowed: bool

class QuestionValueModel(BaseModel):
    value_id: int
    question_id: int
    allowed_values: List[str]

# FastAPI app
app = FastAPI()

# API Endpoints
class MasterQuestionnaireCreate(BaseModel):
    question_type: str
    description: str
    multiple_selection_allowed: bool

class QuestionValue(BaseModel):
    allowed_values: List[str]

@app.post("/add_questionnaire/")
def add_questionnaire(master_questionnaire: MasterQuestionnaireCreate, question_values: List[QuestionValue]):
    # Insert master questionnaire
    sql = "INSERT INTO master_questionnaire (question_type, description, multiple_selection_allowed) VALUES (%s, %s, %s)"
    val = (master_questionnaire.question_type, master_questionnaire.description, master_questionnaire.multiple_selection_allowed)
    mycursor.execute(sql, val)
    mydb.commit()
    
    question_id = mycursor.lastrowid
    
    # Insert question values
    for qv in question_values:
        sql = "INSERT INTO question_values (question_id, allowed_values) VALUES (%s, %s)"
        val = (question_id, ','.join(qv.allowed_values))
        mycursor.execute(sql, val)
        mydb.commit()

    return {"message": "Questionnaire added successfully"}

@app.get("/get_questionnaires/")
def get_questionnaires():
    # Fetch all master questionnaires
    mycursor.execute("SELECT * FROM master_questionnaire")
    master_questionnaires_data = mycursor.fetchall()
    
    questionnaires = []
    for mq_data in master_questionnaires_data:
        master_questionnaire = MasterQuestionnaireModel(question_id=mq_data[0], question_type=mq_data[1], description=mq_data[2], multiple_selection_allowed=bool(mq_data[3]))
        
        # Fetch question values for each master questionnaire
        mycursor.execute("SELECT * FROM question_values WHERE question_id = %s", (mq_data[0],))
        question_values_data = mycursor.fetchall()
        
        question_values = []
        for qv_data in question_values_data:
            question_values.append(QuestionValueModel(question_id=qv_data[0], value_id=qv_data[1], allowed_values=qv_data[2].split(',')))
        
        questionnaires.append({"master_questionnaire": master_questionnaire.dict(), "question_values": [qv.dict() for qv in question_values]})
    
    return questionnaires


@app.put("/update_questionnaire/{question_id}")
def update_questionnaire(question_id: int, master_questionnaire: MasterQuestionnaireCreate, question_values: List[QuestionValue]):
    # Check if question ID exists
    mycursor.execute("SELECT COUNT(*) FROM master_questionnaire WHERE question_id = %s", (question_id,))
    result = mycursor.fetchone()
    if result[0] == 0:
        raise HTTPException(status_code=404, detail="Questionnaire not found")

    # Update master questionnaire
    sql = "UPDATE master_questionnaire SET question_type = %s, description = %s, multiple_selection_allowed = %s WHERE question_id = %s"
    val = (master_questionnaire.question_type, master_questionnaire.description, master_questionnaire.multiple_selection_allowed, question_id)
    mycursor.execute(sql, val)
    mydb.commit()
    
    # Delete existing question values
    sql = "DELETE FROM question_values WHERE question_id = %s"
    val = (question_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    
    # Insert updated question values
    for qv in question_values:
        sql = "INSERT INTO question_values (question_id, allowed_values) VALUES (%s, %s)"
        val = (question_id, ','.join(qv.allowed_values))
        mycursor.execute(sql, val)
        mydb.commit()

    return {"message": f"Questionnaire with ID {question_id} updated successfully"}

@app.delete("/delete_questionnaire/{question_id}")
def delete_questionnaire(question_id: int):
    # Delete master questionnaire
    sql = "DELETE FROM master_questionnaire WHERE question_id = %s"
    val = (question_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    
    # Delete question values
    sql = "DELETE FROM question_values WHERE question_id = %s"
    val = (question_id,)
    mycursor.execute(sql, val)
    mydb.commit()

    return {"message": f"Questionnaire with ID {question_id} deleted successfully"}

# Main function
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

