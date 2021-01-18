import pandas as pd
import re
import numpy as np
import json


class MatchingInterviewerService:
    
    panel_data = pd.read_csv('./panel_info.csv')
    
    
    def get_skills_similarty_score(self, remaining_panel, skills_required):
        remaining_panel['processed_skills'] = remaining_panel['skills'].str.split(',')
        remaining_panel['processed_skills']= remaining_panel['processed_skills'].apply(lambda x:[s.lower() for s in x]) 

        skills_required = [s.strip() for s in skills_required]
        skills_required = [s.lower() for s in skills_required]

        s1 = set(skills_required)
        print("required skills", s1)

        remaining_panel['skills_sim_score'] = remaining_panel['processed_skills'].apply(lambda x : np.round(float(len(s1.intersection(set(x))) / len(s1.union(set(x)))),3))

        remaining_panel.sort_values('skills_sim_score',inplace=True,ascending=False)
        return remaining_panel

    
    
    
    def get_best_x_interviwer_info(self, candidate_dict, check_location=None,check_department=None,x=2):

        panel_data = self.panel_data
        
        if check_location:
            panel_data=panel_data[panel_data['location']==candidate_dict['location']]

        if check_department:
            panel_data=panel_data[panel_data['department']==candidate_dict['department']]    


        # select panel based on role 
        panel_data['role_level'] = panel_data['role'].str.replace(r'[^\d.]+', '')
        panel_data['role_level']=panel_data['role_level'].astype(int)

        candidate_level=int(re.sub("[^0-9]", "", candidate_dict['role']))
        panel_left = panel_data[panel_data['role_level']>= candidate_level]


        panel_info = self.get_skills_similarty_score(panel_left, candidate_dict['skills_required']) 
        panel_info=panel_info.head(x)
        panel_info = panel_info[['name', 'email', 'role', 'department', 'skills', 'location']].head(x)
        
        json_list = json.loads(json.dumps(list(panel_info.T.to_dict().values())))

        return json_list
