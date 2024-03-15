from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import mysql.connector
import hashlib

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

class LevelValueMapping(BaseModel):
    level_id: str
    level_type: str
    allowed_values: List[str]

class KeyCriteria(BaseModel):
    KC1: str = None
    KC2: str = None
    KC3: str = None
    KC4: str = None
    KC5: str = None
    KC6: str = None
    KC7: str = None
    KC8: str = None
    KC9: str = None
    KC10: str = None
    question_sequence_Array: List[dict[str, int]]



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

@app.post("/add_key_criteria/")
def add_key_criteria(mapping: LevelValueMapping):
    level_id = mapping.level_id
    level_type = mapping.level_type
    
    # Insert each allowed value as a separate record
    for allowed_value in mapping.allowed_values:
        sql = "INSERT INTO level_value_mapping (level_id, level_type, allowed_value) VALUES (%s, %s, %s)"
        val = (level_id, level_type, allowed_value)
        mycursor.execute(sql, val)
        mydb.commit()
    
    return {"message": "Key criteria added successfully"}

@app.get("/view_key_criteria/")
def view_key_criteria():
    # Fetch all key criteria
    mycursor.execute("SELECT * FROM level_value_mapping")
    result = mycursor.fetchall()
    if not result:
        raise HTTPException(status_code=404, detail="No key criteria found")
    return {"key_criteria": result}

@app.put("/update_key_criteria/{level_id}")
def update_key_criteria(level_id: str, mapping: LevelValueMapping):
    # Delete existing key criteria for the given level_id
    delete_sql = "DELETE FROM level_value_mapping WHERE level_id = %s"
    delete_val = (level_id,)
    mycursor.execute(delete_sql, delete_val)
    mydb.commit()
    
    # Insert new key criteria
    insert_sql = "INSERT INTO level_value_mapping (level_id, level_type, allowed_value) VALUES (%s, %s, %s)"
    for allowed_value in mapping.allowed_values:
        insert_val = (level_id, mapping.level_type, allowed_value)
        mycursor.execute(insert_sql, insert_val)
        mydb.commit()

    return {"message": f"Key criteria with ID {level_id} updated successfully"}

@app.delete("/delete_key_criteria/{level_id}")
def delete_key_criteria(level_id: str):
    sql = "DELETE FROM level_value_mapping WHERE level_id = %s"
    val = (level_id,)
    mycursor.execute(sql, val)
    mydb.commit()
    if mycursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Key criteria not found")
    return {"message": f"Key criteria with ID {level_id} deleted successfully"}

@app.post("/create_records/")
async def create_records(key_criteria_list: List[KeyCriteria]):
    for key_criteria in key_criteria_list:
        kc_values = [getattr(key_criteria, f"KC{i}", None) for i in range(1, 11)]
        kc_columns = [f"KC{i}" for i in range(1, 11) if getattr(key_criteria, f"KC{i}", None) is not None]
        
        # Extract question IDs and sequences from the request
        question_sequence_array = key_criteria.question_sequence_Array
        
        # Validate request data
        if len(question_sequence_array) == 0:
            raise HTTPException(status_code=400, detail="At least one question-sequence pair must be provided")
        
        for item in question_sequence_array:
            if "question_id" not in item or "sequence_id" not in item:
                raise HTTPException(status_code=400, detail="Each item in question_sequence_Array must have question_id and sequence_id")
            
            question_id = item["question_id"]
            sequence_id = item["sequence_id"]
            
            # Calculate hexcode based on combinations of KC1 to KC10
            key_combination = hashlib.md5(''.join(filter(None, kc_values)).encode()).hexdigest()
            
            # Build SQL query and values
            sql = f"INSERT INTO Question_sequence_layout ({', '.join(kc_columns)}, question_id, sequence, KEY_COMBINATION) VALUES ({', '.join(['%s'] * len(kc_columns))}, %s, %s, %s)"
            val = tuple(filter(None, kc_values)) + (question_id, sequence_id, key_combination)
            
            # Execute SQL query
            mycursor.execute(sql, val)
            mydb.commit()
    
    return {"message": "Records created successfully"}

# Update records endpoint
@app.put("/update_records/{key_combination}")
async def update_records(key_combination: str, key_criteria: KeyCriteria):
    kc_values = [getattr(key_criteria, f"KC{i}", None) for i in range(1, 11)]
    kc_columns = [f"KC{i}=%s" for i in range(1, 11) if getattr(key_criteria, f"KC{i}", None) is not None]
    
    if not kc_columns:
        raise HTTPException(status_code=400, detail="At least one KC column must be provided")
    
    sql = f"UPDATE Question_sequence_layout SET {', '.join(kc_columns)} WHERE KEY_COMBINATION = %s"
    val = [v for v in kc_values if v is not None] + [key_combination]
    
    mycursor.execute(sql, val)
    mydb.commit()
    
    # Update question_sequence_Array if provided
    if key_criteria.question_sequence_Array:
        for item in key_criteria.question_sequence_Array:
            question_id = item["question_id"]
            sequence_id = item["sequence_id"]
            
            # Update SQL query and values
            sql = "UPDATE Question_sequence_layout SET sequence = %s WHERE question_id = %s AND KEY_COMBINATION = %s"
            val = (sequence_id, question_id, key_combination)
            
            mycursor.execute(sql, val)
            mydb.commit()
    
    return {"message": f"Records with key_combination '{key_combination}' updated successfully"}

# Delete records endpoint
@app.delete("/delete_records/{key_combination}")
async def delete_records(key_combination: str):
    sql = "DELETE FROM Question_sequence_layout WHERE KEY_COMBINATION = %s"
    val = (key_combination,)
    
    mycursor.execute(sql, val)
    mydb.commit()
    
    return {"message": f"Records with key_combination '{key_combination}' deleted successfully"}

# Show records endpoint based on key_combination
@app.get("/show_records/{key_combination}")
async def show_records(key_combination: str):
    sql = "SELECT * FROM your_table WHERE KEY_COMBINATION = %s"
    val = (key_combination,)
    
    mycursor.execute(sql, val)
    records = mycursor.fetchall()
    
    if not records:
        raise HTTPException(status_code=404, detail=f"No records found with key_combination '{key_combination}'")
    
    return records


# Main function
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

