import numpy as np
import os
import sys

class Roster:
    def __init__(self, filename):
        with open(os.path.join(sys.path[0], filename)) as file:
            self.text = file.read()
        newtext = ''
        for i in range(len(self.text)-1):
            if self.text[i] == '&':
                seta = set(self.text[i+2:i+5])
                setb = set('APNOXZ')
                newtext = newtext + ' ' + ''.join(seta & setb)
        newtext = newtext.split()
        self.n_weekdays = 7
        self.n_weeks = int(len(newtext) / self.n_weekdays)
        self.data = []
        for i in range(self.n_weeks):
            self.data.append(newtext[i*7:i*7+7])
            
        self.startingWeeks = {'NAVY': (0,3),
                              'LIME': (1,4),
                              'YELLOW': (2,5)}
        
        print(self.data)


    def color_admitting(self, time):
        mins_per_day = 60*24;
        mins_per_week = mins_per_day * self.n_weekdays
        mins_per_roster = mins_per_week * self.n_weeks
        time = time % mins_per_roster
#        rostermins = mins_per_day * self.n_weeks * self.n_weekdays
#        time = time % rostermins
        week = int(np.floor(time / mins_per_week))
        day = int(np.floor((time % mins_per_week) / mins_per_day))
        for i in range(self.n_weeks):
            if 'A' in ''.join(self.data[i][day]):
                self.admitting_week = i
                break
        self.currentWeeks = {'NAVY': ((0+week)%self.n_weeks, (3+week)%self.n_weeks),
                             'LIME': ((1+week)%self.n_weeks, (4+week)%self.n_weeks),
                             'YELLOW': ((2+week)%self.n_weeks, (5+week)%self.n_weeks)}
        
        
        for key in self.currentWeeks.keys():
            if self.admitting_week in self.currentWeeks[key]:
                return key


class Patient:
    a = 1.2180      # shape
    B = 0.00039     # rate

    def __init__(self, admit_time):
        """
        admit_time: minutes
        """
        self.admit_time = admit_time
        self.discharge_time = self.admit_time + self.LoS()
        
    def is_present(self,time):
        return (self.admit_time<=time and self.discharge_time>=time)
        
    def summary(self, time):
        print('Anon patient:\n\tAdmitted: %.1f mins\n\tDischarged: %.1f mins\n\tPresent: %s' % (self.admit_time, self.discharge_time, self.is_present(time)))

    def LoS(self):      # length of stay
        return np.random.gamma(Patient.a, 1/Patient.B)

class Ward:
    def __init__(self, color):
        """
        color: string
        """
        self.color = color
        self.patients = []

    def summary(self, time):
        print('%s ward\n\tPatients: %d' % (self.color, self.n_patients(time)))
        
    def append(self, patient):
        """
        patient: patient object
        """
        self.patients.append(patient)
        
    def n_patients(self, time):
        if isinstance(time, np.ndarray):
            n_patients = np.zeros(len(time))
            for i in range(len(time)):
                n_patients[i] = len([p for p in self.patients if p.is_present(time[i])])
        else:
            n_patients = len([p for p in self.patients if p.is_present(time)])
        return n_patients

class Hospital:
    def __init__(self, name, roster, wards, time):
        """
        name: string
        roster: roster objecti
        wards: list of ward objects
        """
        self.name = name
        self.roster = roster
        self.wards = wards
        self.week = 0       # 0-index weeks and days
        self.weekday = 0

    def summary(self, time):
        print('%s Hospital\n\tCurrent imbalance: %d\n\tWards: %s' % (self.name,
                self.max_imbalance(time), [ward.color for ward in self.wards]))

    def admit(self, patient):
        for ward in self.wards:
            if ward.color == self.roster.color_admitting(patient.admit_time):
                ward.append(patient)
                break

    def max_imbalance(self, time):
        if isinstance(time, np.ndarray):
            imbalance = np.zeros(len(time))
            for k in range(len(time)):
                for i in range(len(self.wards)-1):
                    for j in range(i+1, len(self.wards)):
                        pairwise_imbalance = abs(self.wards[i].n_patients(time[k])-self.wards[j].n_patients(time[k]))
                        if pairwise_imbalance > imbalance[k]:
                            imbalance[k] = pairwise_imbalance
        else:
            imbalance = 0
            for i in range(len(self.wards)-1):
                for j in range(i+1, len(self.wards)):
                    pairwise_imbalance = abs(self.wards[i].n_patients(time)-self.wards[j].n_patients(time))
                    if pairwise_imbalance > imbalance:
                        imbalance = pairwise_imbalance
        return imbalance
