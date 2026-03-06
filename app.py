from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pandas as pd
import plotly.express as px
import markdown
import os
import json

app = FastAPI()

templates = Jinja2Templates(directory="templates")

app.mount("/static", StaticFiles(directory="static"), name="static")


# ---------- HOME ----------

@app.get("/")
def home(request: Request):

    trips = pd.read_csv("data/travel_trips.csv").head(3).to_dict(orient="records")

    projects = os.listdir("content/projects")[:3]
    notes = os.listdir("content/notes")[:3]

    return templates.TemplateResponse(
        "home.html",
        {
            "request": request,
            "projects": projects,
            "trips": trips,
            "notes": notes
        }
    )


# ---------- PROJECTS ----------

@app.get("/projects")
def projects(request: Request):

    files = os.listdir("content/projects")

    return templates.TemplateResponse(
        "projects.html",
        {"request": request, "projects": files}
    )


@app.get("/projects/{project}")
def project_page(request: Request, project: str):

    path = f"content/projects/{project}"

    with open(path, "r") as f:
        html = markdown.markdown(f.read())

    return templates.TemplateResponse(
        "project_page.html",
        {"request": request, "content": html, "title": project}
    )


# ---------- DASHBOARDS ----------

@app.get("/dashboards")
def dashboards(request: Request):

    travel = pd.read_csv("data/travel_trips.csv")

    total_trips = len(travel)
    avg_cost = travel["cost"].mean()

    fig = px.bar(travel, x="trip_name", y="cost", title="Trip Cost")
    travel_chart = fig.to_html(full_html=False)

    trades = pd.read_csv("data/swing_trades.csv")

    win_rate = (trades["profit_percent"] > 0).mean()

    fig2 = px.line(trades, x="date", y="profit_percent", title="Trade Performance")
    trade_chart = fig2.to_html(full_html=False)

    return templates.TemplateResponse(
        "dashboards.html",
        {
            "request": request,
            "total_trips": total_trips,
            "avg_cost": round(avg_cost,2),
            "win_rate": round(win_rate*100,2),
            "travel_chart": travel_chart,
            "trade_chart": trade_chart,
            "trips": travel.to_dict(orient="records"),
            "trades": trades.to_dict(orient="records")
        }
    )


# ---------- TRAVEL ----------

@app.get("/travel")
def travel(request: Request):

    trips = pd.read_csv("data/travel_trips.csv")

    return templates.TemplateResponse(
        "travel.html",
        {"request": request, "trips": trips.to_dict(orient="records")}
    )


@app.get("/travel/{trip}")
def travel_trip(request: Request, trip: str):

    df = pd.read_csv("data/travel_trips.csv")

    row = df[df["trip_name"] == trip].iloc[0].to_dict()

    return templates.TemplateResponse(
        "travel_trip.html",
        {"request": request, "trip": row}
    )


# ---------- NOTES ----------

@app.get("/notes")
def notes(request: Request):

    files = os.listdir("content/notes")

    return templates.TemplateResponse(
        "notes.html",
        {"request": request, "notes": files}
    )


@app.get("/notes/{note}")
def note_page(request: Request, note: str):

    path = f"content/notes/{note}"

    with open(path) as f:
        html = markdown.markdown(f.read())

    return templates.TemplateResponse(
        "note_page.html",
        {"request": request, "content": html, "title": note}
    )

@app.get("/api/github")
def github_stats():

    with open("data/github_stats.json") as f:
        stats = json.load(f)

    return stats

@app.get("/github")
def github_dashboard(request: Request):

    with open("data/github_stats.json") as f:
        stats = json.load(f)

    return templates.TemplateResponse(
        "github.html",
        {"request": request, "stats": stats}
    )