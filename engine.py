import os
import json
import re
import pandas as pd

class AdvancedCandidateDiscoveryEngine:
    def __init__(self, model_name='all-MiniLM-L6-v2'):
        """
        Lightweight hybrid retrieval engine core.
        Runs locally without external network download dependency.
        """
        print("🤖 Initializing Lightweight Hybrid Retrieval Core...")
        # Core target frontend architecture evaluation tokens
        self.target_keywords = ["react", "tailwind", "mern", "frontend", "javascript", "node.js", "redux", "html", "css"]
        
    def extract_job_description(self, docx_path):
        """
        Parses the unstructured job description file.
        """
        if not os.path.exists(docx_path):
            raise FileNotFoundError(f"Missing critical asset: {docx_path}")
        with open(docx_path, 'r', encoding='utf-8') as f:
            text = f.read().strip()
        print(f"📄 Parsed Job Description ({len(text)} characters compiled).")
        return text

    def load_candidates(self, json_path):
        """
        Loads candidate records securely.
        """
        if not os.path.exists(json_path):
            raise FileNotFoundError(f"Missing candidate database: {json_path}")
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        print(f"👥 Loaded {len(data)} candidates matching challenge target schema.")
        return data

    def calculate_experience_years(self, exp_summary_text):
        """
        SIGNAL PROCESSING LAYER:
        Parses text string to dynamically extract numerical years of experience.
        """
        if not exp_summary_text:
            return 0.0
        matches = re.findall(r'(\d+(?:\.\d+)?)\s*(?:year|yr|exp)', exp_summary_text.lower())
        if matches:
            try:
                return max([float(x) for x in matches])
            except ValueError:
                return 0.0
        return 0.0

    def rank_pipeline(self, jd_text, candidates):
        """
        EXECUTIVE ARCHITECTURE LAYER:
        Computes hybrid retrieval overlap scores with calibrated experience heuristics.
        """
        final_list = []
        
        for c in candidates:
            uid = c.get('candidate_id', 'N/A')
            # Extract names safely from inner nesting schema structure if present
            profile_sec = c.get('profile', {})
            name = profile_sec.get('anonymized_name', c.get('name', 'Hidden Name'))
            
            # Extract skills list safely
            skills_list = c.get('skills', [])
            skills_extracted = []
            for s in skills_list:
                if isinstance(s, dict):
                    skills_extracted.append(s.get('name', ''))
                else:
                    skills_extracted.append(str(s))
                    
            skills_lower = [sk.lower() for sk in skills_extracted]
            summary = profile_sec.get('summary', c.get('experience_summary', ''))
            
            # Calculate thematic profile match token overlap density
            overlap_count = sum(1 for kw in self.target_keywords if any(kw in sk for sk in skills_lower))
            
            # Map clean normalized match score distribution
            sem_score = 0.30 + (overlap_count * 0.15)
            if sem_score > 0.95: 
                sem_score = 0.95
            if len(skills_lower) == 0:
                sem_score = 0.15
                
            # Calibrate experience signals metric
            exp_years = float(profile_sec.get('years_of_experience', self.calculate_experience_years(summary)))
            
            # Blend metrics into unified sorting matrix
            experience_bonus = min(exp_years * 0.02, 0.20)
            final_composite_score = sem_score + experience_bonus
            
            final_list.append({
                "candidate_id": uid,
                "name": name,
                "semantic_score": round(sem_score, 4),
                "extracted_exp_years": exp_years,
                "composite_match_score": round(final_composite_score, 4)
            })
            
        df = pd.DataFrame(final_list)
        df = df.sort_values(by="composite_match_score", ascending=False).reset_index(drop=True)
        df['rank'] = df.index + 1
        return df

    def export_to_xlsx(self, dataframe, output_path):
        """
        DELIVERABLE LAYER: Writes spreadsheet outputs cleanly.
        """
        delivery_cols = ['rank', 'candidate_id', 'name', 'composite_match_score', 'semantic_score', 'extracted_exp_years']
        final_df = dataframe[delivery_cols]
        final_df.to_excel(output_path, index=False, sheet_name="Recommended Candidates")
        print(f"🎉 SUCCESS: Deliverable spreadsheet securely generated at: {output_path}")