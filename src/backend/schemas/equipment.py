"""
Equipment data models for HVAC AI Diagnostic.
These define the structure of equipment data in our API.
"""
from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum


class EquipmentType(str, Enum):
    """Types of HVAC equipment."""
    AIR_CONDITIONER = "air_conditioner"
    HEAT_PUMP = "heat_pump"
    FURNACE = "furnace"
    BOILER = "boiler"
    WATER_HEATER = "water_heater"
    DUCTWORK = "ductwork"
    THERMOSTAT = "thermostat"


class EquipmentStatus(str, Enum):
    """Equipment operational status."""
    WORKING = "working"
    NEEDS_MAINTENANCE = "needs_maintenance"
    BROKEN = "broken"
    UNKNOWN = "unknown"


class Symptom(BaseModel):
    """A symptom that can indicate equipment problems."""
    name: str = Field(..., description="Name of the symptom")
    description: str = Field(..., description="Description of what this symptom means")
    severity: int = Field(..., ge=1, le=5, description="Severity from 1 (minor) to 5 (critical)")


class Equipment(BaseModel):
    """Basic equipment information."""
    id: Optional[int] = Field(None, description="Equipment ID")
    name: str = Field(..., description="Equipment name/model")
    equipment_type: EquipmentType = Field(..., description="Type of HVAC equipment")
    manufacturer: str = Field(..., description="Equipment manufacturer")
    model: str = Field(..., description="Equipment model number")
    year_installed: Optional[int] = Field(None, description="Year equipment was installed")
    status: EquipmentStatus = Field(EquipmentStatus.UNKNOWN, description="Current status")
    location: str = Field(..., description="Location of equipment (e.g., 'Basement', 'Roof')")


class DiagnosticRequest(BaseModel):
    """Request for equipment diagnosis."""
    equipment_id: Optional[int] = Field(None, description="ID of equipment to diagnose")
    equipment_type: EquipmentType = Field(..., description="Type of equipment")
    symptoms: List[str] = Field(..., description="List of observed symptoms")
    additional_notes: Optional[str] = Field(None, description="Additional observations")


class DiagnosticResult(BaseModel):
    """Result of equipment diagnosis."""
    equipment_type: EquipmentType
    symptoms: List[str]
    possible_causes: List[str] = Field(..., description="Likely causes of the problem")
    recommended_actions: List[str] = Field(..., description="Suggested repair actions")
    urgency: int = Field(..., ge=1, le=5, description="Urgency level from 1 (low) to 5 (emergency)")
    estimated_cost: Optional[str] = Field(None, description="Estimated repair cost range")


class EquipmentCreate(BaseModel):
    """Data needed to create new equipment."""
    name: str
    equipment_type: EquipmentType
    manufacturer: str
    model: str
    year_installed: Optional[int] = None
    location: str


class EquipmentUpdate(BaseModel):
    """Data for updating equipment."""
    name: Optional[str] = None
    status: Optional[EquipmentStatus] = None
    location: Optional[str] = None


# Example data for testing
SAMPLE_EQUIPMENT = [
    Equipment(
        id=1,
        name="Main AC Unit",
        equipment_type=EquipmentType.AIR_CONDITIONER,
        manufacturer="Carrier",
        model="25HCB4-1234",
        year_installed=2020,
        status=EquipmentStatus.WORKING,
        location="Backyard"
    ),
    Equipment(
        id=2,
        name="Basement Furnace", 
        equipment_type=EquipmentType.FURNACE,
        manufacturer="Trane",
        model="S9X2-8090",
        year_installed=2018,
        status=EquipmentStatus.NEEDS_MAINTENANCE,
        location="Basement"
    ),
    Equipment(
        id=3,
        name="Living Room Thermostat",
        equipment_type=EquipmentType.THERMOSTAT,
        manufacturer="Nest",
        model="Learning-3rd-Gen",
        year_installed=2021,
        status=EquipmentStatus.WORKING,
        location="Living Room"
    )
]

# Common symptoms for different equipment types
COMMON_SYMPTOMS = {
    EquipmentType.AIR_CONDITIONER: [
        "Not cooling",
        "Strange noises",
        "Ice formation",
        "Water leaking",
        "High energy bills",
        "Frequent cycling"
    ],
    EquipmentType.FURNACE: [
        "Not heating",
        "Strange odors",
        "Pilot light out",
        "Loud noises",
        "Uneven heating",
        "Yellow flame"
    ],
    EquipmentType.HEAT_PUMP: [
        "Not heating or cooling",
        "Ice on outdoor unit",
        "Strange noises",
        "High energy costs",
        "Short cycling"
    ]
}