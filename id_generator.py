from sqlalchemy.orm import Session
from datetime import date
from models import IdSequence, Department
from sqlalchemy.exc import NoResultFound

def get_next_sequence_number(db: Session, prefix: str, year: str, dept_code: str) -> int:
    """
    Atomically get the next sequential number for a specific Prefix, Year, and Department.
    key format: "FAC-25-EC" or "URK-25-CS"
    """
    key = f"{prefix}-{year}-{dept_code}"
    
    try:
        # Attempt to lock the row for atomic increment (supported natively in PostgreSQL; SQLite will table-lock)
        sequence = db.query(IdSequence).filter(IdSequence.key == key).with_for_update().first()
        
        if not sequence:
            # Create if it doesn't exist (Seed with 1)
            sequence = IdSequence(key=key, last_value=1)
            db.add(sequence)
            db.commit()
            return 1
            
        # Increment atomically
        sequence.last_value += 1
        db.commit()
        return sequence.last_value
        
    except Exception as e:
        db.rollback()
        raise e

def generate_faculty_id(db: Session, dept_id: int, join_date: date) -> str:
    """
    Generates Faculty ID: FAC + YY + DEPT_CODE + NNN (e.g. FAC25EC001)
    """
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise ValueError(f"Department with ID {dept_id} not found")
        
    dept_code = dept.code.upper()
    yy = str(join_date.year)[-2:]
    
    # Get atomic sequence number
    seq_num = get_next_sequence_number(db, "FAC", yy, dept_code)
    
    # Format padding 3 zeros (e.g. 1 -> 001)
    return f"FAC{yy}{dept_code}{seq_num:03d}"

def generate_student_id(db: Session, dept_id: int, join_year: int) -> str:
    """
    Generates Student ID: URK + YY + DEPT_CODE + NNN (e.g. URK25EC001)
    """
    dept = db.query(Department).filter(Department.id == dept_id).first()
    if not dept:
        raise ValueError(f"Department with ID {dept_id} not found")
        
    dept_code = dept.code.upper()
    yy = str(join_year)[-2:]
    
    seq_num = get_next_sequence_number(db, "URK", yy, dept_code)
    
    return f"URK{yy}{dept_code}{seq_num:03d}"
