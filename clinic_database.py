import sqlite3

class Database:
    def __init__(self, db = "clinic_database.sqlite3"):
        self.conn = sqlite3.connect(db)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

    def read_appt(self):
        self.cursor.execute("""
            SELECT 
                appointments_normalized.id,
                appointments_normalized.appt,
                appointment_types.type AS appt_type,
                pet_types.type AS pet_type,
                appointments_normalized.gender,
                appointments_normalized.name,
                appointments_normalized.breed,
                appointments_normalized.age_yrs,
                appointments_normalized.weight_kgs,
                appointments_normalized.color,
                owners.name AS owner,
                owners.phone,
                owners.email,
                vets.name AS vet,
                vets.specialty,
                appointments_normalized.price
            FROM appointments_normalized
            JOIN appointment_types ON appointments_normalized.appt_type_id = appointment_types.id
            JOIN pet_types ON appointments_normalized.pet_type_id = pet_types.id
            JOIN owners ON appointments_normalized.owner_id = owners.id
            JOIN vets ON appointments_normalized.vet_id = vets.id
            ORDER BY appointments_normalized.appt;
        """)
        return self.cursor.fetchall()

    def get_appt_type_id(self, appt_type):
        self.cursor.execute("SELECT id FROM appointment_types WHERE type = ?", (appt_type,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_pet_type_id(self, pet_type):
        self.cursor.execute("SELECT id FROM pet_types WHERE type = ?", (pet_type,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_owner_id(self, owner_name):
        self.cursor.execute("SELECT id FROM owners WHERE name = ?", (owner_name,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def get_vet_id(self, vet_name):
        self.cursor.execute("SELECT id FROM vets WHERE name = ?", (vet_name,))
        row = self.cursor.fetchone()
        return row[0] if row else None

    def create_appt(self, appt, appt_type, pet_type, gender, name, breed, age_yrs, weight_kgs, color,
                    owner, vet, price):
        appt_type_id = self.get_appt_type_id(appt_type)
        pet_type_id = self.get_pet_type_id(pet_type)
        owner_id = self.get_owner_id(owner)
        vet_id = self.get_vet_id(vet)

        if None in (appt_type_id, pet_type_id, owner_id, vet_id):
            raise ValueError("One or more foreign keys could not be resolved.")

        self.cursor.execute("""
            INSERT INTO appointments_normalized 
            (appt, appt_type_id, pet_type_id, gender, name, breed, age_yrs, weight_kgs, color,
             owner_id, vet_id, price)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                            (appt, appt_type_id, pet_type_id, gender, name, breed, age_yrs, weight_kgs, color,
            owner_id, vet_id, price))
        self.conn.commit()
        return self.cursor.lastrowid

    def update_appt(self, id, appt, appt_type, pet_type, gender, name, breed, age_yrs, weight_kgs, color,
                        owner, vet, price):
        appt_type_id = self.get_appt_type_id(appt_type)
        pet_type_id = self.get_pet_type_id(pet_type)
        owner_id = self.get_owner_id(owner)
        vet_id = self.get_vet_id(vet)

        if None in (appt_type_id, pet_type_id, owner_id, vet_id):
            raise ValueError("One or more foreign keys could not be resolved for update.")

        self.cursor.execute("""UPDATE appointments_normalized SET appt=?, appt_type_id=?, pet_type_id=?, gender=?, name=?, breed=?, age_yrs=?, weight_kgs=?, color=?,
                 owner_id=?, vet_id=?, price=? WHERE id=?""",
                            (appt, appt_type_id, pet_type_id, gender, name, breed, age_yrs, weight_kgs, color,
                 owner_id, vet_id, price, id))
        self.conn.commit()

    def delete_appt(self, id):
        self.cursor.execute("DELETE FROM appointments_clean WHERE id=?", (id,))
        self.conn.commit()