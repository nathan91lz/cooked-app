from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from database import get_connection, init_db
from models import Item

app = FastAPI()

# init DB au démarrage
init_db()

templates = Jinja2Templates(directory="app/templates")


###############
# GET INVENTAIRE
@app.get("/", response_class=HTMLResponse)
def read_items(request: Request):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM inventory")
    items = cursor.fetchall()

    conn.close()

    return templates.TemplateResponse("index.html", {
        "request": request,
        "items": items
    })


################
# ADD ITEM (SETTER)

@app.post("/add")
def add_item(name: str = Form(...), quantity: int = Form(...), location: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO inventory (name, quantity, location) VALUES (?, ?, ?)",
        (name, quantity, location)
    )

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