import os

from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.database import get_connection, init_db
from app.models import Item

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# init DB au démarrage
init_db()

templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

###############
# GET INVENTAIRE
@app.get("/", response_class=HTMLResponse)
def read_items(request: Request):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "items": items
        }
    )

@app.get("/shopping", response_class=HTMLResponse)
def shopping_page(request: Request):
    return templates.TemplateResponse(
        request,
        "shopping.html",
        {}
    )


@app.get("/recipes", response_class=HTMLResponse)
def recipes_page(request: Request):
    return templates.TemplateResponse(
        request,
        "recipes.html",
        {}
    )


################
# ADD ITEM (SETTER)
@app.post("/add")
def add_item(
    name: str = Form(...),
    quantity: int = Form(...),
    unit: str = Form(...),
    location: str = Form(...)
):
    
    name= name.strip().lower()

    if quantity <= 0:
        raise HTTPException(
            status_code=400,
            detail="La quantité doit être supérieure à 0"
        )

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO inventory (name, quantity, unit, location)
        VALUES (?, ?, ?, ?)
        ON CONFLICT(name, location, unit)
        DO UPDATE SET quantity = quantity + excluded.quantity
    """, (name, quantity, unit, location))

    conn.commit()
    conn.close()

    return RedirectResponse("/", status_code=303)


##############
# DELETE ITEM
@app.post("/delete/{item_id}")
def delete_item(item_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))

    conn.commit()
    conn.close()

    return RedirectResponse("/", status_code=303)