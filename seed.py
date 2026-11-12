import json
import os
from database import SessionLocal, engine, Base  # Base ko yahan add kiya
import models

# Tables create karo agar pehle se nahi hain
Base.metadata.create_all(bind=engine)  # Yahan change kiya

def load_data():
    db = SessionLocal()
    data_dir = "data"  # Tera folder name
    
    # Check karo agar data pehle se load hai, toh duplicate na ho
    if db.query(models.Question).first():
        print("Data already exists in DB. Skipping seed.")
        return

    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            filepath = os.path.join(data_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                mcqs = data.get("critical_hazards_mcqs", [])
                for item in mcqs:
                    new_q = models.Question(
                        video_id=filename,
                        timestamp=item.get("timestamp"),
                        hazard_description=item.get("hazard_description"),
                        mcq=item.get("mcq"),
                        options=item.get("options"),
                        correct_answer=item.get("correct_answer"),
                        explanation=item.get("safe_action_explanation")
                    )
                    db.add(new_q)
    
    db.commit()
    print("Data seeded successfully!")
    db.close()

if __name__ == "__main__":
    load_data()