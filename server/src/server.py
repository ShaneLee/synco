#!/usr/bin/python3
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
import os
from pathlib import Path

app = FastAPI()
server_base_dir = Path("/app/data")

@app.post("/write")
async def write_file(file_path: str, content: str):
    with open(file_path, 'w') as file:
        file.write(content)
    return {"message": "File written successfully!"}

@app.delete("/delete")
async def delete_file(file_path: str):
    if os.path.exists(file_path):
        os.remove(file_path)
        return {"message": "File deleted successfully!"}
    raise HTTPException(status_code=404, detail="File not found")

@app.get("/list")
async def list_files(
    directory_path: str,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    # Construct the full path based on the base directory and provided path
    path = server_base_dir / Path(directory_path)
    
    if not path.is_dir():
        raise HTTPException(status_code=404, detail="Directory not found")
    
    # List files and directories
    all_files = [str(f.relative_to(server_base_dir)) for f in path.iterdir() if f.is_file()]
    all_dirs = [str(d.relative_to(server_base_dir)) for d in path.iterdir() if d.is_dir()]
    
    # Combine files and directories
    combined_list = all_files + all_dirs
    
    # Apply pagination
    paginated_list = combined_list[offset:offset+limit]
    
    return {"items": paginated_list}

@app.post("/diff")
async def diff(file: UploadFile = File(...)):
    file_path = server_base_dir / file.filename

    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Server file not found")

    uploaded_content = await file.read()
    user_filenames = set(uploaded_content.decode().splitlines())

    with file_path.open("r") as server_file:
        server_filenames = set(server_file.read().splitlines())

    missing_filenames = list(server_filenames - user_filenames)

    return {"diff": missing_filenames}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)