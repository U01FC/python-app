import pytest
from app import app
from db import ProductModel, create_product

@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_products_empty(client):
    """Ensure GET /api/products returns an empty list initially."""
    response = client.get("/api/products")
    assert response.status_code == 200
    assert response.json == []

def test_post_product(client):
    """Test adding a new product via POST /api/products."""
    response = client.post("/api/products", json={"name": "Test Product", "price": 99.99})
    assert response.status_code == 201
    assert "productId" in response.json

def test_get_product_by_id(client):
    """Ensure GET /api/products/<id> returns the correct product."""
    product = create_product(name="Sample", price=50.0)
    response = client.get(f"/api/products/{product.id}")
    assert response.status_code == 200
    assert response.json["name"] == "Sample"
    assert response.json["price"] == 50.0

def test_patch_product(client):
    """Test updating a product using PATCH /api/products/<id>."""
    product = create_product(name="Old Name", price=20.0)
    response = client.patch(f"/api/products/{product.id}", json={"name": "New Name", "price": 25.0})
    assert response.status_code == 200
    assert response.json["message"] == "Product updated successfully."

    updated_response = client.get(f"/api/products/{product.id}")
    assert updated_response.json["name"] == "New Name"
    assert updated_response.json["price"] == 25.0

def test_delete_product(client):
    """Test deleting a product using DELETE /api/products/<id>."""
    product = create_product(name="To be deleted", price=10.0)
    response = client.delete(f"/api/products/{product.id}")
    assert response.status_code == 200
    assert response.json["message"] == "Product deleted."

    response = client.get(f"/api/products/{product.id}")
    assert response.status_code == 404
    assert response.json["error"] == "Product not found."
