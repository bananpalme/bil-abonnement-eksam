from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os

# --- Konfiguration med SQLite ---
# SQLite gemmer databasen i en fil (app.db) og kræver ingen separat server.
DATABASE_URL = os.environ.get(
    "DATABASE_URL",
    # Fallback til SQLite for lokal udvikling hvis DATABASE_URL ikke er sat
    # Dette gør det nemt at køre uden PostgreSQL.
    "sqlite:///./returnservice_local.db"
)
# VIGTIGT: I Flask appen (app.py) skal du sikre dig, at
# mappen /app er et volumen, så dataen er persistent, 
# ellers forsvinder den, når containeren stopper.

Base = declarative_base()

# --- 1. Entitet: CarReturn ---
# ... (Resten af din CarReturn model forbliver den samme) ...

class CarReturn(Base):
    """
    Registrerer bilaflevering (tidspunkt, nummerplade, kontrakt-ID) og bekræftelse af nøgleafhentning.
    """
    __tablename__ = 'car_returns'
    
    id = Column(Integer, primary_key=True, index=True)
    license_plate = Column(String, index=True, nullable=False) # Nummerplade
    contract_id = Column(String, index=True, nullable=False)   # Lejekontrakt/ID
    
    return_time = Column(DateTime, default=datetime.utcnow, nullable=False) 
    status = Column(String, default='Key dropped in box')
    employee_pickup_id = Column(String, nullable=True) 

# --- Database Initialisering og Session Management ---
# VIGTIGT for SQLite: check_same_thread=False
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Opretter alle tabeller, hvis de ikke eksisterer."""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Genererer en ny database session. Sikrer at sessionen lukkes."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()