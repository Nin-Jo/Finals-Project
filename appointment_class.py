class Appointment:
    def __init__(self, id, appt, appt_type, pet_type, gender, name, breed, age_yrs, weight_kgs, color,
                 owner, phone, email, vet, specialty, price):
        self.id = id
        self.appt = appt
        self.appt_type = appt_type
        self.pet_type = pet_type
        self.gender = gender
        self.name = name
        self.breed = breed
        self.age_yrs = age_yrs
        self.weight_kgs = weight_kgs
        self.color = color
        self.owner = owner
        self.phone = phone
        self.email = email
        self.vet = vet
        self.specialty = specialty
        self.price = price

    def __str__(self):
        return (f"Appointment N{self.id}.\n"
                f"Checked in at {self.appt} for {self.appt_type}.\n"
                f"Patient: A {self.color} {self.breed} {self.pet_type}, {self.gender}, named '{self.name}',\n"
                f"{self.age_yrs} years old, weighs {self.weight_kgs}kgs.\n"
                f"Owner: {self.owner}. Their contact info: {self.phone}, {self.email}.\n"
                f"Patient seen by: {self.vet}, {self.specialty},\n"
                f"Checkout price: ${self.price}.")