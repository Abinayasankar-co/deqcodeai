import os
from typing import List, Optional, Dict, Any

from fastapi import FastAPI, HTTPException, Depends, Request
from pydantic import BaseModel, Field, EmailStr
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI(title="Enterprise Backend API")

# -------------------------------
# MongoDB configuration and client
# -------------------------------
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_DETAILS)
db = client["enterprise_db"]

# -------------------------------
# Helper class for ObjectId conversion in Pydantic
# -------------------------------
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema: dict):
        field_schema.update(type="string")

# -------------------------------
# Pydantic models for our enterprise data
# -------------------------------

class Owner(BaseModel):
    user_id: str
    email: EmailStr
    role: str = "admin"  # owner is admin by default
    free_credits: int = 100  # default free credits

class TeamMember(BaseModel):
    # user_id may be None until the invitation is accepted.
    user_id: Optional[str] = None
    email: EmailStr
    role: str = "entry"  # possible roles: entry, usable, admin
    invitation_status: str = "pending"  # invitation states: pending, accepted, rejected

class Circuit(BaseModel):
    name: str
    description: Optional[str] = None
    circuit_data: Dict[str, Any]  # contains details of the circuit

class EnterpriseCreate(BaseModel):
    name: str
    owner: Owner

class EnterpriseDB(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    owner: Owner
    team: List[TeamMember] = []
    circuits: List[Circuit] = []
    billing: Dict[str, Any] = {}  # billing details, e.g., {"usage": 0, "free_credits": 100}

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}


# -------------------------------
# Dependency: Simulated current user from headers
# In production, this should be replaced by proper authentication.
# -------------------------------
async def get_current_user(request: Request):
    user_id = request.headers.get("X-User-Id")
    user_role = request.headers.get("X-User-Role", "entry")
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    return {"user_id": user_id, "role": user_role}


# -------------------------------
# Endpoint: Create a new Enterprise with an owner
# -------------------------------
@app.post("/enterprises", response_model=EnterpriseDB)
async def create_enterprise(enterprise: EnterpriseCreate):
    enterprise_data = enterprise.dict()
    # Initialize lists and billing details.
    enterprise_data["team"] = []  
    enterprise_data["circuits"] = []
    enterprise_data["billing"] = {
        "usage": 0,
        "free_credits": enterprise_data["owner"]["free_credits"]
    }
    result = await db["enterprises"].insert_one(enterprise_data)
    created_enterprise = await db["enterprises"].find_one({"_id": result.inserted_id})
    return EnterpriseDB(**created_enterprise)


# -------------------------------
# Endpoint: Invite a new team member (invitation based)
# Only the owner or an admin team member can invite.
# -------------------------------
@app.post("/enterprises/{enterprise_id}/invite", response_model=TeamMember)
async def invite_member(
    enterprise_id: str,
    member: TeamMember,
    current_user: dict = Depends(get_current_user)
):
    # Retrieve enterprise document
    enterprise = await db["enterprises"].find_one({"_id": ObjectId(enterprise_id)})
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")

    # Authorization check: only owner or team member with admin role can invite.
    allowed = False
    if enterprise["owner"]["user_id"] == current_user["user_id"]:
        allowed = True
    else:
        for team_member in enterprise.get("team", []):
            if (
                team_member.get("user_id") == current_user["user_id"]
                and team_member.get("role") == "admin"
            ):
                allowed = True
                break

    if not allowed:
        raise HTTPException(status_code=403, detail="Not authorized to invite team members")

    # Ensure the member is not already invited.
    if any(tm["email"] == member.email for tm in enterprise.get("team", [])):
        raise HTTPException(status_code=400, detail="Member already invited")

    member_data = member.dict()
    update_res = await db["enterprises"].update_one(
        {"_id": ObjectId(enterprise_id)},
        {"$push": {"team": member_data}}
    )
    if update_res.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to add member")
    return member


# -------------------------------
# Endpoint: Accept an invitation
# Here the invited user can accept (adding their user_id) by providing their email.
# -------------------------------
@app.post("/enterprises/{enterprise_id}/accept-invite")
async def accept_invite(
    enterprise_id: str,
    email: EmailStr,
    current_user: dict = Depends(get_current_user)
):
    result = await db["enterprises"].update_one(
        {"_id": ObjectId(enterprise_id), "team.email": email},
        {"$set": {"team.$.invitation_status": "accepted", "team.$.user_id": current_user["user_id"]}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Invitation not found")
    return {"message": "Invitation accepted."}


# -------------------------------
# Endpoint: Add a circuit which will be shared within the team.
# Only an accepted member or the owner is permitted.
# -------------------------------
@app.post("/enterprises/{enterprise_id}/circuits", response_model=Circuit)
async def add_circuit(
    enterprise_id: str,
    circuit: Circuit,
    current_user: dict = Depends(get_current_user)
):
    enterprise = await db["enterprises"].find_one({"_id": ObjectId(enterprise_id)})
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")

    # Permission: must be the owner or a team member with accepted invitation.
    permitted = False
    if enterprise["owner"]["user_id"] == current_user["user_id"]:
        permitted = True
    else:
        for member in enterprise.get("team", []):
            if (
                member.get("user_id") == current_user["user_id"]
                and member.get("invitation_status") == "accepted"
            ):
                permitted = True
                break

    if not permitted:
        raise HTTPException(status_code=403, detail="User not a member of the enterprise")

    circuit_data = circuit.dict()
    update_res = await db["enterprises"].update_one(
        {"_id": ObjectId(enterprise_id)},
        {"$push": {"circuits": circuit_data}}
    )
    if update_res.modified_count == 0:
        raise HTTPException(status_code=500, detail="Failed to add circuit")
    return circuit


# -------------------------------
# Endpoint: Billing analytics view (admin only)
# The dashboard (whagonwheel analytics) is available only to admins.
# -------------------------------
@app.get("/enterprises/{enterprise_id}/billing")
async def billing_analytics(
    enterprise_id: str, 
    current_user: dict = Depends(get_current_user)
):
    enterprise = await db["enterprises"].find_one({"_id": ObjectId(enterprise_id)})
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")

    allowed = False
    if enterprise["owner"]["user_id"] == current_user["user_id"]:
        allowed = True
    else:
        for member in enterprise.get("team", []):
            if member.get("user_id") == current_user["user_id"] and member.get("role") == "admin":
                allowed = True
                break

    if not allowed:
        raise HTTPException(status_code=403, detail="Access restricted to administrators only")

    return {"billing": enterprise.get("billing", {})}


# -------------------------------
# Endpoint: Update billing usage
# For simulation purposes, allows an admin to update billing usage.
# -------------------------------
@app.post("/enterprises/{enterprise_id}/billing/update")
async def update_billing(
    enterprise_id: str,
    usage: int,
    current_user: dict = Depends(get_current_user)
):
    enterprise = await db["enterprises"].find_one({"_id": ObjectId(enterprise_id)})
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")

    allowed = False
    if enterprise["owner"]["user_id"] == current_user["user_id"]:
        allowed = True
    else:
        for member in enterprise.get("team", []):
            if member.get("user_id") == current_user["user_id"] and member.get("role") == "admin":
                allowed = True
                break

    if not allowed:
        raise HTTPException(status_code=403, detail="Access restricted to administrators only")

    new_usage = enterprise.get("billing", {}).get("usage", 0) + usage
    await db["enterprises"].update_one(
        {"_id": ObjectId(enterprise_id)},
        {"$set": {"billing.usage": new_usage}}
    )
    return {"message": "Billing updated", "new_usage": new_usage}


# -------------------------------
# Additional Endpoint: List team members
# All authenticated members within the enterprise can view the team list.
# -------------------------------
@app.get("/enterprises/{enterprise_id}/members")
async def list_members(
    enterprise_id: str,
    current_user: dict = Depends(get_current_user)
):
    enterprise = await db["enterprises"].find_one({"_id": ObjectId(enterprise_id)})
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")

    return {"team": enterprise.get("team", [])}


# -------------------------------
# Additional Endpoint: Apply for free credits
# Only the enterprise owner can apply for free credits.
# -------------------------------
@app.post("/enterprises/{enterprise_id}/apply-free-credits")
async def apply_free_credits(
    enterprise_id: str,
    credits: int,
    current_user: dict = Depends(get_current_user)
):
    enterprise = await db["enterprises"].find_one({"_id": ObjectId(enterprise_id)})
    if not enterprise:
        raise HTTPException(status_code=404, detail="Enterprise not found")
    if enterprise["owner"]["user_id"] != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Only the owner can apply for free credits.")

    free_credits = enterprise.get("billing", {}).get("free_credits", 0) + credits
    await db["enterprises"].update_one(
        {"_id": ObjectId(enterprise_id)},
        {"$set": {"billing.free_credits": free_credits}}
    )
    return {"message": "Free credits updated", "free_credits": free_credits}
