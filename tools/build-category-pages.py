#!/usr/bin/env python3
"""Generate the seven new-category warranty pages from an existing page shell.
Usage: build.py <site_dir>
All figures are copied from the Integrity PDS documents (retail prices incl. GST)."""
import sys, json, html, pathlib, re

site = pathlib.Path(sys.argv[1])
shell = (site / "hybrid-electric-car-warranty/index.html").read_text()

head_end = shell.index("<script type=\"application/ld+json\">")
gtag_start = shell.index("<script async src=\"https://www.googletagmanager.com")
main_start = shell.index("<main id=\"main\">")
main_end = shell.index("</main>") + len("</main>")
HEAD_TAIL = shell[gtag_start:main_start]          # gtag + body open + header
FOOT = shell[main_end:]
FONTS = shell[shell.index('<link rel="icon"'):head_end]

def money(n):
    return n if isinstance(n, str) else "${:,}".format(n)

def table(head, rows, first_th=True):
    out = ['<div class="tbl-scroll"><table class="cmp">', "<thead><tr>"]
    out += ['<th scope="col">%s</th>' % h for h in head]
    out.append("</tr></thead>\n<tbody>")
    for r in rows:
        cells = []
        for i, c in enumerate(r):
            c = money(c)
            cells.append('<th scope="row">%s</th>' % c if i == 0 and first_th else "<td>%s</td>" % c)
        out.append("<tr>%s</tr>" % "".join(cells))
    out.append("</tbody></table></div>")
    return "\n".join(out)

COMMON_EXCL = ("faults that were evident before you bought the {noun} or before the manufacturer's warranty ended, "
               "wear and tear, missed or late servicing, modifications outside the manufacturer's specification, "
               "accident, fire, theft, misuse, rust and corrosion, and repairs started without Integrity's approval")

P = []

P.append(dict(
    slug="caravan-warranty", key="caravan", name="Caravan warranty", noun="caravan", pds="integrity-caravan-warranty-pds-v2.2.pdf", pds_name="Caravan Warranty PDS",
    title="Caravan Warranty: Cover, Limits and Prices | MyDriveShield",
    desc="Integrity Caravan and Caravan Plus warranty. Claim limits from $2,500 to $10,000, 12 to 60 months, every price shown from $375 incl. GST.",
    h1="Extended warranty for caravans, with every limit and price shown",
    lead="Two cover types, three levels and five terms. Here is who qualifies, what each level pays and what it costs.",
    intro="The Integrity Caravan Warranty helps with the cost of repairing or replacing listed parts of your caravan after a breakdown or failure. You choose <b>Caravan</b> or <b>Caravan Plus</b>, a level from 1 to 3, and a term of 12, 24, 36, 48 or 60 months.",
    elig=(["Level", "Caravan age when you buy"], [["Level 1", "Up to 12 years old"], ["Level 2", "Up to 7 years old"], ["Level 3", "Up to 5 years old"]]),
    cover=(["What's covered", "Level 1", "Level 2", "Level 3"], [
        ["Parts covered by the original manufacturer's warranty", 2500, 5000, 10000],
        ["Water ingress from the roof, external door, or side, front and rear windows", 1000, 1000, 1000],
        ["<b>Caravan Plus only:</b> living quarters: air conditioning, entertainment unit, fridge, floor heating, hot water unit, microwave, pressure pump, reverse camera, solar panel, pull-out step, stove and rangehood, TV and DVD, washing machine and dryer", 1000, 1000, 1000]]),
    price_note="",
    prices=(["Term", "Caravan L1", "Caravan Plus L1", "Caravan L2", "Caravan Plus L2", "Caravan L3", "Caravan Plus L3"], [
        ["12 months", 375, 732, 410, 758, 464, 821], ["24 months", 419, 866, 464, 901, 508, 955], ["36 months", 464, 1000, 508, 1044, 553, 1089],
        ["48 months", 508, 1133, 544, 1178, 580, 1223], ["60 months", 553, 1267, 589, 1303, 642, 1357]]),
    benefits=["Accommodation: up to $150 a day and $500 per claim, if the caravan is immobilised for more than 1 day and more than 100 km from home",
              "Towing: up to $100 per claim, if the caravan can't be safely towed by your vehicle",
              "Consequential damage to another listed part: up to $350 per claim"],
    service="Your caravan must be serviced every 12 months by a qualified caravan service agent. Keep every service invoice. If a service is more than 30 days late, the warranty becomes inactive.",
    excl_extra="Damage from off-road use is excluded. So are batteries, tyres, glass, cosmetic items and fading or deterioration of paint, trim, curtains and awnings.",
    faqs=[("Does the warranty cover water leaks?", "Water ingress from the roof, external door and the side, front and rear windows is covered up to $1,000 per claim on every level. Other water damage is excluded."),
          ("What is the difference between Caravan and Caravan Plus?", "Caravan Plus adds the living quarters, such as the fridge, air conditioning, hot water unit and solar panel, with a limit of $1,000 per claim."),
          ("Is off-road use covered?", "No. Damage arising out of off-road use is excluded under the PDS.")],
    frm=375))

P.append(dict(
    slug="jet-ski-warranty", key="jetski", name="Jet ski warranty", noun="jet ski", pds="integrity-jetski-warranty-pds-v2.2.pdf", pds_name="Jetski Warranty PDS",
    title="Jet Ski Warranty: Cover, Limits and Prices | MyDriveShield",
    desc="Integrity Jetski warranty. Four levels, engine and jet pump limits from $1,000 to market value, 12 to 60 months, from $589 incl. GST.",
    h1="Extended warranty for jet skis, with every limit and price shown",
    lead="Four levels and three terms. Here is who qualifies, what each level pays and what it costs.",
    intro="The Integrity Jetski Warranty helps with the cost of repairing or replacing listed parts of your jet ski after a breakdown or failure. You choose a level from 1 to 4 and a term of 12, 36 or 60 months. The jet ski must be seaworthy when you buy the warranty.",
    elig=(["Level", "Jet ski age when you buy"], [["Level 1", "Any age"], ["Level 2", "Up to 10 years old"], ["Level 3", "Up to 8 years old"], ["Level 4", "Up to 5 years old"]]),
    cover=(["What's covered", "Level 1", "Level 2", "Level 3"], [
        ["Engine (listed internal parts)", 1000, 2000, 3000], ["Jet pump: jet unit and impeller shaft", 1000, 2000, 3000],
        ["Electric trim motor", 500, 750, 1000], ["Cooling system", 500, 750, 1000], ["Cylinder head: valves, valve springs and hydraulic lifters", 500, 750, 1000],
        ["Bilge pump (if fitted by the manufacturer), cylinder head gasket, ECU, electrical system, fuel system, ignition system, steering system, turbo or supercharger", "Not covered", "$500 each", "$750 each"]]),
    cover_note="<b>Level 4</b> covers the parts that were originally covered by the manufacturer's warranty, except the PDS exclusions, up to the jet ski's market value.",
    price_note="",
    prices=(["Term", "Level 1", "Level 2", "Level 3", "Level 4"], [["12 months", 589, 910, 1160, 1776], ["36 months", 1026, 1330, 1580, 2410], ["60 months", 1214, 1500, 1776, 2678]]),
    benefits=["Towing: up to $100 per claim, if the jet ski's trailer can't be safely towed", "Consequential damage to another listed part: up to $350 per claim"],
    service="Levels 1 to 3, jet ski up to 10 years old: a 4 stroke must be serviced every 12 months or 50 hours, a 2 stroke every 6 months or 25 hours, whichever comes first. Over 10 years old: a 4 stroke every 6 months or 25 hours, a 2 stroke every 6 months or 15 hours. Level 4: follow the manufacturer's schedule. Services must be done by a qualified jet ski service agent. If a service is more than 30 days or 5 hours late, the warranty becomes inactive.",
    excl_extra="Water ingress, submersion and corrosion are excluded. So is use in racing, competitions or sporting events, and damage from poor quality or incorrect fuel.",
    faqs=[("Is there an age limit?", "Level 1 has no age limit. Level 2 is for jet skis up to 10 years old, Level 3 up to 8 years and Level 4 up to 5 years."),
          ("Is a supercharged jet ski covered?", "The turbo or supercharger is a listed part on Levels 2 and 3. A failure caused by a unit that wasn't supplied, fitted or endorsed by the manufacturer is excluded."),
          ("Does it cover water getting into the engine?", "No. Failures caused by water ingress, submersion or corrosion are excluded under the PDS.")],
    frm=589))

P.append(dict(
    slug="boat-warranty", key="marine", name="Boat and marine warranty", noun="boat", pds="integrity-marine-warranty-pds-v2.2.pdf", pds_name="Marine Warranty PDS",
    title="Boat &amp; Marine Engine Warranty: Limits and Prices | MyDriveShield",
    desc="Integrity Marine warranty for single and twin engine boats. Engine limits from $1,500 to $5,000, 12 to 60 months, from $500 incl. GST.",
    h1="Extended warranty for boats and marine engines, with every limit and price shown",
    lead="Three levels, three terms and separate prices for single and twin engines. Here is who qualifies, what each level pays and what it costs.",
    intro="The Integrity Marine Warranty helps with the cost of repairing or replacing listed parts of your vessel after a breakdown or failure. You choose a level from 1 to 3 and a term of 12, 36 or 60 months. The vessel must be seaworthy when you buy the warranty.",
    elig=(["Level", "Vessel age when you buy"], [["Level 1", "Any age"], ["Level 2", "Up to 10 years old"], ["Level 3", "Up to 7 years old"]]),
    cover=(["What's covered", "Level 1", "Level 2", "Level 3"], [
        ["Engine (listed internal parts)", 1500, 3000, 5000], ["Gearbox lower unit: internally lubricated parts of the gear foot, stern drive and gearbox", 1500, 3000, 5000],
        ["Cooling system: water pump impeller and bearings", 500, 750, 1000], ["Hydraulics: lines, pump, power tilt and trim motor", 500, 750, 1000],
        ["Propeller: internal bushing", 500, 750, 1000], ["Cylinder head: heads, valve lifters and valve springs", 500, 750, 1000],
        ["Bilge pump (if fitted by the manufacturer), control box and steering system, cylinder head gasket, electric anchor winch motor, electrical system, fuel system, GPS (sounder and marine radio), trailer brake master cylinder and calipers", "Not covered", "$750 each", "$1,000 each"]]),
    price_note="",
    prices=(["Term", "L1 single", "L1 twin", "L2 single", "L2 twin", "L3 single", "L3 twin"], [
        ["12 months", 500, 732, 714, 857, 1000, 1285], ["36 months", 821, 1071, 1000, 1214, 1464, 1714], ["60 months", 982, 1250, 1160, 1357, 1625, 1964]]),
    benefits=["Towing: up to $100 per claim, if the vessel's trailer can't be safely towed", "Consequential damage to another listed part: up to $350 per claim"],
    service="Levels 1 and 2: service every 6 months or 50 hours, whichever comes first. Level 3: every 12 months or 100 hours. Services must be done by a qualified vessel service agent. If a service is more than 30 days or 5 hours late, the warranty becomes inactive.",
    excl_extra="Water ingress, submersion and corrosion are excluded. So is use in racing, competitions or sporting events, and damage from poor quality or incorrect fuel.",
    faqs=[("Why are there single and twin engine prices?", "The price depends on whether the vessel has one engine or two. Both are shown in the price table."),
          ("Is the trailer covered?", "On Levels 2 and 3 the trailer's brake master cylinder and brake calipers are listed parts. Wheels and tyres are excluded."),
          ("Is there an age limit?", "Level 1 has no age limit. Level 2 is for vessels up to 10 years old and Level 3 up to 7 years.")],
    frm=500))

P.append(dict(
    slug="motorbike-warranty", key="motorbike", name="Motorbike warranty", noun="motorbike", pds="integrity-motorbike-warranty-pds-v2.2.pdf", pds_name="Motorbike Warranty PDS",
    title="Motorbike Warranty: Cover, Limits and Prices | MyDriveShield",
    desc="Integrity Motorbike warranty for motorbikes, scooters and quad bikes. Four levels, 12 to 60 months, every price shown from $232 incl. GST.",
    h1="Extended warranty for motorbikes, scooters and quad bikes, with every limit and price shown",
    lead="Four levels and three terms. Here is who qualifies, what each level pays and what it costs.",
    intro="The Integrity Motorbike Warranty helps with the cost of repairing or replacing listed parts after a breakdown or failure. It can be bought for a motorbike, scooter or quad bike. You choose a level from 1 to 4 and a term of 12, 36 or 60 months.",
    elig=(["Level", "Motorbike when you buy"], [["Level 1", "Any age and any kilometres"], ["Level 2", "Up to 10 years old and under 100,000 km"], ["Level 3", "Up to 6 years old and under 50,000 km"], ["Level 4", "Up to 5 years old and under 40,000 km"]]),
    cover=(["What's covered", "Level 1", "Level 2"], [
        ["Engine (listed internal parts)", 500, 2000], ["Gearbox and transmission: internally lubricated parts", 500, 2000], ["Cooling system: water pump, cooling fan and fan clutch", 500, 2000],
        ["Brakes: master cylinder and disc brake calipers", 500, 2000], ["Electrical: starter motor, alternator and voltage regulator", 500, 2000],
        ["ABS module, clutch master and slave cylinder, engine control module, cylinder head and gasket, final drive, fuel pump and injectors, ignition switch, radiator", "Not covered", "$2,000 each"]]),
    cover_note="<b>Levels 3 and 4</b> cover the parts that were originally covered by the manufacturer's warranty, except the PDS exclusions. Level 3 pays up to $5,000 per claim. Level 4 pays up to the motorbike's market value.",
    price_note="",
    prices=(["Term", "Level 1", "Level 2", "Level 3", "Level 4"], [["12 months", 232, 696, 785, 1053], ["36 months", 410, 875, 982, 1321], ["60 months", 589, 1053, 1178, 1767]]),
    benefits=["Accommodation: up to $150 a day and $500 per claim, if the motorbike is immobilised for more than 1 day and more than 100 km from home",
              "Car or motorbike hire: up to $100 a day and $500 per claim, if the motorbike is immobilised for more than 2 days",
              "Consequential damage to another listed part: up to $350 per claim"],
    service="Levels 1 and 2: service every 6 months or 6,000 km, whichever comes first. Levels 3 and 4: follow the manufacturer's schedule. Services must be done by a licensed mechanical workshop. If a service is more than 30 days or 1,000 km late, the warranty becomes inactive.",
    excl_extra="Damage from off-road use is excluded. So is use in racing, rallies or motor sport events.",
    faqs=[("Are scooters and quad bikes included?", "Yes. The PDS defines a motorbike as the motorbike, scooter or quad bike named on your warranty schedule."),
          ("Is off-road riding covered?", "No. Any damage arising out of off-road use is excluded under the PDS."),
          ("How much does Level 1 pay?", "Up to $500 per claim for each listed part: engine, gearbox, cooling system, brakes and electrical.")],
    frm=232))

MH_ROWS = "Engine, gearbox and transmission, differential, turbo or supercharger, ABS brake system, air conditioning, brakes, clutch, computers, cooling system, cylinder head and gasket, driveshaft and universals, electrical, fuel system, ignition system, power windows, radiator, steering, suspension, transmission computer"
P.append(dict(
    slug="motorhome-warranty", key="motorhome", name="Motorhome warranty", noun="motorhome", pds="integrity-motorhome-warranty-pds-v2.2.pdf", pds_name="Motorhome Warranty PDS",
    title="Motorhome Warranty: Cover, Limits and Prices | MyDriveShield",
    desc="Integrity Motorhome and Motorhome Plus warranty. Claim limits from $1,000 to $5,000 per part, 12 to 60 months, from $750 incl. GST.",
    h1="Extended warranty for motorhomes, with every limit and price shown",
    lead="Two cover types, three levels and three terms. Here is who qualifies, what each level pays and what it costs.",
    intro="The Integrity Motorhome Warranty helps with the cost of repairing or replacing listed parts of your motorhome after a breakdown or failure. You choose <b>Motorhome</b> or <b>Motorhome Plus</b>, a level from 1 to 3, and a term of 12, 36 or 60 months.",
    elig=(["Level", "Motorhome when you buy"], [["Level 1", "Any age and any kilometres"], ["Level 2", "Up to 15 years old and under 200,000 km"], ["Level 3", "Up to 10 years old and under 160,000 km"]]),
    cover=(["What's covered", "Level 1", "Level 2", "Level 3"], [
        [MH_ROWS + " (listed parts in each section; the limit applies to each section)", 1000, 3000, 5000],
        ["Water ingress from the roof, external door, or side, front and rear windows", 350, 1250, 1500],
        ["<b>Motorhome Plus only:</b> living quarters: air conditioning, entertainment unit, fridge, floor heating, hot water unit, microwave, pressure pump, reverse camera, solar panel, pull-out step, stove and rangehood, TV and DVD, washing machine and dryer", 1000, 1000, 1000]]),
    price_note="",
    prices=(["Term", "Motorhome L1", "Plus L1", "Motorhome L2", "Plus L2", "Motorhome L3", "Plus L3"], [
        ["12 months", 750, 1107, 1107, 1464, 1821, 2178], ["36 months", 821, 1357, 1178, 1714, 2250, 2428], ["60 months", 928, 1642, 1285, 2000, 2714, 3071]]),
    benefits=["Accommodation: up to $150 a day and $500 per claim, if the motorhome is immobilised for more than 1 day and more than 100 km from home",
              "Towing: up to $100 per claim, if the motorhome can't be safely driven",
              "Consequential damage to another listed part: up to $350 per claim"],
    service="Your motorhome must be serviced every 6 months or 10,000 km, whichever comes first, by a licensed mechanical workshop. If a service is more than 30 days or 1,000 km late, the warranty becomes inactive.",
    excl_extra="Damage from off-road use is excluded. So are batteries, tyres, glass and cosmetic items.",
    faqs=[("What is the difference between Motorhome and Motorhome Plus?", "Motorhome Plus adds the living quarters, such as the fridge, air conditioning, hot water unit and solar panel, with a limit of $1,000 per claim."),
          ("Is there an age or kilometre limit?", "Level 1 has none. Level 2 is for motorhomes up to 15 years old and under 200,000 km. Level 3 is up to 10 years old and under 160,000 km."),
          ("Does it cover water leaks?", "Water ingress from the roof, external door and windows is covered up to $350, $1,250 or $1,500 per claim, depending on the level.")],
    frm=750))

P.append(dict(
    slug="machinery-warranty", key="machinery", name="Machinery warranty", noun="machine", pds="integrity-machinery-warranty-pds-v1.0.pdf", pds_name="Machinery Warranty PDS",
    title="Machinery Warranty: Cover, Limits and Prices | MyDriveShield",
    desc="Integrity Machinery warranty. Engine, transmission and hydraulic pump limits of $2,000 or $3,000, 12 to 60 months, from $942 incl. GST.",
    h1="Extended warranty for machinery, with every limit and price shown",
    lead="Two levels and three terms. Here is who qualifies, what each level pays and what it costs.",
    intro="The Integrity Machinery Warranty helps with the cost of repairing or replacing listed parts of your machine after a breakdown or failure. You choose Level 1 or Level 2 and a term of 12, 36 or 60 months.",
    elig=(["Level", "Machine when you buy"], [["Level 1", "Any age and any hours"], ["Level 2", "Up to 10 years old and under 10,000 hours"]]),
    cover=(["What's covered", "Level 1", "Level 2"], [
        ["Engine (listed internal parts)", 2000, 3000], ["Gearbox and transmission: internally lubricated parts, torque converter and transfer case", 2000, 3000],
        ["Differential: internally lubricated parts", 2000, 3000], ["Turbo or supercharger: impellers and bearings", 2000, 3000], ["Hydraulics: hydraulic pumps", 2000, 3000],
        ["Air conditioning compressor", 750, 1250], ["Engine control module", 750, 1250], ["Cooling system: water pump and cooling fan", 750, 1250],
        ["Cylinder head and head gasket", 750, 1250], ["Electrical: starter motor and alternator", 750, 1250], ["Fuel system: lift pump, injector pump and metal delivery lines", 750, 1250]]),
    price_note="",
    prices=(["Term", "Level 1", "Level 2"], [["12 months", 942, 1308], ["36 months", 1300, 1541], ["60 months", 1478, 1933]]),
    benefits=["Downtime: up to $100 a day and $500 per claim, if the machine is immobilised for 2 business days in a row",
              "Consequential damage to another listed part: up to $500 per claim", "EGR or DPF regeneration: up to $350 per claim"],
    service="Your machine must be serviced as the manufacturer directs, by a licensed mechanical workshop. Each service invoice must show the date and hour reading. If a service is more than 30 days or 5 hours late, the warranty becomes inactive.",
    excl_extra="",
    faqs=[("Is there an age or hour limit?", "Level 1 has none. Level 2 is for machines up to 10 years old with under 10,000 hours."),
          ("Does it pay for downtime?", "When a claim is approved, up to $100 a day and $500 per claim, if the machine is immobilised for 2 business days in a row."),
          ("How do I buy?", "Ask us for a quote. We will confirm the machine's details with you before cover is arranged.")],
    frm=942))

P.append(dict(
    slug="truck-warranty", key="truck", name="Truck warranty", noun="truck", pds="integrity-truck-warranty-pds-v3.2.pdf", pds_name="Truck Warranty PDS",
    title="Truck Warranty: Cover, Limits and Prices | MyDriveShield",
    desc="Integrity Truck warranty for medium, heavy and prime mover trucks. Engine limits from $5,000 to $20,000, 6 to 24 months, from $2,500 incl. GST.",
    h1="Extended warranty for trucks, with every limit and price shown",
    lead="Three levels, three terms and three weight classes. Here is who qualifies, what each level pays and what it costs.",
    intro="The Integrity Truck Warranty helps with the cost of repairing or replacing listed parts of your truck after a breakdown or failure. You choose a level from 1 to 3 and a term of 6, 12 or 24 months. The price depends on the truck's gross vehicle mass (GVM).",
    elig=(["Level", "Truck when you buy"], [["Level 1", "Up to 15 years old or 800,000 km"], ["Level 2", "Up to 12 years old or 650,000 km"], ["Level 3", "Up to 10 years old or 500,000 km"]]),
    cover=(["What's covered", "Level 1", "Level 2", "Level 3"], [
        ["Engine (listed internal parts)", 5000, 10000, 20000], ["Gearbox and transmission: internally lubricated parts", 5000, 10000, 20000], ["Differential: internally lubricated parts", 5000, 10000, 20000],
        ["Air conditioning compressor", 1250, 2500, 5000], ["Brakes: master cylinder and power booster", 1250, 2500, 5000],
        ["Cooling system: water pump, cooling fan and fan clutch", 1250, 2500, 5000], ["Electrical: starter motor, alternator and voltage regulator", 1250, 2500, 5000]]),
    price_note="Medium is 4,000 to 16,500 kg GVM. Heavy is 16,501 to 22,500 kg GVM. Prime mover is 22,501 kg GVM and above.",
    prices=(["Level and term", "Medium", "Heavy", "Prime mover"], [
        ["Level 1, 6 months", 2500, 2857, 3214], ["Level 1, 12 months", 3303, 3660, 4017], ["Level 1, 24 months", 4910, 6071, 6517],
        ["Level 2, 6 months", 4107, 4464, 4732], ["Level 2, 12 months", 5892, 6250, 6517], ["Level 2, 24 months", 9464, 10178, 10696],
        ["Level 3, 6 months", 5535, 5892, 6071], ["Level 3, 12 months", 7678, 8035, 8303], ["Level 3, 24 months", 12946, 13660, 14151]]),
    benefits=["Accommodation: up to $150 a day and $500 per claim, if the truck is immobilised for more than 1 day and more than 100 km from home",
              "Towing: up to $100 per claim, if the truck can't be safely driven", "Consequential damage to another listed part: up to $350 per claim"],
    service="Your truck must be serviced as the manufacturer directs, by a licensed mechanical workshop. Each service invoice must show the date and odometer reading. If a service is more than 30 days or 1,000 km late, the warranty becomes inactive.",
    excl_extra="Damage from off-road use is excluded. So is use in racing, rallies or motor sport events.",
    faqs=[("How is my truck's class decided?", "By its gross vehicle mass. Medium is 4,000 to 16,500 kg, heavy is 16,501 to 22,500 kg and prime mover is 22,501 kg and above."),
          ("What terms are available?", "6, 12 or 24 months."),
          ("How do I buy?", "Ask us for a quote. We will confirm the truck's details with you before cover is arranged.")],
    frm=2500))

COMMON_FAQ = ("Can I cancel?", "Yes. You get a full refund if you cancel within 30 days of purchase, or before cover starts, and no claim has been paid. After that the refund is pro rata, less any accepted claim and a $62.50 administration fee.")

def page(p):
    url = "https://mydriveshield.com.au/%s/" % p["slug"]
    faqs = p["faqs"] + [COMMON_FAQ]
    ld = [{"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
              {"@type": "ListItem", "position": 1, "name": "Home", "item": "https://mydriveshield.com.au/"},
              {"@type": "ListItem", "position": 2, "name": p["name"], "item": url}]},
          {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
              {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faqs]}]
    quote = "/?callback=%s#quote" % p["key"]
    cta = "Request a %s quote" % p["noun"]
    desc = html.escape(p["desc"], quote=True)
    head = f'''<!DOCTYPE html>
<html lang="en-AU">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{p["title"]}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="noindex">
<link rel="canonical" href="{url}">
<meta property="og:type" content="website">
<meta property="og:title" content="{p["title"]}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta name="twitter:card" content="summary">
{FONTS}<script type="application/ld+json">{json.dumps(ld)}</script>
'''
    cover_note = '<p>%s</p>' % p["cover_note"] if p.get("cover_note") else ""
    price_note = '<p>%s</p>' % p["price_note"] if p.get("price_note") else ""
    excl_extra = " " + p["excl_extra"] if p["excl_extra"] else ""
    pds = "/docs/" + p["pds"]
    main = f'''<main id="main">
<section class="page-hero">
  <div class="wrap">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="/">Home</a> / <span aria-current="page">{p["name"]}</span></nav>
    <h1>{p["h1"]}</h1>
    <p>{p["lead"]}</p>
    <div class="hx-actions"><a href="{quote}" class="btn btn-primary btn-lg" data-cat="{p["key"]}">{cta}</a></div>
  </div>
</section>
<div class="doc">
<p>{p["intro"]} The warranty is issued by Integrity Car Care. If the {p["noun"]} is still under the manufacturer's warranty, cover begins when that ends.</p>
<div class="note"><p><b>This is not insurance.</b> It is a discretionary risk product. Integrity decides whether to pay each claim and considers every claim on its merits. The claim limit is the most that can be paid for a listed part per claim, and an approved amount may be lower.</p></div>

<h2>Who can buy it</h2>
{table(*p["elig"])}

<h2>What's covered and the claim limits</h2>
{table(*p["cover"])}
{cover_note}
<p>Limits are per claim and include GST. The full list of parts in each section is in the <a href="{pds}">{p["pds_name"]}</a>.</p>

<h2>Prices</h2>
{table(*p["prices"])}
{price_note}
<p>All prices include GST. These are the full prices set out in the PDS.</p>

<h2>Extra benefits when a claim is approved</h2>
<ul>
{"".join("<li>%s</li>" % b for b in p["benefits"])}
</ul>
<p>You pay first and are reimbursed on a paid invoice, under the conditions in the PDS.</p>

<h2>Servicing you must keep up</h2>
<p>{p["service"]} The cost of servicing is yours.</p>

<h2>What isn't covered</h2>
<p>The PDS excludes {COMMON_EXCL.format(noun=p["noun"])}.{excl_extra} Only the listed part that failed first is covered, apart from the consequential damage benefit above. The full lists are in the <a href="{pds}">{p["pds_name"]}</a>.</p>

<h2>Claims, transfers and cancelling</h2>
<ul>
<li>Contact Integrity on <a href="tel:0391206666">03 9120 6666</a> before any repair starts. Repairs started without approval are rejected.</li>
<li>You pay for diagnosis unless it is accepted as part of an approved claim.</li>
<li>If you sell, the warranty can be transferred to the new owner within 7 days for a $62.50 fee, with a condition report.</li>
<li>Full refund if you cancel within 30 days of purchase and no claim has been paid.</li>
</ul>

<h2>Common questions</h2>
<div class="faq" style="margin:0">
{"".join('<div class="qa"><button aria-expanded="false">%s<span class="plus">+</span></button><div class="ans"><p>%s</p></div></div>' % (html.escape(q), a) for q, a in faqs)}
</div>
<div class="cta-row"><a href="{quote}" class="btn btn-primary btn-lg" data-cat="{p["key"]}">{cta}</a></div>
<p style="font-size:13.5px;color:var(--muted)">MyDriveShield gives factual information and arranges cover as Integrity Car Care's Authorised Representative. We don't give general or personal advice. Read the <a href="{pds}">{p["pds_name"]}</a> to decide whether the product suits you. Eligibility is subject to Integrity's approval.</p>
</div>
</main>'''
    return head + HEAD_TAIL + main + FOOT

for p in P:
    d = site / p["slug"]
    d.mkdir(exist_ok=True)
    (d / "index.html").write_text(page(p))
    print("wrote", p["slug"], "from", money(p["frm"]))

json.dump([{k: p[k] for k in ("slug", "key", "name", "frm")} for p in P], open(pathlib.Path(__file__).with_name("pages.json"), "w"))
