from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey, Enum, DateTime, JSON
from sqlalchemy.orm import relationship
import enum
import datetime
from database import Base

class RoleEnum(enum.Enum):
    ADMIN = "ADMIN"
    HOD = "HOD"
    FACULTY = "FACULTY"

class StatusEnum(enum.Enum):
    PENDING = "PENDING"
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    REJECTED = "REJECTED"

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True) # Used for Login ID (Faculty ID, URK, or Admin)
    password_hash = Column(String)
    role = Column(Enum(RoleEnum), default=RoleEnum.FACULTY)
    is_active = Column(Boolean, default=True)

    faculty_profile = relationship("FacultyProfile", back_populates="user", uselist=False)

class Department(Base):
    __tablename__ = "departments"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True) # e.g. EC, CS
    full_name = Column(String)

    faculties = relationship("FacultyProfile", back_populates="department")
    students = relationship("Student", back_populates="department")

class FacultyProfile(Base):
    __tablename__ = "faculty_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    faculty_id = Column(String, unique=True, index=True) # e.g. FAC25EC001
    
    full_name = Column(String)
    gender = Column(String)
    dob = Column(Date)
    contact = Column(String)
    address = Column(String)
    
    department_id = Column(Integer, ForeignKey("departments.id"))
    position = Column(String)
    experience_years = Column(Integer)
    join_date = Column(Date)
    
    highest_qualification = Column(String)
    specialisation = Column(String)
    biometric_photo_url = Column(String, nullable=True)

    # New fields from CSV/XLSX requirements
    age = Column(Integer, nullable=True)
    pan = Column(String, nullable=True)
    total_industry_experience = Column(Integer, nullable=True)
    type_of_association = Column(String, nullable=True)
    currently_working_or_not = Column(String, nullable=True)
    dol = Column(Date, nullable=True) # Date of leaving
    source_of_record = Column(String, nullable=True)
    
    
    status = Column(Enum(StatusEnum), default=StatusEnum.PENDING)

    user = relationship("User", back_populates="faculty_profile")
    department = relationship("Department", back_populates="faculties")

class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    urk_id = Column(String, unique=True, index=True) # e.g. URK25EC001
    
    name = Column(String)
    department_id = Column(Integer, ForeignKey("departments.id"))
    year_of_study = Column(Integer)
    phone = Column(String)
    parent_name = Column(String)
    barcode = Column(String, unique=True, index=True) # Tied to URK ID

    department = relationship("Department", back_populates="students")

class IdSequence(Base):
    """
    Table to support atomic ID generation locking.
    key format: "FAC-25-EC" or "URK-25-CS"
    """
    __tablename__ = "id_sequences"
    
    key = Column(String, primary_key=True, index=True)
    last_value = Column(Integer, default=0)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # The user who performed action
    action = Column(String) # e.g. "FACULTY_APPROVED", "HOD_ASSIGNED"
    entity = Column(String) # e.g. "FacultyProfile", "Department"
    details = Column(String) # JSON string of additional details

class TimetableSlot(Base):
    __tablename__ = "timetable_slots"

    id = Column(Integer, primary_key=True, index=True)
    faculty_id = Column(Integer, ForeignKey("users.id"))
    department_id = Column(Integer, ForeignKey("departments.id"))
    year_of_study = Column(Integer)
    subject = Column(String)
    day_of_week = Column(Integer) # 0=Monday, 6=Sunday
    period = Column(Integer) # 1 to 8

    # Note: In a full app, we'd add relationships back to FacultyProfile/User/Department

class ClassAttendance(Base):
    """Daily auto-generated register for specific Slot period."""
    __tablename__ = "class_attendance"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    period = Column(Integer)
    slot_id = Column(Integer, ForeignKey("timetable_slots.id"))
    student_id = Column(Integer, ForeignKey("students.id"))
    
    status = Column(String, default="ABSENT") # PRESENT, ABSENT, EVENT_EXCUSED
    marked_method = Column(String, nullable=True) # "SCAN" or "MANUAL"
    is_marked = Column(Boolean, default=False) # Marked by faculty?

class FacultyBiometricAttendance(Base):
    """Daily attendance for the faculty themselves."""
    __tablename__ = "faculty_biometric_attendance"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_user_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    status = Column(String) # PRESENT, ABSENT, EXCUSED, UNMARKED
    verified_by_user_id = Column(Integer, ForeignKey("users.id"), nullable=True) # HOD or Admin

class LeaveApplication(Base):
    __tablename__ = "leave_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    faculty_user_id = Column(Integer, ForeignKey("users.id"))
    start_date = Column(Date)
    end_date = Column(Date)
    reason = Column(String)
    status = Column(String, default="PENDING") # APPROVED, REJECTED

class SubstituteAssignment(Base):
    __tablename__ = "substitute_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    leave_application_id = Column(Integer, ForeignKey("leave_applications.id"))
    original_faculty_id = Column(Integer, ForeignKey("users.id"))
    substitute_faculty_id = Column(Integer, ForeignKey("users.id"))
    date = Column(Date)
    reason = Column(String)
    status = Column(String, default="PENDING")
    slot_id = Column(Integer, ForeignKey("timetable_slots.id"))

class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(String)
    date = Column(DateTime, default=datetime.datetime.utcnow)
    target_department_id = Column(Integer, ForeignKey("departments.id"), nullable=True) # Null means global
    created_by_user_id = Column(Integer, ForeignKey("users.id"))
    is_active = Column(Boolean, default=True)
