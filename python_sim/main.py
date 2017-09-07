from classes import Roster, Patient, Ward, Hospital
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    colors = ['NAVY', 'LIME', 'YELLOW']
    roster = Roster('roster.txt')
    wards = [Ward(color) for color in colors]

    hospital = Hospital('Trump', roster, wards, None)
    admit_times = np.random.rand(1000)*60480*6
    for t in admit_times:
        hospital.admit(Patient(t))
    patient = Patient(admit_time=0)
    hospital.admit(patient)
    
    t = 15000
    hospital.summary(t)
    for ward in wards:
        ward.summary(t)
#        for patient in ward.patients:
#            patient.summary(t)

    # generate patients
    
    sample_t = np.linspace(0, 60480*6, 1001)
#    for ward in hospital.wards:
#        plt.plot(sample_t, ward.n_patients(sample_t))
    plt.plot(sample_t, hospital.max_imbalance(sample_t))

