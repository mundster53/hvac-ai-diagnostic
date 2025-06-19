"""
Enhanced Equipment API endpoints for HVAC AI Diagnostic.
Now includes comprehensive diagnostics for all major HVAC equipment types.
"""
from fastapi import APIRouter, HTTPException
from typing import List, Dict
from ..schemas.equipment import (
    Equipment, 
    EquipmentCreate, 
    DiagnosticRequest, 
    DiagnosticResult,
    EquipmentType,
    SAMPLE_EQUIPMENT,
    COMMON_SYMPTOMS
)

# Create router for equipment endpoints
router = APIRouter(prefix="/equipment", tags=["equipment"])

# In-memory storage for demo (later we'll use a real database)
equipment_db = SAMPLE_EQUIPMENT.copy()

# Comprehensive diagnostic database
COMPREHENSIVE_DIAGNOSTICS = {
    EquipmentType.AIR_CONDITIONER: {
        "not cooling": {
            "causes": [
                "Dirty or clogged air filter",
                "Low refrigerant levels",
                "Frozen evaporator coils",
                "Faulty compressor",
                "Blocked condenser coils",
                "Thermostat malfunction",
                "Ductwork leaks"
            ],
            "actions": [
                "Replace air filter immediately",
                "Check for ice on indoor unit - if present, turn off system",
                "Clean outdoor condenser coils",
                "Check thermostat settings and batteries",
                "Schedule professional refrigerant level check",
                "Inspect ductwork for visible leaks"
            ],
            "urgency": 3,
            "cost": "$50 - $800 depending on cause"
        },
        "strange noises": {
            "causes": [
                "Loose fan blades or motor mounts",
                "Worn compressor bearings", 
                "Damaged fan motor",
                "Debris in outdoor unit",
                "Refrigerant leak causing hissing",
                "Electrical arcing"
            ],
            "actions": [
                "Turn off system immediately to prevent damage",
                "Check for visible debris around outdoor unit",
                "Do not attempt repairs - call professional",
                "Document the type of noise (grinding, squealing, hissing)"
            ],
            "urgency": 4,
            "cost": "$150 - $1200 depending on component"
        },
        "ice formation": {
            "causes": [
                "Dirty air filter restricting airflow",
                "Low refrigerant charge",
                "Blocked return air vents",
                "Faulty blower motor",
                "Dirty evaporator coils"
            ],
            "actions": [
                "Turn off system immediately and let ice melt completely",
                "Check and replace air filter",
                "Ensure all vents are open and unblocked",
                "Wait 24 hours before restarting",
                "Call technician if problem persists"
            ],
            "urgency": 3,
            "cost": "$100 - $600"
        },
        "high energy bills": {
            "causes": [
                "Dirty air filter reducing efficiency",
                "Old, inefficient equipment",
                "Poor insulation",
                "Ductwork leaks",
                "Oversized or undersized unit"
            ],
            "actions": [
                "Replace air filter monthly",
                "Seal visible ductwork leaks",
                "Add insulation to attic/basement",
                "Schedule energy efficiency audit",
                "Consider programmable thermostat"
            ],
            "urgency": 2,
            "cost": "$20 - $300 for DIY improvements"
        }
    },
    
    EquipmentType.FURNACE: {
        "not heating": {
            "causes": [
                "Pilot light extinguished",
                "Dirty air filter",
                "Faulty thermostat",
                "Gas supply issues",
                "Ignition system failure",
                "Heat exchanger problems"
            ],
            "actions": [
                "Check thermostat settings and batteries",
                "Replace air filter",
                "Check gas supply valve is open",
                "Attempt to relight pilot light (if safe to do so)",
                "Check circuit breakers",
                "Call gas company if you smell gas"
            ],
            "urgency": 4,
            "cost": "$75 - $1500 depending on issue"
        },
        "strange odors": {
            "causes": [
                "Gas leak (rotten egg smell)",
                "Dirty burner assembly",
                "Cracked heat exchanger",
                "Dust burning off at start of season",
                "Electrical problems"
            ],
            "actions": [
                "If gas smell: evacuate immediately and call gas company",
                "Turn off furnace if electrical burning smell",
                "Change air filter",
                "Schedule immediate professional inspection",
                "Do not use furnace until inspected"
            ],
            "urgency": 5,
            "cost": "Emergency service: $200 - $3000+"
        },
        "pilot light issues": {
            "causes": [
                "Dirty pilot orifice",
                "Faulty thermocouple",
                "Gas pressure problems",
                "Drafts extinguishing pilot",
                "Bad gas valve"
            ],
            "actions": [
                "Follow manufacturer's relight procedure",
                "Clean around pilot light area",
                "Check for drafts near furnace",
                "If pilot won't stay lit, call technician",
                "Consider upgrading to electronic ignition"
            ],
            "urgency": 3,
            "cost": "$100 - $400"
        },
        "yellow flame": {
            "causes": [
                "Insufficient combustion air",
                "Dirty burner",
                "Cracked heat exchanger",
                "Improper gas pressure",
                "Carbon monoxide production risk"
            ],
            "actions": [
                "Turn off furnace immediately",
                "Ensure proper ventilation",
                "Install carbon monoxide detector if not present",
                "Call technician immediately - safety hazard",
                "Do not use until professionally inspected"
            ],
            "urgency": 5,
            "cost": "$150 - $2500+ (safety critical)"
        }
    },
    
    EquipmentType.HEAT_PUMP: {
        "not heating in winter": {
            "causes": [
                "Heat pump in defrost mode",
                "Auxiliary heat not working",
                "Low refrigerant",
                "Outdoor unit frozen",
                "Reversing valve stuck"
            ],
            "actions": [
                "Wait 15 minutes - may be in defrost cycle",
                "Check auxiliary heat strips",
                "Clear snow/ice from outdoor unit",
                "Check air filter",
                "Verify thermostat set to 'heat' mode"
            ],
            "urgency": 4,
            "cost": "$100 - $800"
        },
        "ice on outdoor unit": {
            "causes": [
                "Normal defrost cycle operation",
                "Defrost system malfunction",
                "Low refrigerant",
                "Dirty coils",
                "Blocked airflow"
            ],
            "actions": [
                "Allow normal defrost cycle to complete (10-15 minutes)",
                "Clear debris from around unit",
                "Check that fan is operating",
                "If ice persists >30 minutes, call technician",
                "Don't pour hot water on unit"
            ],
            "urgency": 3,
            "cost": "$150 - $600"
        },
        "short cycling": {
            "causes": [
                "Dirty air filter",
                "Refrigerant leak",
                "Oversized unit",
                "Thermostat problems",
                "Electrical issues"
            ],
            "actions": [
                "Replace air filter",
                "Check thermostat location and settings",
                "Ensure proper clearance around outdoor unit",
                "Monitor cycle times (should run 15+ minutes)",
                "Schedule professional diagnosis"
            ],
            "urgency": 3,
            "cost": "$75 - $500"
        }
    },
    
    EquipmentType.BOILER: {
        "no heat": {
            "causes": [
                "Pilot light out",
                "Low water pressure",
                "Pump failure",
                "Thermostat malfunction",
                "Gas supply issues",
                "Airlocked system"
            ],
            "actions": [
                "Check boiler pressure gauge (should be 1-2 bar)",
                "Relight pilot light if safe",
                "Check thermostat settings",
                "Bleed radiators to remove air",
                "Check gas supply",
                "Reset boiler using reset button"
            ],
            "urgency": 4,
            "cost": "$100 - $1200"
        },
        "water leaks": {
            "causes": [
                "Corroded pipes",
                "Faulty pressure relief valve",
                "Pump seal failure",
                "Boiler tank corrosion",
                "Loose connections"
            ],
            "actions": [
                "Turn off water supply to boiler",
                "Turn off electrical supply",
                "Place buckets to catch drips",
                "Call plumber immediately",
                "Check for gas leaks if near gas lines"
            ],
            "urgency": 5,
            "cost": "$200 - $5000+ depending on location"
        },
        "strange noises": {
            "causes": [
                "Limescale buildup (kettling)",
                "Pump bearing wear",
                "Air in system",
                "Loose components",
                "Water flow restrictions"
            ],
            "actions": [
                "Bleed radiators to remove air",
                "Check pump settings",
                "Schedule descaling service",
                "Tighten visible loose connections",
                "Monitor noise patterns and document"
            ],
            "urgency": 3,
            "cost": "$150 - $800"
        }
    },
    
    EquipmentType.WATER_HEATER: {
        "no hot water": {
            "causes": [
                "Pilot light out (gas)",
                "Tripped circuit breaker (electric)",
                "Faulty heating elements",
                "Thermostat failure",
                "Gas supply issues"
            ],
            "actions": [
                "Check circuit breaker and reset if needed",
                "Relight pilot light following instructions",
                "Check gas supply valve",
                "Test temperature settings",
                "Wait 2-3 hours for recovery after repairs"
            ],
            "urgency": 3,
            "cost": "$100 - $600"
        },
        "water not hot enough": {
            "causes": [
                "Thermostat set too low",
                "Sediment buildup in tank",
                "Faulty heating element",
                "Undersized water heater",
                "Heat loss from uninsulated pipes"
            ],
            "actions": [
                "Increase thermostat setting to 120°F",
                "Insulate hot water pipes",
                "Flush tank to remove sediment",
                "Test heating elements with multimeter",
                "Consider tank replacement if over 10 years old"
            ],
            "urgency": 2,
            "cost": "$50 - $1200"
        },
        "water leaks": {
            "causes": [
                "Pressure relief valve discharge",
                "Tank corrosion",
                "Loose connections",
                "Faulty drain valve",
                "Internal tank failure"
            ],
            "actions": [
                "Turn off water supply immediately",
                "Turn off power/gas supply",
                "Drain tank if leaking from bottom",
                "Call plumber for assessment",
                "Check homeowner's insurance coverage"
            ],
            "urgency": 5,
            "cost": "$200 - $2500"
        }
    },
    
    EquipmentType.THERMOSTAT: {
        "not responding": {
            "causes": [
                "Dead batteries",
                "Loose wiring connections",
                "Blown fuse",
                "WiFi connectivity issues",
                "Software glitch"
            ],
            "actions": [
                "Replace batteries with fresh ones",
                "Check wiring connections are tight",
                "Reset thermostat to factory settings",
                "Check WiFi connection for smart thermostats",
                "Update firmware if available"
            ],
            "urgency": 2,
            "cost": "$10 - $200"
        },
        "wrong temperature readings": {
            "causes": [
                "Poor thermostat location",
                "Dirty sensors",
                "Calibration drift",
                "Heat sources nearby",
                "Drafts affecting sensor"
            ],
            "actions": [
                "Clean thermostat with soft brush",
                "Check for heat sources nearby (lamps, electronics)",
                "Recalibrate if option available",
                "Consider relocating thermostat",
                "Compare with separate thermometer"
            ],
            "urgency": 2,
            "cost": "$20 - $300"
        }
    }
}

# Extended symptoms list for all equipment types
EXTENDED_SYMPTOMS = {
    EquipmentType.AIR_CONDITIONER: [
        "Not cooling", "Strange noises", "Ice formation", "Water leaking", 
        "High energy bills", "Frequent cycling", "Weak airflow", "Bad odors",
        "Unit won't turn on", "Blowing warm air"
    ],
    EquipmentType.FURNACE: [
        "Not heating", "Strange odors", "Pilot light out", "Loud noises",
        "Uneven heating", "Yellow flame", "Frequent cycling", "High gas bills",
        "Cold air blowing", "Thermostat not working"
    ],
    EquipmentType.HEAT_PUMP: [
        "Not heating in winter", "Not cooling in summer", "Ice on outdoor unit",
        "Strange noises", "High energy costs", "Short cycling", "Auxiliary heat running constantly",
        "Unit won't switch modes"
    ],
    EquipmentType.BOILER: [
        "No heat", "Radiators not warming", "Water leaks", "Strange noises",
        "Low water pressure", "Pilot light issues", "High gas bills",
        "Uneven heating", "Pump not working"
    ],
    EquipmentType.WATER_HEATER: [
        "No hot water", "Water not hot enough", "Water too hot", "Water leaks",
        "Strange noises", "Rusty water", "Bad smell", "Running out quickly",
        "Pilot light out"
    ],
    EquipmentType.THERMOSTAT: [
        "Not responding", "Wrong temperature readings", "Display blank",
        "Won't hold settings", "WiFi connectivity issues", "Short cycling system",
        "Dead batteries", "Wiring issues"
    ],
    EquipmentType.DUCTWORK: [
        "Poor airflow", "Noisy operation", "Uneven temperatures", "High energy bills",
        "Dust problems", "Visible damage", "Disconnected sections", "Insulation problems"
    ]
}


@router.get("/", response_model=List[Equipment])
async def get_all_equipment():
    """Get a list of all equipment."""
    return equipment_db


@router.get("/{equipment_id}", response_model=Equipment)
async def get_equipment(equipment_id: int):
    """Get specific equipment by ID."""
    for equipment in equipment_db:
        if equipment.id == equipment_id:
            return equipment
    
    raise HTTPException(status_code=404, detail="Equipment not found")


@router.post("/", response_model=Equipment)
async def create_equipment(equipment_data: EquipmentCreate):
    """Create new equipment."""
    # Generate new ID
    new_id = max([eq.id for eq in equipment_db if eq.id], default=0) + 1
    
    # Create new equipment
    new_equipment = Equipment(
        id=new_id,
        **equipment_data.dict()
    )
    
    equipment_db.append(new_equipment)
    return new_equipment


@router.get("/types/{equipment_type}/symptoms")
async def get_symptoms_for_equipment_type(equipment_type: EquipmentType):
    """Get comprehensive symptoms for a specific equipment type."""
    symptoms = EXTENDED_SYMPTOMS.get(equipment_type, [])
    return {
        "equipment_type": equipment_type,
        "symptoms": symptoms,
        "count": len(symptoms)
    }


@router.post("/diagnose", response_model=DiagnosticResult)
async def diagnose_equipment(diagnostic_request: DiagnosticRequest):
    """
    Perform comprehensive diagnosis based on equipment type and symptoms.
    Now includes detailed analysis for all major HVAC equipment types.
    """
    equipment_type = diagnostic_request.equipment_type
    symptoms = [s.lower().strip() for s in diagnostic_request.symptoms]
    
    # Get diagnostic database for this equipment type
    equipment_diagnostics = COMPREHENSIVE_DIAGNOSTICS.get(equipment_type, {})
    
    # Collect all possible causes and actions
    all_causes = []
    all_actions = []
    max_urgency = 1
    cost_estimates = []
    
    # Analyze each symptom
    matched_symptoms = []
    for symptom in symptoms:
        for diagnostic_key, diagnostic_data in equipment_diagnostics.items():
            if diagnostic_key in symptom or any(word in symptom for word in diagnostic_key.split()):
                matched_symptoms.append(diagnostic_key)
                all_causes.extend(diagnostic_data["causes"])
                all_actions.extend(diagnostic_data["actions"])
                max_urgency = max(max_urgency, diagnostic_data["urgency"])
                cost_estimates.append(diagnostic_data["cost"])
    
    # Remove duplicates while preserving order
    unique_causes = []
    unique_actions = []
    
    for cause in all_causes:
        if cause not in unique_causes:
            unique_causes.append(cause)
    
    for action in all_actions:
        if action not in unique_actions:
            unique_actions.append(action)
    
    # Determine cost estimate
    if cost_estimates:
        estimated_cost = cost_estimates[0]  # Use first match
        if len(cost_estimates) > 1:
            estimated_cost += " (multiple issues possible)"
    else:
        estimated_cost = "Contact professional for estimate"
    
    # If no specific symptoms matched, provide general advice
    if not unique_causes:
        unique_causes = [
            "General maintenance may be needed",
            "System requires professional inspection",
            "Age-related wear and tear"
        ]
        unique_actions = [
            "Schedule routine maintenance",
            "Contact qualified HVAC professional",
            "Review equipment age and warranty status"
        ]
        max_urgency = 2
        estimated_cost = "$100 - $300 for inspection"
    
    # Add general safety advice for high urgency items
    if max_urgency >= 4:
        unique_actions.insert(0, "⚠️ SAFETY: If you smell gas or suspect danger, evacuate and call emergency services")
    
    return DiagnosticResult(
        equipment_type=equipment_type,
        symptoms=diagnostic_request.symptoms,
        possible_causes=unique_causes[:8],  # Limit to top 8 causes
        recommended_actions=unique_actions[:10],  # Limit to top 10 actions
        urgency=max_urgency,
        estimated_cost=estimated_cost
    )


@router.get("/stats/summary")
async def get_equipment_summary():
    """Get summary statistics of all equipment."""
    total_equipment = len(equipment_db)
    
    # Count by type
    type_counts = {}
    status_counts = {}
    
    for equipment in equipment_db:
        # Count by type
        type_name = equipment.equipment_type.value
        type_counts[type_name] = type_counts.get(type_name, 0) + 1
        
        # Count by status
        status_name = equipment.status.value
        status_counts[status_name] = status_counts.get(status_name, 0) + 1
    
    return {
        "total_equipment": total_equipment,
        "by_type": type_counts,
        "by_status": status_counts,
        "diagnostic_coverage": {
            equipment_type.value: len(EXTENDED_SYMPTOMS.get(equipment_type, []))
            for equipment_type in EquipmentType
        }
    }


@router.get("/diagnostics/capabilities")
async def get_diagnostic_capabilities():
    """Get information about diagnostic capabilities for each equipment type."""
    capabilities = {}
    
    for equipment_type in EquipmentType:
        equipment_diags = COMPREHENSIVE_DIAGNOSTICS.get(equipment_type, {})
        symptoms = EXTENDED_SYMPTOMS.get(equipment_type, [])
        
        capabilities[equipment_type.value] = {
            "supported_symptoms": len(symptoms),
            "diagnostic_scenarios": len(equipment_diags),
            "symptoms_list": symptoms,
            "diagnostic_scenarios_list": list(equipment_diags.keys())
        }
    
    return {
        "total_equipment_types": len(EquipmentType),
        "capabilities": capabilities,
        "system_features": [
            "Multi-symptom analysis",
            "Urgency prioritization", 
            "Cost estimation",
            "Safety warnings",
            "Professional recommendations"
        ]
    }