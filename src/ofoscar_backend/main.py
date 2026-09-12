from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Project(BaseModel):
  title: str
  description: str

projects = []

@app.get("/projects")
def get_projects():
  return projects

@app.post("/projects")
def add_project(project: Project):
  projects.append(project)
  return project
