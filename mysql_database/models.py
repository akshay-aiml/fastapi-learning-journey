# Column:
# Used to create table columns

# Integer:
# Integer data type

# String:
# String/VARCHAR data type

from sqlalchemy import Column, Integer, String


# =========================================================
# Import Base Class
# =========================================================
# Base is the parent class for all ORM models

from database import Base


# =========================================================
# USER MODEL
# =========================================================
# This class represents the "users" table in database

class User(Base):

    # -----------------------------------------------------
    # Table Name
    # -----------------------------------------------------
    __tablename__ = "users"


    # =====================================================
    # TABLE COLUMNS
    # =====================================================

    # Primary Key
    id = Column(
        Integer,
        primary_key=True,
        index=True
    )


    # User Name
    name = Column(
        String(100),
        nullable=False
    )


    # User Email
    email = Column(
        String(100),
        unique=True,
        nullable=False
    )


    # User Age
    age = Column(
        Integer,
        nullable=False
    )