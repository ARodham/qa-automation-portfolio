from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field

app = FastAPI(title="QA Portfolio Demo App", version="1.0.0")

ITEMS = [
    {"id": 1, "name": "Wireless Headset", "category": "Audio", "in_stock": True},
    {"id": 2, "name": "Mechanical Keyboard", "category": "Input", "in_stock": True},
    {"id": 3, "name": "USB-C Dock", "category": "Accessories", "in_stock": False},
]


class ItemCreate(BaseModel):
    name: str = Field(min_length=2, max_length=80)
    category: str = Field(min_length=2, max_length=40)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.get("/api/items")
def list_items():
    return {"count": len(ITEMS), "items": ITEMS}


@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    item = next((x for x in ITEMS if x["id"] == item_id), None)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.post("/api/items", status_code=201)
def create_item(item: ItemCreate):
    return {
        "id": 99,
        "name": item.name,
        "category": item.category,
        "in_stock": True,
    }


@app.get("/", response_class=HTMLResponse)
def login_page():
    return HTMLResponse("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>QA Portfolio Demo</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 760px; margin: 50px auto; padding: 0 18px; }
    input, button { display:block; margin:10px 0; padding:10px; width:300px; }
    #error { color:#a00; margin-top:10px; }
  </style>
</head>
<body>
  <h1>QA Portfolio Demo</h1>
  <p>Sign in to view inventory.</p>
  <form id="login-form">
    <label>Username <input id="username" aria-label="Username"/></label>
    <label>Password <input id="password" aria-label="Password" type="password"/></label>
    <button type="submit">Sign in</button>
  </form>
  <div id="error" role="alert" aria-live="polite"></div>
<script>
document.getElementById("login-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  if (username === "demo_user" && password === "quality123") {
    window.location.href = "/inventory";
  } else {
    document.getElementById("error").textContent = "Invalid username or password";
  }
});
</script>
</body>
</html>
""")


@app.get("/inventory", response_class=HTMLResponse)
def inventory_page():
    return HTMLResponse("""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8"/>
  <title>Inventory</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 760px; margin: 50px auto; padding: 0 18px; }
    input { padding:10px; width:300px; margin-bottom:16px; }
    li { padding:7px 0; }
  </style>
</head>
<body>
  <h1>Inventory</h1>
  <label>Search inventory
    <input id="search" aria-label="Search inventory" placeholder="Search"/>
  </label>
  <ul id="items"></ul>
<script>
async function loadItems() {
  const response = await fetch("/api/items");
  const data = await response.json();
  const list = document.getElementById("items");

  function render(filter = "") {
    list.innerHTML = "";
    data.items
      .filter(item => item.name.toLowerCase().includes(filter.toLowerCase()))
      .forEach(item => {
        const li = document.createElement("li");
        const span = document.createElement("span");
        span.dataset.testid = "item-name";
        span.textContent = item.name;
        li.appendChild(span);
        list.appendChild(li);
      });
  }

  render();
  document.getElementById("search").addEventListener("input", event => render(event.target.value));
}
loadItems();
</script>
</body>
</html>
""")
