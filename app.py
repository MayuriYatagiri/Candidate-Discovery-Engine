import os
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware  # <-- Import the network layer
from engine import AdvancedCandidateDiscoveryEngine

app = FastAPI(
    title="Intelligent Candidate Discovery API",
    description="Intelligent Candidate Discovery Screening Engine",
    version="1.0.0"
)

# 🌐 Enable seamless browser integration links
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the engine core once on startup
try:
    pipeline = AdvancedCandidateDiscoveryEngine()
except Exception as e:
    print(f"❌ Failed to initialize core pipeline model: {e}")
    pipeline = None

OUTPUT_XLSX = "recommended_candidates.xlsx"

def resolve_asset_paths():
    """
    Points to the asset files in the current root folder.
    """
    return "job_description.txt", "candidates.json"

@app.get("/")
def read_root():
    return {
        "status": "online",
        "challenge": "Intelligent Candidate Discovery",
        "endpoints": {
            "/evaluate-static": "Runs the local pipeline using the workspace files and refreshes the XLSX sheet.",
            "/download-deliverable": "Downloads the compiled recommendations spreadsheet."
        }
    }

@app.post("/evaluate-static")
def evaluate_static_files():
    """
    Triggers the deep semantic ranking engine using the static files in the workspace.
    Refreshes and locks in the recommended_candidates.xlsx spreadsheet.
    """
    if not pipeline:
        raise HTTPException(status_code=500, detail="AI Model Core not initialized properly.")
        
    job_docx, candidates_json = resolve_asset_paths()
    
    if not os.path.exists(job_docx) or not os.path.exists(candidates_json):
        raise HTTPException(
            status_code=404, 
            dateil=f"Challenge asset files missing. Checked: '{job_docx}' and '{candidates_json}'."
        )
        
    try:
        if job_docx.endswith('.txt'):
            with open(job_docx, 'r', encoding='utf-8') as f:
                jd_content = f.read()
        else:
            jd_content = pipeline.extract_job_description(job_docx)
            
        candidate_pool = pipeline.load_candidates(candidates_json)
        final_rankings = pipeline.rank_pipeline(jd_content, candidate_pool)
        pipeline.export_to_xlsx(final_rankings, OUTPUT_XLSX)
        
        top_candidates = final_rankings.to_dict(orient="records")
        return {
            "status": "success",
            "message": "Pipeline successfully recalculated. Deliverable sheet updated.",
            "total_candidates_evaluated": len(final_rankings),
            "top_10_preview": top_candidates
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline failure: {str(e)}")

@app.get("/download-deliverable")
def download_xlsx_sheet():
    if not os.path.exists(OUTPUT_XLSX):
        raise HTTPException(status_code=400, detail="Spreadsheet file not generated yet. Run /evaluate-static first.")
    
    return FileResponse(
        path=OUTPUT_XLSX, 
        filename="candidate_recommendations.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )