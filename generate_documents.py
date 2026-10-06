"""
generate_documents.py
Generates 75 comprehensive, realistic markdown documents for Apex Car Rental RAG corpus.
Categories:
1. Fleet Specifications (15 docs)
2. Insurance & Protection Plans (10 docs)
3. Pricing, Surcharges & Payment Policies (10 docs)
4. Rental Eligibility & Reservation Rules (10 docs)
5. Vehicle Pickup, Return & Inspection (10 docs)
6. Emergency Procedures & Roadside Assistance (10 docs)
7. Airport & Downtown Location Guides (10 docs)
"""

import os
from pathlib import Path

DOCS_DIR = Path(__file__).resolve().parent / "data" / "documents"
DOCS_DIR.mkdir(parents=True, exist_ok=True)

documents = [
    # --- 1. FLEET (15 docs) ---
    {
        "filename": "fleet_01_economy_sedan.md",
        "title": "Economy Sedan - Toyota Corolla & Honda Civic",
        "category": "Fleet",
        "content": """# Vehicle Profile: Economy Sedan (Toyota Corolla / Honda Civic)

## Overview & Fleet Class
- **Class Code:** ECAR
- **Sample Models:** Toyota Corolla LE (2024), Honda Civic LX (2024), Nissan Sentra SV.
- **Daily Base Rate:** $45.00 / day
- **Weekly Discounted Rate:** $270.00 / week (7 days for price of 6)

## Specifications & Capacity
- **Seating:** 5 Adults (best for 4 adults comfortably)
- **Luggage Capacity:** 2 Large Suitcases (28") + 2 Small Carry-ons (21")
- **Fuel Economy:** 32 MPG City / 41 MPG Highway (Combined 36 MPG)
- **Transmission:** Continuously Variable Transmission (CVT) Automatic
- **Drivetrain:** Front-Wheel Drive (FWD)

## Included Standard Amenities
- Apple CarPlay and Android Auto wireless connectivity
- Integrated Backup Camera with dynamic guidelines
- Forward Collision Warning & Lane Departure Assist
- Full Bluetooth hands-free phone & audio streaming
- 12V DC power outlet & 2x USB-C fast charging ports

## Mileage & Fuel Requirements
- **Mileage Allowance:** Unlimited mileage within the continental United States and Canada.
- **Required Fuel Type:** Regular Unleaded (87 Octane). Full-to-Full policy applies.
"""
    },
    {
        "filename": "fleet_02_compact_sedan.md",
        "title": "Compact Sedan - Hyundai Elantra & Kia Forte",
        "category": "Fleet",
        "content": """# Vehicle Profile: Compact Sedan (Hyundai Elantra / Kia Forte)

## Overview & Fleet Class
- **Class Code:** CCAR
- **Sample Models:** Hyundai Elantra SEL (2024), Kia Forte GT-Line (2024).
- **Daily Base Rate:** $48.00 / day
- **Weekly Rate:** $288.00 / week

## Specifications & Performance
- **Seating:** 5 Passengers
- **Luggage:** 2 Checked Suitcases + 1 Duffel Bag
- **Fuel Economy:** 31 MPG City / 40 MPG Highway
- **Transmission:** Intelligent Variable Transmission (IVT) Automatic
- **Safety Rating:** 5-Star NHTSA Overall Safety Rating

## Features
- 8-inch high-resolution touchscreen display
- Adaptive Cruise Control with Stop & Go
- Blind Spot Collision Avoidance Assist
- Rear cross-traffic collision alert
- Heated front side mirrors for winter visibility
"""
    },
    {
        "filename": "fleet_03_midsize_sedan.md",
        "title": "Midsize Sedan - Toyota Camry & Hyundai Sonata",
        "category": "Fleet",
        "content": """# Vehicle Profile: Midsize Sedan (Toyota Camry / Hyundai Sonata)

## Overview & Fleet Class
- **Class Code:** ICAR
- **Sample Models:** Toyota Camry SE (2024), Hyundai Sonata SEL (2024), Nissan Altima.
- **Daily Base Rate:** $56.00 / day
- **Weekly Rate:** $336.00 / week

## Specifications & Capacity
- **Seating:** 5 Adults with expansive rear passenger legroom (38 inches)
- **Trunk Space:** 15.1 cu ft (fits 3 large suitcases + 2 carry-on bags)
- **Engine:** 2.5L 4-Cylinder (203 Horsepower)
- **Fuel Economy:** 28 MPG City / 39 MPG Highway
- **Fuel:** Regular Unleaded (87 Octane)

## Premium Comfort Highlights
- Dual-zone automatic climate control with rear-seat vents
- 8-way power adjustable driver's seat with power lumbar support
- Qi Wireless Smartphone Charging Pad
- Smart Key System with Push Button Start
"""
    },
    {
        "filename": "fleet_04_fullsize_sedan.md",
        "title": "Full-Size Sedan - Chevrolet Malibu & Dodge Charger",
        "category": "Fleet",
        "content": """# Vehicle Profile: Full-Size Sedan (Chevrolet Malibu / Dodge Charger)

## Overview & Fleet Class
- **Class Code:** FCAR
- **Sample Models:** Chevrolet Malibu LT (2024), Dodge Charger SXT (2023).
- **Daily Base Rate:** $65.00 / day
- **Weekly Rate:** $390.00 / week

## Specifications
- **Seating:** 5 Adults (spacious shoulder and hip room)
- **Cargo Capacity:** 15.7 cu ft (holds 3 full suitcases and golf bags)
- **Fuel Economy:** 27 MPG City / 35 MPG Highway
- **Drivetrain:** Rear-Wheel Drive (Charger) / Front-Wheel Drive (Malibu)

## Included Features
- Remote vehicle start via key fob
- Acoustic laminated windshield for silent highway cruising
- 10-speaker premium audio system
- Built-in OnStar 4G LTE Wi-Fi hotspot capability
"""
    },
    {
        "filename": "fleet_05_compact_suv.md",
        "title": "Compact SUV - Toyota RAV4 & Honda CR-V",
        "category": "Fleet",
        "content": """# Vehicle Profile: Compact SUV (Toyota RAV4 / Honda CR-V)

## Overview & Fleet Class
- **Class Code:** IFAR
- **Sample Models:** Toyota RAV4 XLE AWD (2024), Honda CR-V EX AWD (2024).
- **Daily Base Rate:** $72.00 / day
- **Weekly Rate:** $432.00 / week

## Specifications & Practicality
- **Seating:** 5 Adults with upright commanding seating position
- **Ground Clearance:** 8.4 inches (ideal for light gravel and winter snow)
- **Cargo Space:** 37.6 cu ft behind rear seats; 69.8 cu ft with seats folded flat
- **Suitcase Capacity:** 4 Large Suitcases + 2 Backpacks
- **Drivetrain:** All-Wheel Drive (AWD) with Snow/Mud Terrain Modes
- **Fuel Economy:** 27 MPG City / 33 MPG Highway

## Amenities & Extras
- Power rear liftgate with height adjustment
- Roof rails installed (compatible with ski racks and kayak holders)
- All-weather rubber floor mats front and rear
"""
    },
    {
        "filename": "fleet_06_midsize_family_suv.md",
        "title": "Midsize 7-Passenger SUV - Ford Explorer & Highlander",
        "category": "Fleet",
        "content": """# Vehicle Profile: Midsize 7-Passenger SUV (Ford Explorer / Toyota Highlander)

## Overview & Fleet Class
- **Class Code:** SFAR / FRAR
- **Sample Models:** Ford Explorer XLT (2024), Toyota Highlander LE (2024).
- **Daily Base Rate:** $85.00 / day
- **Weekly Rate:** $510.00 / week

## Capacity & Dimensions
- **Seating:** 7 Passengers (2-3-2 configuration with easy 3rd-row slide access)
- **Luggage:** 3 Large Bags with 3rd row upright; 6 Large Bags with 3rd row folded
- **Towing Capability:** Class III Hitch capable up to 5,000 lbs (towing requires prior authorization)
- **Drivetrain:** Intelligent 4WD / AWD with Terrain Management System
- **Fuel Economy:** 21 MPG City / 28 MPG Highway

## Family Convenience Package
- Tri-zone independent rear climate controls
- 5 USB ports across all three rows
- Integrated rear door sunshades
- Automatic emergency rear braking with pedestrian detection
"""
    },
    {
        "filename": "fleet_07_fullsize_suv.md",
        "title": "Full-Size SUV - Chevrolet Tahoe & Ford Expedition",
        "category": "Fleet",
        "content": """# Vehicle Profile: Full-Size SUV (Chevrolet Tahoe / Ford Expedition)

## Overview & Fleet Class
- **Class Code:** FFAR
- **Sample Models:** Chevrolet Tahoe LT 4WD (2024), Ford Expedition XLT Max (2024).
- **Daily Base Rate:** $115.00 / day
- **Weekly Rate:** $690.00 / week

## Specs & Extreme Capability
- **Seating:** 8 Passengers (2-3-3 seating layout)
- **Engine:** 5.3L EcoTec3 V8 (355 HP) or 3.5L EcoBoost Twin Turbo
- **Cargo Capacity:** 25.5 cu ft behind row 3; up to 122.9 cu ft maximum cargo volume
- **Luggage:** 5 Checked Suitcases + 4 Carry-ons comfortably
- **Fuel Economy:** 15 MPG City / 20 MPG Highway (28-gallon fuel tank)

## Standard Luxury & Towing
- 10.2-inch infotainment screen with Google built-in
- Heated front and second-row leather seats
- 360-degree HD Surround Vision camera system
- Power-folding 3rd-row seats
"""
    },
    {
        "filename": "fleet_08_ev_standard.md",
        "title": "Electric Vehicle Standard - Tesla Model 3 RWD",
        "category": "Fleet",
        "content": """# Vehicle Profile: Electric Vehicle Standard (Tesla Model 3 RWD)

## Overview & Fleet Class
- **Class Code:** ECAR-EV
- **Model:** Tesla Model 3 Rear-Wheel Drive (2024 Refresh)
- **Daily Base Rate:** $75.00 / day
- **Weekly Rate:** $450.00 / week

## Battery, Range & Charging
- **EPA Estimated Range:** 272 Miles on 100% Charge
- **Acceleration:** 0-60 mph in 5.8 seconds
- **Charging Protocol:** Tesla NACS port. Supercharger billing is auto-billed to your rental card at wholesale cost with zero markup.
- **Apex EV Battery Guarantee:** Picked up with at least 80% state of charge. Must be returned with at least 70% state of charge (or purchase $25 EV Pre-paid Return recharge option).
- **Included Cables:** Mobile Connector Kit with 110V household adapter and J1772 Level 2 adapter in frunk.

## Interior & Tech
- 15.4-inch central touchscreen interface
- Premium 9-speaker audio system
- Front trunk (Frunk) + Rear deep sub-trunk storage
- Luggage Capacity: 3 Large Bags + 1 Duffel
"""
    },
    {
        "filename": "fleet_09_ev_suv_long_range.md",
        "title": "Electric SUV Long Range - Tesla Model Y & Mustang Mach-E",
        "category": "Fleet",
        "content": """# Vehicle Profile: Electric SUV Long Range (Tesla Model Y / Ford Mach-E)

## Overview & Fleet Class
- **Class Code:** IFAR-EV
- **Models:** Tesla Model Y Long Range AWD (2024), Ford Mustang Mach-E Extended Range AWD (2024).
- **Daily Base Rate:** $92.00 / day
- **Weekly Rate:** $552.00 / week

## Performance & Range
- **EPA Range:** 310 Miles (Model Y) / 300 Miles (Mach-E)
- **Drivetrain:** Dual Motor All-Wheel Drive
- **Seating:** 5 Adults comfortably
- **Cargo Space:** 76 cu ft total cargo volume
- **Luggage:** 4 Large Suitcases + 2 Backpacks

## Unique Perks
- Glass panoramic acoustic roof
- Sentry Mode & Dashcam security included
- Level 2 home charging cable kit included
- Access to Tesla Supercharging Network and Electrify America fast chargers
"""
    },
    {
        "filename": "fleet_10_luxury_sedan.md",
        "title": "Luxury Sedan - BMW 5 Series & Audi A6",
        "category": "Fleet",
        "content": """# Vehicle Profile: Luxury Sedan (BMW 5 Series / Audi A6)

## Overview & Fleet Class
- **Class Code:** LCAR
- **Sample Models:** BMW 530i xDrive (2024), Audi A6 45 TFSI Quattro (2024).
- **Daily Base Rate:** $125.00 / day
- **Weekly Rate:** $750.00 / week

## Engine & Luxury Specs
- **Engine:** 2.0L Turbocharged inline-4 (255 HP)
- **Drivetrain:** Intelligent All-Wheel Drive (xDrive / Quattro)
- **Seating:** 5 Executive passengers
- **Luggage:** 3 Checked Suitcases (18.7 cu ft trunk)
- **Mileage Terms:** 250 miles/day included. Additional miles billed at $0.35/mile.

## Exclusive Amenities
- Vernasca perforated genuine leather upholstery
- Harman Kardon 16-speaker 464W Surround Sound System
- Head-Up Display (HUD) projected onto windshield
- Multi-contour 16-way massage seats
- Required Fuel: 91+ Octane Premium Gasoline
"""
    },
    {
        "filename": "fleet_11_luxury_suv.md",
        "title": "Luxury SUV - BMW X5 & Mercedes-Benz GLE",
        "category": "Fleet",
        "content": """# Vehicle Profile: Luxury SUV (BMW X5 / Mercedes-Benz GLE 350)

## Overview & Fleet Class
- **Class Code:** LFAR
- **Sample Models:** BMW X5 xDrive40i (2024), Mercedes-Benz GLE 350 4MATIC (2024).
- **Daily Base Rate:** $145.00 / day
- **Weekly Rate:** $870.00 / week

## Luxury Performance
- **Engine:** 3.0L Turbocharged Inline-6 with 48V Mild Hybrid (375 HP)
- **Seating:** 5 Adults (spacious executive cabin)
- **Cargo:** 33.9 cu ft behind row 2; fits 4 large Samsonite bags + golf equipment
- **Towing:** Up to 7,200 lbs rated capability

## Cabin Features
- Panoramic sky lounge glass roof with LED ambient accents
- Burmester / Harman Kardon high-fidelity audio system
- Active air suspension with automatic level control
- Premium 91+ Octane required
"""
    },
    {
        "filename": "fleet_12_convertible.md",
        "title": "Convertible Sports Car - Ford Mustang GT & Chevy Camaro",
        "category": "Fleet",
        "content": """# Vehicle Profile: Convertible Sports Car (Ford Mustang GT / Chevy Camaro)

## Overview & Fleet Class
- **Class Code:** STAR
- **Sample Models:** Ford Mustang GT Premium Convertible (2024), Chevy Camaro SS (2023).
- **Daily Base Rate:** $95.00 / day
- **Weekly Rate:** $570.00 / week

## Specs & Driving Thrills
- **Engine:** 5.0L Ti-VCT V8 (480 HP)
- **Roof:** Fully motorized power-retractable soft top (opens in 7 seconds)
- **Seating:** 4 Passengers (2 front adults + 2 small rear passengers)
- **Luggage:** 1 Large Suitcase + 2 Soft Weekend Duffel Bags (11.4 cu ft)
- **Exhaust:** Active valve performance exhaust with Quiet/Sport/Track modes
"""
    },
    {
        "filename": "fleet_13_minivan_family.md",
        "title": "Family Minivan - Chrysler Pacifica & Honda Odyssey",
        "category": "Fleet",
        "content": """# Vehicle Profile: Family Minivan (Chrysler Pacifica / Honda Odyssey)

## Overview & Fleet Class
- **Class Code:** MVAR
- **Sample Models:** Chrysler Pacifica Touring L (2024), Honda Odyssey EX-L (2024).
- **Daily Base Rate:** $79.00 / day
- **Weekly Rate:** $474.00 / week

## Ultimate Family Practicality
- **Seating:** 7 or 8 Passengers with Stow 'n Go fold-in-floor seating
- **Luggage Capacity:** 5 Large Suitcases + Stroller + 4 Carry-ons
- **Access:** Dual power sliding rear doors + hands-free power tailgate
- **Rear Entertainment:** Dual 10.1-inch seatback touchscreens with HDMI inputs
- **Fuel Economy:** 19 MPG City / 28 MPG Highway (Regular 87 Fuel)
"""
    },
    {
        "filename": "fleet_14_passenger_van_12_seat.md",
        "title": "12-Passenger Van - Ford Transit 350 Passenger",
        "category": "Fleet",
        "content": """# Vehicle Profile: 12-Passenger Van (Ford Transit 350)

## Overview & Fleet Class
- **Class Code:** FVAR
- **Model:** Ford Transit 350 XLT Passenger Van (Medium Roof)
- **Daily Base Rate:** $139.00 / day
- **Weekly Rate:** $834.00 / week

## Group Capacity
- **Seating:** 12 Adults (2-3-3-4 configuration)
- **Roof Height:** Medium Roof (standing height 5'11" inside cabin)
- **Luggage Space:** Dedicated rear cargo bay holds 8-10 suitcases
- **Engine:** 3.5L EcoBoost V6 (310 HP)

## Driver Requirements for 12-Passenger Vans
- Driver must be at least 25 years old.
- Standard valid Class D driver's license (no Commercial Driver's License CDL needed for non-commercial personal use).
- Proof of full collision insurance coverage required at vehicle hand-off.
"""
    },
    {
        "filename": "fleet_15_pickup_truck_4x4.md",
        "title": "Full-Size 4x4 Pickup Truck - Ford F-150 & Chevy Silverado",
        "category": "Fleet",
        "content": """# Vehicle Profile: Full-Size 4x4 Pickup Truck (Ford F-150 / Silverado 1500)

## Overview & Fleet Class
- **Class Code:** SPAR
- **Sample Models:** Ford F-150 SuperCrew XLT 4x4 (2024), Chevrolet Silverado 1500 LT 4WD (2024).
- **Daily Base Rate:** $89.00 / day
- **Weekly Rate:** $534.00 / week

## Capability & Bed Dimensions
- **Cab Style:** Crew Cab (5 full adult seats with huge rear floor storage)
- **Bed Length:** 5.5 ft / 6.5 ft bed with spray-in bedliner and tie-down cleats
- **Drivetrain:** Shift-on-the-fly 4-Wheel Drive with Low Range
- **Payload Capacity:** 1,950 lbs
- **Towing Limit:** 7,500 lbs (requires optional towing package add-on for $15/day)
"""
    },

    # --- 2. INSURANCE & PROTECTION (10 docs) ---
    {
        "filename": "insurance_01_standard_included.md",
        "title": "Standard Protection Plan (Included Basic Coverage)",
        "category": "Insurance",
        "content": """# Apex Standard Protection Plan (Included by Default)

## Summary & Cost
- **Daily Cost:** $0.00 / day (included with every valid Apex rental contract)
- **Deductible:** $1,500.00 USD per incident

## What Is Covered
1. **Third-Party Bodily Injury & Property Damage:** Meets statutory minimum financial responsibility limits required by state law.
2. **Vehicle Damage:** Covers damage to the Apex rental vehicle exceeding the $1,500 deductible, provided the renter has complied with all terms of the rental agreement.

## Exclusions & Limitations
- Renter is personally liable for the initial $1,500 deductible out-of-pocket before insurance applies.
- Does NOT cover glass chips, windshield cracks, side window breakage, tire punctures, rim scuffs, or lost car keys.
- Does NOT provide roadside assistance (towing, jumpstarts, lockouts are billed separately at standard service rates).
- Voided if vehicle is operated off-road, driven while impaired, or piloted by an unauthorized driver.
"""
    },
    {
        "filename": "insurance_02_silver_protection.md",
        "title": "Silver Protection Plan (Reduced Deductible & Glass/Tires)",
        "category": "Insurance",
        "content": """# Apex Silver Protection Plan

## Pricing & Deductible
- **Daily Cost:** $18.00 / day
- **Collision Deductible:** Reduced to $300.00 USD (down from $1,500)

## Comprehensive Added Coverages
- **Glass & Windshield Waiver:** 100% coverage for stone chips, cracks, and complete windshield replacements with $0 glass deductible.
- **Tire & Rim Protection:** Full repair or replacement reimbursement for punctures, sidewall tears, and curb rash up to $600 per tire.
- **Side Mirror Coverage:** Covers exterior driver and passenger mirrors damaged by passing traffic or tight parking spots.
- **Exterior Body Dent Waiver:** Scratches and minor dings under 3 inches are automatically forgiven without charge upon return.

## Recommended For
Travelers planning highway road trips, gravel or national park travel, and city drivers navigating tight parking garages.
"""
    },
    {
        "filename": "insurance_03_gold_platinum_zero_deductible.md",
        "title": "Gold Platinum Protection Plan (Zero Deductible & Total Peace of Mind)",
        "category": "Insurance",
        "content": """# Apex Gold Platinum Protection Plan (Comprehensive $0 Deductible)

## Pricing & Terms
- **Daily Cost:** $30.00 / day
- **Deductible:** $0.00 USD (Renter pays nothing for covered mechanical or body damage)

## Complete Protection Scope
1. **Zero Financial Liability:** Full waiver of all repair costs, loss-of-use fees, and administrative assessment charges in the event of an accident or total loss.
2. **Glass & Tire Full Waiver:** $0 deductible for windshield, roof glass, tires, and alloy wheels.
3. **24/7 Premium Roadside Assistance Included:** Free unlimited towing, battery jump-starts, flat tire changes using the vehicle spare, fuel delivery (up to 3 gallons free), and emergency lockout service.
4. **Lost Key Replacement Waiver:** Up to 1 replacement smart key fob (value up to $450) replaced with zero charge.
5. **Personal Effects Coverage (PEC):** Up to $1,500 coverage for theft of personal electronics and luggage from inside the locked vehicle (police report mandatory).
"""
    },
    {
        "filename": "insurance_04_cdw_collision_damage_waiver.md",
        "title": "Collision Damage Waiver (CDW / LDW) Explained",
        "category": "Insurance",
        "content": """# Collision Damage Waiver (CDW) & Loss Damage Waiver (LDW)

## Understanding CDW vs. Insurance
CDW is not technically an insurance policy; it is an express contractual waiver by Apex Car Rental releasing the renter from financial responsibility for loss or damage to the vehicle during the rental period.

## Pricing
- **CDW Standalone:** $22.00 / day
- **Deductible:** $0 out-of-pocket responsibility for vehicle repair or replacement.

## What CDW Covers
- Collision with another vehicle, animal, or stationary object (guardrail, post).
- Rollover accidents and single-car incidents.
- Theft or vandalism of the entire vehicle.
- Loss of Use fees: Covers revenue lost by Apex while the car is out of service in the body shop.

## How to Invalidate CDW
CDW becomes immediately void if:
- The driver was not registered on the rental agreement.
- The driver was under the influence of alcohol, drugs, or prescription narcotics.
- The vehicle was used for ridesharing (Uber, Lyft) or commercial delivery without an authorized commercial endorsement.
- The vehicle was driven across borders without written cross-border authorization.
"""
    },
    {
        "filename": "insurance_05_sli_supplemental_liability.md",
        "title": "Supplemental Liability Insurance (SLI / Third-Party Protection)",
        "category": "Insurance",
        "content": """# Supplemental Liability Insurance (SLI)

## Coverage Limits & Cost
- **Daily Premium:** $14.50 / day
- **Liability Limit:** Provides primary liability protection up to $1,000,000 USD combined single limit (CSL) per accident.

## Why SLI Is Vital
Standard state statutory minimums are frequently as low as $25,000 for bodily injury and $10,000 for property damage. In a serious multi-vehicle highway accident, claims quickly exceed these minimums, exposing the renter's personal savings, home equity, and wages. SLI shields the renter up to $1,000,000.

## International Renters
SLI is strongly recommended for international visitors whose overseas personal auto insurance policies do not cover third-party liability claims within the United States.
"""
    },
    {
        "filename": "insurance_06_personal_accident_effects_pai_pec.md",
        "title": "Personal Accident & Personal Effects Protection (PAI / PEC)",
        "category": "Insurance",
        "content": """# Personal Accident Insurance (PAI) & Personal Effects Coverage (PEC)

## Combined Package Pricing
- **Daily Cost:** $9.00 / day covers both driver and all authorized passengers.

## Personal Accident Insurance (PAI) Benefits
- **Accidental Death Benefit:** $175,000 for named primary driver; $17,500 per passenger.
- **Accidental Medical Expense Reimbursement:** Up to $3,500 per person for ambulance, emergency room, and hospital stays resulting directly from an accident while inside the vehicle.
- **Ambulance Service Benefit:** Up to $250 per person.

## Personal Effects Coverage (PEC)
- **Per Incident Limit:** $1,500 total aggregate ($500 per single item).
- **Covered Items:** Laptops, cameras, clothing, sports gear, and travel luggage stolen from a locked vehicle trunk or cabin.
- **Filing Requirement:** Renter must present a verified local police crime report within 48 hours of discovery.
"""
    },
    {
        "filename": "insurance_07_credit_card_rental_insurance_guide.md",
        "title": "Using Credit Card Rental Car Insurance at Apex",
        "category": "Insurance",
        "content": """# Credit Card Rental Car Collision Coverage Guidelines

## Primary vs. Secondary Credit Card Coverage
Many credit cards (such as Chase Sapphire Reserve, Capital One Venture X, Amex Premium Car Rental Protection) offer auto rental collision damage waivers:
- **Primary Coverage:** Pays first without notifying your personal auto insurance provider.
- **Secondary Coverage:** Requires you to file a claim with your domestic auto insurer first; the card pays only your deductible.

## Mandatory Steps to Activate Credit Card Coverage
1. **Decline Apex CDW/LDW:** You must explicitly decline the Apex Collision Damage Waiver at the counter.
2. **Pay Entire Rental with That Card:** The full reservation must be paid and authorized on the specific eligible credit card.
3. **Be the Primary Renter:** The cardholder's name must match the primary renter listed on the contract.

## Important Apex Policy Note
If you decline Apex CDW and rely on credit card coverage, you remain personally liable to Apex for damages up to the full market value of the vehicle until your credit card issuer processes and reimburses the claim. A temporary credit card security authorization of $500 is placed on the card at pickup (instead of $200).
"""
    },
    {
        "filename": "insurance_08_windshield_and_tire_standalone.md",
        "title": "Road Hazard Glass & Tire Protection (Standalone Option)",
        "category": "Insurance",
        "content": """# Standalone Road Hazard Glass & Tire Protection

## Overview & Pricing
- **Daily Rate:** $7.50 / day
- **Deductible:** $0

## What Is Covered
- **Windshields:** Repair of bullseye chips, star breaks, and cracks up to 6 inches, or full OEM replacement if unrepairable.
- **Tires:** Puncture repairs, plug services, and new tire replacement caused by roadway debris, nails, potholes, or jagged road surfaces.
- **Wheels:** Structural rim repair if bent by an unavoidable pothole on public roads.

## Exclusions
Does not cover tire wear caused by deliberate burnouts, off-road driving on unpaved trails, or curb damage caused by parallel parking errors.
"""
    },
    {
        "filename": "insurance_09_theft_and_vandalism_policy.md",
        "title": "Theft and Vandalism Policy",
        "category": "Insurance",
        "content": """# Vehicle Theft & Vandalism Policy

## Protocol When Theft Occurs
1. **Immediately Notify Police:** Call 911 or the local police department within 2 hours of discovering the theft and obtain a formal Police Incident Report number.
2. **Contact Apex Security Hotline:** Call 1-800-555-APEX (ext 2 for Security & Claims).
3. **Return Keys:** You must surrender all original keys provided at rental pickup. Failure to return the physical keys creates a legal presumption of gross negligence or vehicle abandonment unless stolen under verified robbery.

## Financial Responsibility
- **With Gold Platinum or CDW:** $0 liability, provided original keys are surrendered and a police report is filed.
- **With Standard Protection:** Renter is liable for the full current actual cash value (ACV) of the vehicle minus recovery value, plus up to 30 days loss of use.
"""
    },
    {
        "filename": "insurance_10_unauthorized_driver_liability.md",
        "title": "Unauthorized Driver Consequences and Liability Voiding",
        "category": "Insurance",
        "content": """# Policy on Unauthorized Drivers and Complete Liability Voiding

## Strict Rule Definition
Only individuals whose names, dates of birth, and driver's license numbers are explicitly listed on the Apex Rental Agreement are authorized to operate the rental vehicle.

## Consequences of Allowing an Unauthorized Driver
If an unauthorized person operates the car for even one minute:
1. **Total Insurance Voidance:** ALL purchased protection plans (CDW, Silver, Gold Platinum, SLI, PAI) are revoked and nullified retroactively.
2. **Direct Personal Liability:** The primary renter becomes 100% personally responsible for all bodily injury, death, and property damage caused to third parties, as well as the complete replacement cost of the Apex vehicle.
3. **Contract Termination:** Apex reserves the right to remotely disable the vehicle ignition via telematics and repossess the car immediately without refund.
4. **Permanent Blacklist:** The primary renter will be permanently barred from all future Apex Car Rental reservations nationwide.
"""
    },

    # --- 3. PRICING & FEES (10 docs) ---
    {
        "filename": "pricing_01_daily_rates_and_weekend_surges.md",
        "title": "Daily Base Rates and Weekend Demand Pricing",
        "category": "Pricing",
        "content": """# Daily Base Rates & Weekend Demand Pricing Structure

## Baseline Tier Pricing
- **Economy Sedan (ECAR):** $45.00 / day
- **Compact Sedan (CCAR):** $48.00 / day
- **Midsize Sedan (ICAR):** $56.00 / day
- **Compact SUV (IFAR):** $72.00 / day
- **Electric EV Standard (ECAR-EV):** $75.00 / day
- **Family 7-Passenger SUV (SFAR):** $85.00 / day
- **Full-Size SUV (FFAR):** $115.00 / day
- **Luxury Sedan (LCAR):** $125.00 / day

## Weekend Surge Pricing
- High-demand periods: Friday 12:00 PM through Sunday 11:59 PM.
- Base daily rates during peak weekend windows may adjust upwards by 10% to 25% depending on local fleet availability.
- Reservations booked more than 14 days in advance are guaranteed the quoted base rate regardless of weekend demand spikes.
"""
    },
    {
        "filename": "pricing_02_young_driver_surcharge.md",
        "title": "Young Driver Surcharge Policy (Ages 21–24)",
        "category": "Pricing",
        "content": """# Young Driver Surcharge Policy (Ages 21 to 24)

## Fee Structure
- **Daily Surcharge:** $20.00 / day per young driver.
- Applies to all primary drivers and authorized additional drivers between 21 and 24 years of age.
- Drivers under 21 years of age are strictly ineligible to rent from Apex (no exceptions).

## Vehicle Restrictions for Young Drivers
To ensure safety and manage actuarial risk, drivers aged 21-24 are permitted to rent the following vehicle classes only:
- Economy Sedan (ECAR)
- Compact Sedan (CCAR)
- Midsize Sedan (ICAR)
- Compact SUV (IFAR)
- Electric Vehicle Standard (Tesla Model 3 RWD)

## Restricted Vehicle Classes
Drivers aged 21-24 CANNOT rent: Full-Size SUVs (Tahoe/Expedition), Luxury Sedans (BMW 5 Series), Luxury SUVs, or 12-Passenger Vans. These classes require the driver to be at least 25 years old.
"""
    },
    {
        "filename": "pricing_03_security_deposits_and_card_holds.md",
        "title": "Security Deposits and Credit/Debit Card Holds",
        "category": "Pricing",
        "content": """# Security Deposits & Authorization Holds

## Credit Card Security Deposit
- **Standard Deposit Hold:** $200.00 USD authorization hold placed on the card at vehicle pickup.
- **Luxury / Full-Size SUV Deposit:** $500.00 USD authorization hold.
- The authorization hold is not an immediate charge; it temporarily freezes available credit line funds.

## Debit Card Acceptance Policy
- Debit cards with Visa or Mastercard logos are accepted at airport and city counters under the following conditions:
  1. A security deposit hold of **$500.00 USD** is processed.
  2. Renter must present proof of a confirmed return airline boarding pass matching the renter's name.
  3. Renter must provide two forms of government identification (e.g., Driver's License + Passport).
  4. Prepaid, Chime, Venmo, CashApp, and crypto cards are strictly NOT accepted.

## Release Timeline
- Security holds are released by Apex within 24 hours of successful vehicle check-in.
- Depending on the customer's issuing bank, the funds typically reappear in available credit in 2 to 5 business days (credit cards) or 5 to 10 business days (debit cards).
"""
    },
    {
        "filename": "pricing_04_fuel_and_ev_recharging_options.md",
        "title": "Fuel Return Options and EV Battery Charging Fees",
        "category": "Pricing",
        "content": """# Fuel & EV Recharging Options

## Standard Fuel Policy: Full-to-Full
All gasoline vehicles depart with a full fuel tank. Return the vehicle with a 100% full tank from a gas station within a 5-mile radius of the return station to pay $0 refueling fees (retain fuel receipt).

## Refueling Options:
1. **Pre-Paid Fuel Option:** Purchase a full tank at discounted wholesale market price at checkout ($3.85/gallon). Return the car at any fuel level with no extra charge. No refund for unused fuel.
2. **Apex Post-Return Refueling Service:** If returned with less than a full tank without pre-paid fuel, Apex refuels the vehicle at **$7.95 per gallon** required to reach full.

## Electric Vehicle (EV) Battery Rules
- **Pickup Level:** Guaranteed at least 80% state of charge.
- **Return Level Required:** At least 70% state of charge.
- **Return Under 70% Fee:** $35.00 recharging convenience fee applied.
- **Return Under 20% Fee:** $65.00 critical battery low recharge fee applied.
- **Pre-Paid EV Recharge Option:** $25.00 flat fee added at pickup lets you return the EV at any battery level down to 10%.
"""
    },
    {
        "filename": "pricing_05_additional_driver_fees.md",
        "title": "Additional Driver Fees and Free Spouse Exemptions",
        "category": "Pricing",
        "content": """# Additional Driver Fees & Legal Exemptions

## Standard Fee
- **Additional Driver Rate:** $10.00 / day per authorized driver (maximum charge capped at $100 per rental contract).

## Free Authorized Driver Exceptions (No Fee)
The daily additional driver fee is waived entirely for:
1. **Legal Spouse or Domestic Partner:** Must live at the same physical residential address shown on driver's license.
2. **Corporate Business Colleagues:** When renting under a recognized Apex Corporate Agreement, company coworkers traveling on company business are authorized at no charge.
3. **Apex Black Tier Loyalty Members:** Black tier members receive one free additional driver on every rental.

## In-Person Registration Mandatory
Every additional driver MUST present their physical, valid driver's license in person at the rental counter before driving.
"""
    },
    {
        "filename": "pricing_06_tolls_and_transponders.md",
        "title": "Electronic Toll Transponder Service (Apex E-Pass)",
        "category": "Pricing",
        "content": """# Electronic Toll Transponder Service (Apex E-Pass)

## Overview & Device
Every Apex vehicle is equipped with an integrated digital toll transponder (compatible with E-ZPass, SunPass, FasTrak, TxTag, ExpressToll, and Peach Pass).

## Option A: Apex Unlimited Toll Pass
- **Daily Rate:** $11.99 / rental day.
- Covers unlimited toll road usage across all state toll plazas and express lanes without per-toll tracking or administrative fees. Recommended for heavy toll corridors (New York, Florida, Texas, California).

## Option B: Pay-Per-Toll Standard
- If you decline the Unlimited Toll Pass and drive through electronic cashless toll lanes, the transponder automatically logs the toll.
- **Fee:** Actual toll rate assessed by the toll authority + a **$4.95 daily usage fee** applied only on days a toll is incurred (daily usage fee capped at $24.75 per 30-day rental period).
"""
    },
    {
        "filename": "pricing_07_cancellation_and_refund_policy.md",
        "title": "Cancellation Terms, No-Shows, and Refund Schedules",
        "category": "Pricing",
        "content": """# Reservation Cancellation, No-Show, & Refund Schedule

## Pay Later (Reserve at Counter) Bookings
- **Cancellation Fee:** $0.00. Cancel at any time before the scheduled pickup time with no penalty.
- No-shows are released 2 hours after scheduled pickup time without financial charge.

## Pre-Paid (Pay Now) Bookings
- **Cancellation 48+ Hours Before Pickup:** 100% full refund returned to the original payment card.
- **Cancellation 24 to 48 Hours Before Pickup:** Refund issued minus a **$50.00 administrative fee**.
- **Cancellation Less Than 24 Hours or No-Show:** Renter is charged a **$100.00 late cancellation fee** (or the total booking amount if under $100); any remainder is refunded.

## Flight Delays & Airline Disruptions
If you provide your airline and flight number during booking, Apex automatically monitors flight status and holds your reservation for up to 6 hours past scheduled arrival without no-show fees.
"""
    },
    {
        "filename": "pricing_08_equipment_addons_pricing.md",
        "title": "Equipment and Add-On Accessory Pricing",
        "category": "Pricing",
        "content": """# Equipment Add-Ons & Accessory Daily Pricing

## Child Safety Seats
- **Infant Rear-Facing Seat (5-22 lbs):** $8.00 / day (capped at $70/rental)
- **Convertible Toddler Seat (20-40 lbs):** $8.00 / day (capped at $70/rental)
- **High-Back Booster Seat (40-80 lbs):** $6.00 / day (capped at $50/rental)
- All child seats meet federal NHTSA crash test specifications. Due to liability regulations, renters must secure the seat into the vehicle latch points themselves.

## Navigation & Connectivity
- **Garmin GPS Touchscreen Navigator:** $6.00 / day (lifetime maps & multi-language voice guidance)
- **Apex 4G LTE Wi-Fi Mobile Hotspot:** $9.95 / day (connects up to 8 laptops and tablets simultaneously with unlimited high-speed data)

## Winter Equipment
- **Ski & Snowboard Roof Rack:** $12.00 / day (holds up to 4 pairs of skis or 2 snowboards; available on SUVs only).
"""
    },
    {
        "filename": "pricing_09_late_return_fees_and_grace_periods.md",
        "title": "Late Return Fees and Grace Period Policies",
        "category": "Pricing",
        "content": """# Late Return Fees & Grace Period Policy

## 29-Minute Official Grace Period
Apex provides a standard **29-minute courtesy grace period** beyond the scheduled drop-off time on your rental agreement without any extra charge.

## Hourly Late Surcharges (30 to 119 minutes late)
- If the vehicle is returned 30 to 119 minutes past the scheduled return time:
  - Billed at **$18.00 per hour** for standard sedans and compact SUVs.
  - Billed at **$28.00 per hour** for luxury vehicles, full-size SUVs, and passenger vans.

## Full Day Charge (120+ minutes late)
Returns 2 hours or more past the scheduled time trigger a full additional day's base rate charge plus a **$25.00 Late Return Administrative Disruption Fee** (as this impacts subsequent reservations).

## Extending Your Rental
Need to keep the car longer? Call 1-800-555-APEX or extend via the app at least 3 hours before drop-off time to lock in your existing daily rate with zero disruption fees.
"""
    },
    {
        "filename": "pricing_10_cleaning_and_smoking_penalties.md",
        "title": "Cleaning Fees and Strict Smoke/Vape Penalties",
        "category": "Pricing",
        "content": """# Cleaning Standards & Prohibited Substance Penalties

## 100% Smoke-Free Fleet Policy
Apex maintains a strictly enforced 100% smoke-free fleet. This includes tobacco cigarettes, cigars, electronic vaporizers (vapes), cannabis products, and e-liquids.

## Smoking Violation Assessment: $300.00 Flat Fine
If any evidence of smoking or vaping is detected upon vehicle return (including residual odor, ash, burns, or vape oil stains):
- A mandatory **$300.00 decontamination and ozone ionizer detailing fee** is charged immediately.

## Pet Hair & Heavy Soil Cleaning Fees
- **Standard Dust / Rain / Light Mud:** Covered under routine complimentary car wash.
- **Excessive Pet Hair, Mud, or Food Spills:** If seats or carpets require deep upholstery shampooing or extraction, an excessive detailing fee between **$150.00 and $250.00** is assessed based on shop labor.
"""
    },

    # --- 4. RENTAL ELIGIBILITY & RESERVATION RULES (10 docs) ---
    {
        "filename": "policy_01_driver_license_requirements.md",
        "title": "Driver's License and Identity Verification Guidelines",
        "category": "Eligibility",
        "content": """# Driver's License & Identity Verification Requirements

## Acceptable Driver's Licenses
- Renter must present an original, physical, government-issued driver's license valid throughout the entire rental duration.
- Must be written in English or accompanied by an official translation or International Driving Permit (IDP).
- Digital driver's licenses (Apple Wallet / State DMV apps) are accepted for identity verification at select airport counters, but a physical physical card must be presented for credit authorization compliance.

## Temporary Paper Licenses
- Accepted only if accompanied by the expired physical plastic license and official DMV government renewal documentation.
- Learner's permits, probationary licenses with nighttime curfews, and photocopies are strictly rejected.
"""
    },
    {
        "filename": "policy_02_international_driving_permits.md",
        "title": "International Driving Permits and Foreign Travelers",
        "category": "Eligibility",
        "content": """# International Driving Permits (IDP) & Overseas Travelers

## Requirements for International Renters
Visitors from outside the United States and Canada must present:
1. **Valid National Driver's License:** Issued by their home country in their legal name.
2. **Valid Passport:** With entry stamp or valid I-94 arrival record.
3. **International Driving Permit (IDP):** Mandatory if the home country driver's license is not in the Roman/Latin alphabet (e.g., Arabic, Cyrillic, Mandarin, Japanese, Hebrew). An IDP translates the home license and is only valid when presented alongside the original physical national license.

## Return Airfare Verification
International renters paying with a debit card must provide proof of an international return airline ticket departing within 30 days of the rental start date.
"""
    },
    {
        "filename": "policy_03_minimum_and_maximum_rental_age.md",
        "title": "Age Restrictions: Minimum and Maximum Rental Ages",
        "category": "Eligibility",
        "content": """# Age Limits & Senior Driver Guidelines

## Minimum Age Requirements
- **Absolute Minimum Age:** 21 years old. Persons aged 20 and younger cannot rent from Apex under any circumstance.
- **Ages 21–24:** Subject to a $20/day Young Driver Surcharge and limited to Economy, Compact, Midsize Sedans, and Standard EVs.
- **Ages 25+:** Eligible to rent all vehicle categories including Luxury, Full-Size SUVs, and 12-Passenger Vans with zero age surcharges.

## Maximum Age Limits
- Apex has **no maximum age ceiling** within the United States.
- Drivers aged 75 and older must possess a valid, unexpired, unrestricted driver's license and undergo standard physical vision check compliance as mandated by their issuing state or nation.
"""
    },
    {
        "filename": "policy_04_geographic_and_cross_border_travel.md",
        "title": "Geographic Limits and Cross-Border Travel (Canada & Mexico)",
        "category": "Eligibility",
        "content": """# Geographic Driving Boundaries & Cross-Border Travel

## Continental United States & Canada
- All Apex vehicles can be freely driven across state borders within the continental United States and into all Canadian provinces with zero border crossing surcharge.
- Unlimited mileage terms remain fully intact while traveling in Canada.

## Travel Into Mexico
- Driving into Mexico is **strictly permitted only from our Texas, Arizona, and California border depots** with prior written authorization.
- Must purchase mandatory **Apex Mexico Auto Insurance** ($35.00/day) at the rental counter, as Mexican federal law does not recognize US domestic insurance or credit card waivers.
- Taking an unauthorized Apex vehicle across the Mexican border is treated as criminal vehicle conversion and automatically voids all insurance.
"""
    },
    {
        "filename": "policy_05_one_way_rentals_and_drop_charges.md",
        "title": "One-Way Rentals and Inter-City Drop Charges",
        "category": "Eligibility",
        "content": """# One-Way Rentals & Inter-City Drop Fees

## Booking a One-Way Rental
Apex supports convenient one-way itineraries between major airport and downtown depots nationwide (e.g., pick up at JFK Airport, drop off at Boston Logan).

## Inter-City Drop Fee Calculation
One-way rentals are subject to a **One-Way Drop Charge** determined by the straight-line distance between the pickup and drop-off hubs:
- **Intra-Metro Transfers (< 50 miles):** $25.00 flat fee.
- **Regional Inter-City (50 to 250 miles):** $75.00 - $150.00 fee.
- **Long-Distance / Cross-Country (250+ miles):** Quoted at booking based on fleet rebalancing demand (typically $0.30 - $0.50 per highway mile).

## Unauthorized Drop-Off Penalty
Returning a vehicle to an unauthorized depot without amending your contract results in a **$250.00 Unauthorized Drop-Off Surcharge** plus standard mileage redistribution fees.
"""
    },
    {
        "filename": "policy_06_loyalty_apex_rewards_club.md",
        "title": "Apex Rewards Loyalty Club Tiers and Privileges",
        "category": "Eligibility",
        "content": """# Apex Rewards Loyalty Club Program

## Membership Levels & Perks
Membership is free to join at booking. Earn 1 Apex Point per $1 spent on rental rates and protection plans.

### 1. Silver Tier (Entry Level - 0 to 4 rentals/year)
- Skip the counter: digital key access directly on your smartphone.
- 5% discount on standard daily base rates.
- Dedicated member priority customer care phone line.

### 2. Gold Tier (5 to 14 rentals/year or 25+ rental days)
- 10% discount on base daily rates.
- Guaranteed complimentary one-car-class vehicle upgrade (subject to availability).
- Free additional driver waiver for spouse or colleague.

### 3. Black Tier (15+ rentals/year or $4,000+ annual spend)
- 15% discount on all rentals.
- Guaranteed double car-class upgrade (e.g., pay for Economy, drive Midsize SUV).
- Free Gold Platinum Protection Plan on every 5th rental.
- Zero cancellation fees on pre-paid reservations up to 1 hour before pickup.
"""
    },
    {
        "filename": "policy_07_corporate_business_accounts.md",
        "title": "Corporate and Commercial Business Travel Accounts",
        "category": "Eligibility",
        "content": """# Apex Corporate & Commercial Business Travel Program

## Corporate Account Benefits
Organizations spending over $10,000 annually qualify for an Apex Corporate Master Agreement:
- **Fixed Negotiated Rates:** Year-round rate ceilings immune to peak holiday and summer surge pricing.
- **Built-In CDW & SLI:** Full collision damage waiver ($0 deductible) and $1,000,000 primary liability automatically included in the negotiated corporate rate.
- **Automatic Authorized Colleagues:** Any full-time employee possessing a valid corporate badge and driver's license is covered as an authorized driver without fees.
- **Direct Corporate Monthly Billing:** Centralized billing through consolidated corporate invoicing with Net-30 payment terms.
"""
    },
    {
        "filename": "policy_08_long_term_and_monthly_rentals.md",
        "title": "Long-Term Mini-Lease and Monthly Rentals (30–90 Days)",
        "category": "Eligibility",
        "content": """# Long-Term & Monthly Mini-Lease Program

## Multi-Week & Monthly Discounts
Rentals extending beyond 28 consecutive days qualify for Apex Long-Term Mini-Lease pricing:
- **28 to 59 Days:** 20% discount off standard daily rate.
- **60 to 90 Days:** 30% discount off standard daily rate.

## Maintenance & Inspection Requirement
- Long-term rentals must complete a complimentary 15-minute maintenance and safety inspection at any Apex service hub every 30 days or every 3,000 miles (whichever occurs first) for oil condition, brake wear, and tire rotation.
- Apex swaps the vehicle for a fresh, identical or higher-class vehicle if scheduled maintenance takes longer than 45 minutes.
"""
    },
    {
        "filename": "policy_09_prohibited_uses_of_vehicles.md",
        "title": "Prohibited Uses and Immediate Contract Default",
        "category": "Eligibility",
        "content": """# Prohibited Uses and Breach of Rental Agreement

## Strictly Forbidden Activities
Under no circumstances may an Apex vehicle be used:
1. **Races, Speed Tests & Tracks:** Operating on closed circuits, racetracks, drag strips, or drifting courses.
2. **Off-Roading:** Driving on unpaved roads, logging paths, beaches, trails, or terrain not recognized as public roads on official state maps.
3. **Commercial Ridesharing / Delivery:** Driving for Uber, Lyft, DoorDash, Instacart, or courier services without an explicit Apex Commercial Ride endorsement.
4. **Towing or Pushing:** Towing another vehicle, trailer, boat, or equipment without factory hitch and Apex authorization.
5. **Transportation of Hazardous Materials:** Carrying combustible chemicals, fireworks, commercial quantities of toxic substances, or contraband.

## Repercussions
Breaching any prohibited use triggers immediate repossession, forfeiture of deposits, assessment of all investigative expenses, and total voiding of insurance.
"""
    },
    {
        "filename": "policy_10_credit_checks_and_scoring_criteria.md",
        "title": "Credit Verification and Soft Inquiries for Debit Renters",
        "category": "Eligibility",
        "content": """# Credit Verification & Screening Guidelines

## Major Credit Cards
Renters presenting an active, valid major credit card (Visa, Mastercard, American Express, Discover) do **NOT** undergo any credit check or credit bureau scoring inquiry. Verification is limited to an authorization hold of the estimated rental amount plus the $200 security deposit.

## Debit Card Soft Credit Inquiry
For customers utilizing a bank debit card at non-airport downtown counters:
- Apex conducts a confidential **soft credit inquiry** via Equifax or Experian.
- A soft inquiry does **NOT** impact the customer's credit score.
- Minimum qualifying score: 620.
- If the customer does not meet the threshold, they must present a valid major credit card to secure the rental.
"""
    },

    # --- 5. VEHICLE PICKUP, RETURN & INSPECTION (10 docs) ---
    {
        "filename": "pickup_01_counter_and_paperwork_checklist.md",
        "title": "Rental Counter Checklist: Required Documents at Pickup",
        "category": "Pickup & Return",
        "content": """# Counter Checklist: What to Bring for Pickup

## Mandatory Items Checklist
Please ensure you bring the following items to the Apex rental desk:
1. **Physical Driver's License:** Unexpired, valid government-issued plastic card in your name.
2. **Major Credit Card or Qualifying Debit Card:** The name on the card must match the primary driver's license exactly.
3. **Reservation Confirmation Number:** 8-character code (e.g., APX-78214) in email or mobile app.
4. **Flight Number (Airport Pickups):** Ensures hold protection in case of airline delays.
5. **Passport & IDP (International Travelers):** Required for overseas customers whose licenses are non-English.
"""
    },
    {
        "filename": "pickup_02_pre_rental_damage_inspection.md",
        "title": "Pre-Rental Vehicle Inspection and Walkaround Protocol",
        "category": "Pickup & Return",
        "content": """# Pre-Rental Vehicle Inspection & Walkaround Protocol

## The 3-Minute Walkaround Process
Before leaving the parking bay, perform a 360-degree walkaround of the vehicle:
1. **Check Body Panels:** Inspect front and rear bumpers, door quarter-panels, and rocker moldings for dents or scrapes.
2. **Check Glass & Lights:** Verify no star chips on the windshield, unbroken headlights, and clean side mirrors.
3. **Check Tires & Wheels:** Inspect tire tread depth and check for alloy wheel curb scratches.
4. **Inspect Cabin:** Check upholstery for burns, excessive pet hair, or lingering tobacco smoke odor.

## Digital Inspection Slip (Apex Scan App)
Use the Apex Mobile App or counter paper slip to photograph any pre-existing blemishes larger than 1 inch (or coin size). Our gate attendant validates and stamps your digital contract so you are never charged for prior damage.
"""
    },
    {
        "filename": "pickup_03_after_hours_key_drop_return.md",
        "title": "After-Hours Key Drop Return Procedures",
        "category": "Pickup & Return",
        "content": """# After-Hours Key Drop Return Protocol

## Returning When the Counter Is Closed
Many Apex locations offer convenient 24/7 key drop boxes for early-morning or late-night departures:
1. **Park the Vehicle:** Park in designated Apex return bays. Turn off headlights and internal cabin lights.
2. **Retrieve Belongings:** Thoroughly check trunk, glove box, center console, and door pockets. Remove sunglasses, chargers, and toll passes.
3. **Note Mileage & Fuel:** Take a photo of the odometer and fuel gauge displayed on the digital dashboard.
4. **Lock the Car:** Lock all vehicle doors securely.
5. **Deposit Key:** Place the key into the heavy-duty yellow Apex Key Drop Slot located beside the rental counter or return booth.

## Final Billing Confirmation
The vehicle is inspected by our morning team at 6:00 AM, and an itemized digital receipt is emailed to you within 2 hours of inspection.
"""
    },
    {
        "filename": "pickup_04_fuel_station_proximity_and_receipts.md",
        "title": "Fuel Return Verification and Local Station Proximity",
        "category": "Pickup & Return",
        "content": """# Fuel Level Verification & Local Station Requirements

## 5-Mile Proximity Rule
Under the Full-to-Full policy, the vehicle must be refueled at a commercial gas station located within a **5-mile radius** of the drop-off depot.

## Retain Your Fuel Receipt
Keep your printed gas pump receipt showing the date, timestamp, number of gallons purchased, and station address. If the fuel gauge reads slightly below 100% due to sensor latency, presenting your receipt within 5 miles guarantees $0 refueling penalty fees.
"""
    },
    {
        "filename": "pickup_05_ev_charging_network_and_adapters.md",
        "title": "EV Charging Guidelines, Supercharger Billing, and Adapters",
        "category": "Pickup & Return",
        "content": """# Electric Vehicle (EV) Charging Guide & Supercharger Billing

## Tesla Supercharger Network Access
- All Apex Tesla vehicles (Model 3 & Model Y) have automated plug-and-charge functionality at all Tesla Supercharger stations.
- Simply plug the cable into the charge port. Charging commences immediately without requiring a Tesla mobile app.
- **Wholesale Pass-Through Billing:** Supercharger kilowatt-hour (kWh) costs are billed directly to your Apex rental invoice with **zero markup or administration fees**.

## Non-Tesla Fast Charging (CCS & J1772)
- Vehicles include a standard J1772 Level 2 adapter located in the glove compartment or front trunk.
- Use Electrify America, EVgo, or ChargePoint networks using credit card tap-to-pay at the charger.
"""
    },
    {
        "filename": "pickup_06_airport_terminal_shuttles.md",
        "title": "Airport Terminal Shuttles and Consolidated Rental Car Centers",
        "category": "Pickup & Return",
        "content": """# Airport Terminal Shuttles & Rental Facilities (ConRAC)

## Finding the Apex Counter at Major Airports
- **On-Airport Consolidated Rental Facilities (ConRAC):** At hubs like ORD, DFW, ATL, and LAX, follow signs for Ground Transportation / Rental Car Shuttles. Dedicated electric trains (People Movers) or airport shuttle buses transport you directly to the unified rental facility.
- **Off-Airport Depot Shuttles:** At locations with dedicated off-site facilities (e.g., JFK or LAS), board the branded **Apex Blue & White Shuttle Van** departing curbside every 10–15 minutes outside baggage claim.
- Track shuttle vans in real-time via the Apex Mobile App GPS tracker.
"""
    },
    {
        "filename": "pickup_07_lost_and_found_property.md",
        "title": "Lost and Found Personal Property Recovery",
        "category": "Pickup & Return",
        "content": """# Lost and Found Personal Property Retrieval

## How to Report a Left-Behind Item
If you left an item in an Apex rental car after turning in your keys:
1. Visit `apexcar.com/lost-and-found` or call the location depot directly within 30 days.
2. Provide your Rental Agreement number (APX-XXXXX), vehicle license plate, and detailed description of the item (color, serial numbers, passwords).
3. If recovered by our vehicle detail team, items are logged into our secure on-site safe.

## Return Shipping Options
Recovered property can be retrieved in person at the local counter during business hours, or shipped to your home address via FedEx / UPS at the customer's expense. Unclaimed items are donated to charity after 60 days.
"""
    },
    {
        "filename": "pickup_08_child_seat_installation_rules.md",
        "title": "Child Safety Seat Inspection and Self-Installation Policy",
        "category": "Pickup & Return",
        "content": """# Child Safety Seat Compliance & Installation Policy

## Strict Self-Installation Rule
Apex rental agents provide certified, sanitized child safety seats and infant carriers upon request. However, by federal insurance guidelines:
- **Apex counter staff are strictly prohibited from strapping or installing child seats into customer vehicles.**
- The parent, legal guardian, or adult renter is solely responsible for proper tethering, LATCH connection, and seatbelt routing.

## Seat Inspection & Sanitation
Every returned car seat undergoes high-temperature steam sanitation and visual structural inspection for harness fraying and buckle integrity before being sealed in protective plastic bags.
"""
    },
    {
        "filename": "pickup_09_winter_driving_and_snow_chains.md",
        "title": "Winter Driving, Mountain Passes, and Snow Chain Policies",
        "category": "Pickup & Return",
        "content": """# Winter Weather Driving & Snow Chain Restrictions

## Mountain Hub Winter Preparedness
Apex vehicles stationed in mountain regions (Denver, Salt Lake City, Seattle, Lake Tahoe) are equipped with high-tread all-season tires (M+S rated) and cold-weather windshield wiper fluids rated to -20°F.

## Snow Chains & Tire Socks Policy
- **Tire Chains:** Metallic tire chains are **strictly prohibited** on low-profile sedans, EVs, and luxury models due to inner wheel-well suspension clearance hazards.
- **Approved Traction Devices:** In states with mandatory chain-control laws (e.g., California I-80 Donner Pass, Colorado Traction Law Code 15), renters traveling in AWD/4WD SUVs with M+S tires meet statutory requirements. If fabric snow socks are necessary, approved auto-socks may be purchased at our mountain counters.
"""
    },
    {
        "filename": "pickup_10_express_return_and_mobile_receipts.md",
        "title": "Apex Express Lane Return and Mobile E-Receipts",
        "category": "Pickup & Return",
        "content": """# Apex Express Drop-Off & Instant Digital Receipts

## The 60-Second Return Flow
For fast airport departures, utilize the Apex Express Return Lane:
1. Drive into the designated **Express Return** lanes.
2. An Apex service agent scans the vehicle barcode affixed to the driver's windshield with a handheld digital terminal.
3. The scanner communicates with the vehicle telematics to instantly read exact mileage, remaining fuel percentage, and diagnostic trouble codes.
4. Hand the key fob to the agent.
5. An itemized invoice is delivered to your email inbox within 60 seconds with zero paperwork to sign.
"""
    },

    # --- 6. EMERGENCY PROCEDURES & ROADSIDE (10 docs) ---
    {
        "filename": "emergency_01_breakdown_and_engine_warning.md",
        "title": "Mechanical Breakdown and Engine Warning Light Protocol",
        "category": "Emergencies",
        "content": """# Mechanical Breakdown & Check Engine Warning Protocol

## Immediate Safety Actions
If a mechanical malfunction occurs or the dashboard displays a flashing check engine warning:
1. **Pull to Safety:** Safely maneuver the vehicle onto the highway shoulder or parking lot away from active traffic.
2. **Activate Hazard Lights:** Turn on hazard flashers and set the parking brake.
3. **Contact 24/7 Roadside Assistance:** Call **1-800-555-APEX (Prompt 1)** immediately.

## Mechanical Replacement Guarantee
If an Apex vehicle suffers a mechanical breakdown not caused by customer abuse or road hazards:
- A roadside tow truck is dispatched within 45 minutes.
- Apex delivers a replacement vehicle directly to your location or arranges complimentary taxi/rideshare transportation to the nearest Apex hub.
- Renter is reimbursed for downtime or refunded the daily rate for the impacted duration.
"""
    },
    {
        "filename": "emergency_02_flat_tire_and_spare_tire_procedure.md",
        "title": "Flat Tire Procedure, Run-Flats, and Tire Repair Kits",
        "category": "Emergencies",
        "content": """# Flat Tire Procedures & Equipment Locations

## Types of Tire Setups by Vehicle Class
- **Sedans & SUVs:** Equipped with a compact donut spare tire, tire jack, and lug wrench located beneath the trunk cargo false floor.
- **Electric Vehicles (Tesla Model 3/Y):** Due to battery weight distribution, EVs do NOT carry a spare tire. They are equipped with an emergency 12V air compressor and chemical sealant kit in the lower trunk compartment.
- **Luxury Sedans (BMW 5 Series):** Outfitted with Run-Flat tires capable of traveling up to 50 miles at a maximum speed of 50 mph following a complete puncture.

## Roadside Dispatch for Tire Service
If you do not wish to change the tire yourself or lack a spare, contact Apex Roadside Dispatch. Covered at $0 with Gold Platinum or Silver Protection; standard dispatch fee of $75 applies under Standard Protection.
"""
    },
    {
        "filename": "emergency_03_accident_reporting_and_police_reports.md",
        "title": "Vehicle Collision Reporting and Police Documentation Requirements",
        "category": "Emergencies",
        "content": """# Collision & Accident Protocol: Step-by-Step

## What to Do at the Scene of an Accident
1. **Check for Injuries & Call Emergency Services:** Call 911 immediately if medical assistance is needed or if significant property damage occurred.
2. **Obtain Official Police Incident Report:** A formal police case number is **mandatory** for all insurance claims and liability waivers.
3. **Exchange Information:** Collect the other driver's full name, phone number, driver's license number, vehicle make/model, license plate, and auto insurance policy number.
4. **Capture Visual Evidence:** Take wide-angle and close-up photographs of both vehicles, vehicle positions relative to street signs, skid marks, and weather conditions.
5. **Report to Apex within 12 Hours:** Call the Apex Claims Department at 1-800-555-APEX (Prompt 3) and submit the online Incident Form.
"""
    },
    {
        "filename": "emergency_04_lost_or_damaged_key_fob.md",
        "title": "Lost, Stolen, or Damaged Smart Key Fob Replacement",
        "category": "Emergencies",
        "content": """# Lost, Stolen, or Water-Damaged Key Fob Policy

## Modern Smart Fob Costs
Modern vehicles utilize encrypted digital proximity key fobs. Replacing, laser-cutting, and reprogramming an electronic key fob requires dealership programming tools:
- **Standard Key Replacement Fee:** $250.00 to $450.00 (depending on vehicle make).
- **Gold Platinum Protection Coverage:** $0 replacement fee for one lost key per rental contract.

## Emergency Mobile Locksmith Dispatch
If keys are locked inside the vehicle or lost at your hotel/activity:
- Apex dispatches an emergency mobile locksmith to decode the door locks or deliver a duplicate backup key from the local hub.
"""
    },
    {
        "filename": "emergency_05_battery_jump_starts_and_dead_cells.md",
        "title": "Dead Battery Jump-Start Protocols and Hybrid 12V Systems",
        "category": "Emergencies",
        "content": """# Dead Battery Jump-Starts & 12V Electrical Systems

## Causes of Discharged Batteries
Leaving dome lights, headlights, or 12V cooler accessories running while the engine is shut off will deplete the starting battery within 3 to 6 hours.

## How to Request a Jump-Start
1. Call 24/7 Roadside Assistance at 1-800-555-APEX.
2. A mobile service vehicle with a booster pack will be routed to your coordinates.
3. **EV Note:** On electric vehicles (Tesla), never attempt to jump-start another vehicle using the Tesla 12V low-voltage battery posts, as this will damage the high-voltage DC-DC inverter and void warranties.
"""
    },
    {
        "filename": "emergency_06_parking_tickets_and_moving_violations.md",
        "title": "Parking Citations, Traffic Camera Violations, and Impounds",
        "category": "Emergencies",
        "content": """# Traffic Violations, Parking Tickets, & Vehicle Impound Protocol

## Paying Citations Directly
Renters are encouraged to pay local municipal parking tickets or toll citations directly to the issuing city before the rental contract closes. Provide the receipt to the Apex desk agent upon return.

## If Apex Receives the Ticket by Mail
If a municipality mails a photo-enforced red light, bus lane, speeding, or parking citation to Apex:
- Apex remits payment to the municipal authority on the vehicle's behalf.
- The fine is charged to the renter's credit card along with a **$30.00 Administrative Processing Fee** per citation.

## Vehicle Impoundment
If the vehicle is towed and impounded due to illegal parking or driving violations, the renter is liable for all towing fees, municipal release charges, storage lot storage fees, and daily rental rates until the vehicle is released.
"""
    },
    {
        "filename": "emergency_07_emergency_fuel_and_battery_towing.md",
        "title": "Emergency Fuel Delivery and Depleted EV Battery Recovery",
        "category": "Emergencies",
        "content": """# Running Out of Fuel or EV Charge on the Highway

## Running Out of Gasoline
- Apex Roadside Assistance dispatches an emergency service vehicle to deliver **3 gallons of fuel** directly to your location.
- **Cost:** Free delivery under Gold Platinum Protection. For standard customers, a flat service dispatch fee of $45.00 plus retail fuel price applies.

## Depleted EV Battery on the Road (0% Charge)
- Electric vehicles cannot be filled with a fuel can. If an EV battery drops to 0% and shuts down, it must be loaded onto a flatbed tow truck (EVs cannot be towed with wheels rolling on the pavement).
- Flatbed transport to the nearest DC Fast Charger or Supercharger is arranged by Apex dispatch. Flatbed transport fees apply unless covered under Gold Platinum.
"""
    },
    {
        "filename": "emergency_08_pet_travel_rules_and_cleaning.md",
        "title": "Pet Travel Guidelines, Service Animals, and Cleanliness",
        "category": "Emergencies",
        "content": """# Traveling with Pets & Service Animals

## Pet-Friendly Policy
Apex is proud to be pet-friendly! Domestic dogs and cats are welcomed in all rental vehicles at zero extra daily pet surcharge.

## Guidelines for Responsible Pet Travel
1. **Crates & Seat Covers:** Pets must be kept in travel crates or travel on protective blankets/hammocks spread across rear seating.
2. **Safety Restraints:** Ensure pets are harnessed safely and not loose on the driver's lap.
3. **Cleanliness:** Return the vehicle free of excessive pet shedding, mud, and odor. A standard vacuuming is appreciated.

## Service Animals
Service animals recognized under the Americans with Disabilities Act (ADA) are exempt from crating rules. Detail cleaning fees are waived for service animal hair unless severe physical upholstery damage occurs.
"""
    },
    {
        "filename": "emergency_09_severe_weather_and_hail_damage.md",
        "title": "Severe Weather Precautions, Flooding, and Hail Damage",
        "category": "Emergencies",
        "content": """# Severe Weather Alerts, Hail, and Flooding Precautions

## Protecting the Vehicle in Bad Weather
- **Hail Storms:** If severe thunderstorm or tornado warnings are issued with large hail, park under covered hotel porticos, underground garages, or gas station canopies when possible.
- **Flash Flooding:** Never drive through standing water or flooded underpasses. Water ingestion into engine air intakes causes hydrolock, destroying the engine block.

## Coverage for Weather Damage
- Weather and act-of-nature damage (hail dents, falling tree branches, flood damage) is fully covered under **Gold Platinum Protection** or **CDW** with $0 deductible.
- Under Standard Protection, the renter's personal comprehensive auto policy applies, or the $1,500 standard deductible is charged.
"""
    },
    {
        "filename": "emergency_10_roadside_assistance_phone_directory.md",
        "title": "Apex 24/7 Roadside Assistance Hotline & Contact Directory",
        "category": "Emergencies",
        "content": """# Apex 24/7 Emergency Hotline Directory

## Toll-Free Emergency Dispatch Lines
- **Primary 24/7 Emergency & Roadside:** 1-800-555-APEX (1-800-555-2739)
  - Prompt 1: Mechanical Breakdown & Towing Dispatch
  - Prompt 2: Flat Tire, Lockout & Dead Battery Assistance
  - Prompt 3: New Collision or Accident Reporting
  - Prompt 4: Security, Vehicle Theft & Fraud Hotline

## Digital Assistance via Smartphone
- **SMS Roadside Chat:** Text `HELP` along with your agreement number to `44273` (44APEX) for instant automated GPS location dispatch.
- **Apex Web Concierge:** Visit `apexcar.com/roadside` to monitor real-time tow truck ETA on Google Maps.
"""
    },

    # --- 7. AIRPORT & DOWNTOWN LOCATIONS (10 docs) ---
    {
        "filename": "location_01_jfk_new_york_airport.md",
        "title": "JFK International Airport Hub (New York City)",
        "category": "Locations",
        "content": """# Location Guide: New York JFK International Airport

## Facility Details & Operating Hours
- **Location Code:** JFK
- **Address:** Building 312, Federal Circle, Jamaica, NY 11430
- **Operating Hours:** Open 24 Hours / 7 Days a week / 365 Days a year
- **Counter Phone:** (718) 555-0142

## How to Reach the Apex JFK Hub
- Take the automated **JFK AirTrain** from any airline terminal directly to **Federal Circle Station**.
- Exit the turnstiles and follow the overhead signs down the escalator to the Ground Transportation shuttle lane.
- Board the dedicated Apex shuttle bus running continuously every 8 minutes (3-minute ride to our depot).

## Fleet Availability at JFK
Full range of AWD SUVs, Electric Vehicles (Tesla Supercharger hub on-site with 12 stalls), and Executive Sedans. All vehicles equipped with E-ZPass toll transponders.
"""
    },
    {
        "filename": "location_02_lax_los_angeles_airport.md",
        "title": "Los Angeles International Airport Hub (LAX)",
        "category": "Locations",
        "content": """# Location Guide: Los Angeles International Airport (LAX)

## Location Information
- **Location Code:** LAX
- **Address:** 9021 South Sepulveda Blvd, Los Angeles, CA 90045
- **Operating Hours:** Open 24 Hours Daily
- **Direct Phone:** (310) 555-0188

## Shuttles & Pickup Instructions
- Exit the lower level (Arrivals / Baggage Claim) and walk to the pink-striped **Rental Car Shuttles** island curbside.
- Board the Apex LAX shuttle for a quick 7-minute ride to our Sepulveda facility.
- Digital keyholders and Black Tier members proceed straight to their assigned parking stalls on the second deck.

## Highlights
Features our largest convertible and EV fleet, with Mustang Convertibles and Tesla Model Ys available year-round.
"""
    },
    {
        "filename": "location_03_ord_chicago_ohare.md",
        "title": "Chicago O'Hare International Airport Hub (ORD)",
        "category": "Locations",
        "content": """# Location Guide: Chicago O'Hare International Airport (ORD)

## Location & Consolidated Facility (MMFAC)
- **Location Code:** ORD
- **Address:** Multi-Modal Facility (MMFAC), 10255 W Zemke Blvd, Chicago, IL 60666
- **Hours:** 24/7 Operations

## Airport Transit System (ATS)
- All O'Hare car rental companies are consolidated within the Multi-Modal Facility.
- Board the complimentary **Airport Transit System (ATS) People Mover Train** from Terminals 1, 2, 3, or 5 directly to the MMF Station (Level 2).
- Apex is located at Counter 6 in the main customer concourse.

## Winterized Vehicles
All ORD vehicles feature high-grade winter windshield washer fluid and high-tread all-season tires for severe Midwestern winter conditions.
"""
    },
    {
        "filename": "location_04_dfw_dallas_fort_worth.md",
        "title": "Dallas/Fort Worth International Airport Hub (DFW)",
        "category": "Locations",
        "content": """# Location Guide: Dallas/Fort Worth International Airport (DFW)

## Facility Overview
- **Location Code:** DFW
- **Address:** 2424 E 38th St, DFW Airport, TX 75261
- **Hours of Operation:** 24 Hours / 7 Days

## Rental Car Shuttle Instructions
- Upon collecting baggage at any terminal (A, B, C, D, or E), exit the lower level curbside.
- Look for the large blue **Rental Car Shuttle** curbside stop. Shuttles depart every 5 minutes for the 10-minute trip to the DFW Rental Car Center.
- Apex is stationed in Zone C of the main floor.

## Local Perks
Extensive inventory of Full-Size SUVs (Chevrolet Tahoe, Ford Expedition) and 4x4 Pickup Trucks (Ford F-150 SuperCrew).
"""
    },
    {
        "filename": "location_05_mia_miami_international_airport.md",
        "title": "Miami International Airport Hub (MIA)",
        "category": "Locations",
        "content": """# Location Guide: Miami International Airport (MIA)

## Consolidated Center (MIA RCC)
- **Location Code:** MIA
- **Address:** MIA Rental Car Center, 3900 NW 25th St, Miami, FL 33142
- **Hours:** 24/7 Operations

## MIA Mover Train
- From the main airport terminal, take the 3rd-floor moving walkway Skyride to the **MIA Mover Station**.
- Take the 4-minute automated electric train directly to the Rental Car Center (RCC).
- Apex is located on the 3rd floor customer hall.

## Special Amenities
Convertibles, Luxury Sedans, and all-inclusive SunPass toll packages available for turnpike travel to Fort Lauderdale and the Florida Keys.
"""
    },
    {
        "filename": "location_06_den_denver_international_airport.md",
        "title": "Denver International Airport Mountain Hub (DEN)",
        "category": "Locations",
        "content": """# Location Guide: Denver International Airport (DEN)

## Facility Details
- **Location Code:** DEN
- **Address:** 25500 E 78th Ave, Denver, CO 80249
- **Operating Hours:** 5:00 AM to 1:00 AM Daily

## Shuttles
- Exit the Jeppesen Terminal on Level 5 (Island 4 outside Baggage Claim doors 505 to 513).
- Board the Apex Mountain Express shuttle running every 8 minutes.

## Colorado Mountain Package
Rentals from DEN heading to ski resorts (Vail, Breckenridge, Aspen) feature AWD SUVs meeting Colorado DOT I-70 Passenger Vehicle Traction Law standards. Ski and snowboard racks available upon advance reservation.
"""
    },
    {
        "filename": "location_07_sfo_san_francisco_airport.md",
        "title": "San Francisco International Airport Hub (SFO)",
        "category": "Locations",
        "content": """# Location Guide: San Francisco International Airport (SFO)

## Consolidated Rental Center
- **Location Code:** SFO
- **Address:** SFO Rental Car Center, 780 N McDonnell Rd, San Francisco, CA 94128
- **Operating Hours:** 24/7 Daily

## AirTrain Access
- Take the **AirTrain Blue Line** from any passenger terminal or the International Terminal directly to the Rental Car Center station.
- Take the escalator to Level 4 for the Apex priority service counter and self-service vehicle bays.

## Green Fleet Focus
SFO has Apex's largest concentration of electric vehicles and plug-in hybrids, offering seamless FasTrak bridge toll processing for Golden Gate and Bay Bridge crossings.
"""
    },
    {
        "filename": "location_08_las_vegas_mccarran_harry_reid.md",
        "title": "Las Vegas Harry Reid International Airport Hub (LAS)",
        "category": "Locations",
        "content": """# Location Guide: Las Vegas Harry Reid International Airport (LAS)

## Rental Car Center (LAS RCC)
- **Location Code:** LAS
- **Address:** 7135 Gilespie St, Las Vegas, NV 89119
- **Operating Hours:** Open 24/7

## Shuttle Directions
- From Terminal 1 or Terminal 3, proceed to baggage claim and follow blue signs to the airport rental car shuttle boarding zone.
- Complimentary shuttles arrive every 5 minutes for the 7-minute trip to the center.

## Specialty Vehicles
Full lineup of Luxury Sedans, Convertibles, and 12-Passenger Vans for corporate convention groups visiting the Las Vegas Strip.
"""
    },
    {
        "filename": "location_09_bos_boston_logan_airport.md",
        "title": "Boston Logan International Airport Hub (BOS)",
        "category": "Locations",
        "content": """# Location Guide: Boston Logan International Airport (BOS)

## Consolidated Rental Agency Center (RCC)
- **Location Code:** BOS
- **Address:** 15 Transportation Way, East Boston, MA 02128
- **Operating Hours:** 5:00 AM to 1:30 AM Daily

## Massport Shuttle Bus (Route 22, 33, 55)
- Board the clean blue-and-white **Massport Rental Car Center Shuttle** curbside at Terminals A, B, C, or E.
- Massport buses run every 4 minutes directly to the centralized multi-level facility.

## Toll Transponders
All Boston vehicles feature registered MassDOT E-ZPass transponders for Sumner Tunnel and Massachusetts Turnpike tolling.
"""
    },
    {
        "filename": "location_10_sea_seattle_tacoma_airport.md",
        "title": "Seattle-Tacoma International Airport Hub (SEA)",
        "category": "Locations",
        "content": """# Location Guide: Seattle-Tacoma International Airport (SEA)

## Dedicated Rental Facility
- **Location Code:** SEA
- **Address:** 3150 S 160th St, SeaTac, WA 98188
- **Operating Hours:** 24/7 Daily

## Shuttle Logistics
- Exit baggage claim at the north and south ends of the main terminal.
- Follow signs to the dedicated SEA airport car rental shuttle bays.
- Shuttles run continuously 24/7 for the 5-minute trip to the rental facility.

## Washington & Pacific Northwest Travel
Unlimited mileage permits easy travel to Mount Rainier National Park, the Olympic Peninsula, and cross-border drives to Vancouver, British Columbia.
"""
    }
]

def main():
    print(f"Generating {len(documents)} realistic domain documents in: {DOCS_DIR}")
    for idx, doc in enumerate(documents, start=1):
        filepath = DOCS_DIR / doc["filename"]
        # Add metadata header as yaml-like frontmatter
        full_text = f"""---
id: DOC-{idx:03d}
title: "{doc['title']}"
category: "{doc['category']}"
filename: "{doc['filename']}"
---

{doc['content'].strip()}
"""
        filepath.write_text(full_text, encoding="utf-8")
        print(f"[{idx:02d}/75] Created: {doc['filename']}")
    print(f"\nSuccessfully created all {len(documents)} documents!")

if __name__ == "__main__":
    main()
