from flask import Flask, jsonify, request, send_from_directory, render_template_string
from flask_cors import CORS
import csv
import json
import os

app = Flask(__name__, static_folder='recipe-images', static_url_path='/recipe-images')
CORS(app)

# HTML template for the landing page
LANDING_PAGE_HTML = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Recipe API - Documentation</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 40px 20px;
        }
        .container {
            max-width: 900px;
            margin: 0 auto;
        }
        .header {
            text-align: center;
            color: white;
            margin-bottom: 40px;
        }
        .header h1 {
            font-size: 3rem;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .header p {
            font-size: 1.2rem;
            opacity: 0.9;
        }
        .status-badge {
            display: inline-block;
            background: #4ade80;
            color: #166534;
            padding: 8px 16px;
            border-radius: 20px;
            font-weight: 600;
            margin-top: 15px;
        }
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            margin-bottom: 25px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        }
        .card h2 {
            color: #4c1d95;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e5e7eb;
        }
        .endpoint {
            background: #f8fafc;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 15px;
            border-left: 4px solid #667eea;
        }
        .endpoint:last-child {
            margin-bottom: 0;
        }
        .method {
            display: inline-block;
            padding: 4px 12px;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.85rem;
            margin-right: 10px;
        }
        .method.get {
            background: #dbeafe;
            color: #1e40af;
        }
        .endpoint-url {
            font-family: 'Consolas', 'Monaco', monospace;
            color: #7c3aed;
            font-weight: 600;
        }
        .endpoint-desc {
            color: #64748b;
            margin-top: 10px;
            line-height: 1.6;
        }
        .params-table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 15px;
        }
        .params-table th, .params-table td {
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }
        .params-table th {
            background: #f1f5f9;
            color: #475569;
            font-weight: 600;
        }
        .params-table code {
            background: #e0e7ff;
            padding: 2px 8px;
            border-radius: 4px;
            color: #4338ca;
            font-size: 0.9rem;
        }
        .example-box {
            background: #1e1e1e;
            color: #d4d4d4;
            padding: 15px 20px;
            border-radius: 8px;
            font-family: 'Consolas', 'Monaco', monospace;
            font-size: 0.9rem;
            overflow-x: auto;
            margin-top: 15px;
        }
        .example-label {
            color: #9ca3af;
            font-size: 0.8rem;
            margin-bottom: 8px;
            display: block;
        }
        .try-btn {
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 8px 16px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 600;
            font-size: 0.85rem;
            margin-top: 10px;
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .try-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
        }
        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }
        .feature {
            text-align: center;
            padding: 20px;
            background: #f8fafc;
            border-radius: 10px;
        }
        .feature-icon {
            font-size: 2.5rem;
            margin-bottom: 10px;
        }
        .feature h3 {
            color: #4c1d95;
            margin-bottom: 5px;
        }
        .feature p {
            color: #64748b;
            font-size: 0.9rem;
        }
        .footer {
            text-align: center;
            color: white;
            margin-top: 40px;
            opacity: 0.8;
        }
        .footer a {
            color: white;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🍛 Recipe API</h1>
            <p>A RESTful API for Indian recipes with filtering capabilities</p>
            <div class="status-badge">✓ Service Running</div>
        </div>

        <div class="card">
            <h2>✨ Features</h2>
            <div class="features">
                <div class="feature">
                    <div class="feature-icon">📚</div>
                    <h3>Rich Data</h3>
                    <p>Detailed recipe information with ingredients & steps</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🔍</div>
                    <h3>Smart Filters</h3>
                    <p>Filter by region, cuisine, diet type & more</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">🖼️</div>
                    <h3>Images</h3>
                    <p>Recipe thumbnails included</p>
                </div>
                <div class="feature">
                    <div class="feature-icon">⚡</div>
                    <h3>Fast & Free</h3>
                    <p>No authentication required</p>
                </div>
            </div>
        </div>

        <div class="card">
            <h2>📡 API Endpoints</h2>
            
            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-url">/recipes</span>
                <p class="endpoint-desc">Retrieve all recipes with optional filtering. Returns an array of recipe objects.</p>
                
                <table class="params-table">
                    <thead>
                        <tr>
                            <th>Parameter</th>
                            <th>Type</th>
                            <th>Description</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td><code>region</code></td>
                            <td>string</td>
                            <td>Filter by region (e.g., North, South, East, West)</td>
                        </tr>
                        <tr>
                            <td><code>cuisine</code></td>
                            <td>string</td>
                            <td>Filter by cuisine type (e.g., Punjabi, Tamil)</td>
                        </tr>
                        <tr>
                            <td><code>diet_type</code></td>
                            <td>string</td>
                            <td>Filter by diet (e.g., veg, non-veg)</td>
                        </tr>
                        <tr>
                            <td><code>difficulty</code></td>
                            <td>string</td>
                            <td>Filter by difficulty level</td>
                        </tr>
                        <tr>
                            <td><code>max_oil</code></td>
                            <td>integer</td>
                            <td>Maximum oil content in ml</td>
                        </tr>
                    </tbody>
                </table>
                
                <span class="example-label">Example Request:</span>
                <div class="example-box">GET /recipes?region=North&diet_type=veg&max_oil=50</div>
                <a href="/recipes" target="_blank" class="try-btn">Try it →</a>
            </div>

            <div class="endpoint">
                <span class="method get">GET</span>
                <span class="endpoint-url">/recipes/{recipe_id}</span>
                <p class="endpoint-desc">Retrieve a specific recipe by its unique ID.</p>
                
                <span class="example-label">Example Request:</span>
                <div class="example-box">GET /recipes/recipe_001</div>
            </div>
        </div>

        <div class="card">
            <h2>📦 Response Format</h2>
            <p class="endpoint-desc">Each recipe object contains the following fields:</p>
            <div class="example-box">
{
    "id": "recipe_001",
    "name": "Butter Chicken",
    "region": "North",
    "cuisine": "Punjabi",
    "diet_type": "non-veg",
    "difficulty": "Medium",
    "prep_time_min": 30,
    "cook_time_min": 45,
    "servings": 4,
    "estimated_oil_ml": 60,
    "ingredients": ["chicken", "butter", "tomatoes", ...],
    "steps": ["Marinate chicken...", "Heat oil...", ...],
    "thumbnail_url": "/recipe-images/butter_chicken.jpg"
}
            </div>
        </div>

        <div class="footer">
            <p>Built with ❤️ using Flask | <a href="https://github.com/QuincyThawne/Recipe" target="_blank">GitHub</a></p>
        </div>
    </div>
</body>
</html>
'''


@app.route('/recipe-images/<path:filename>')
def serve_image(filename):
    """Serve recipe images."""
    return send_from_directory('recipe-images', filename)

def load_recipes(base_url=None):
    """Load recipes from CSV file."""
    recipes = []
    csv_path = os.path.join(os.path.dirname(__file__), 'recipes_rows.csv')
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Parse JSON fields
            try:
                row['ingredients'] = json.loads(row['ingredients'])
            except (json.JSONDecodeError, KeyError):
                row['ingredients'] = []
            
            try:
                row['steps'] = json.loads(row['steps'])
            except (json.JSONDecodeError, KeyError):
                row['steps'] = []
            
            # Convert numeric fields
            try:
                row['estimated_oil_ml'] = float(row['estimated_oil_ml']) if row.get('estimated_oil_ml') else None
            except (ValueError, TypeError):
                row['estimated_oil_ml'] = None
            
            try:
                row['servings'] = int(row['servings']) if row.get('servings') else None
            except (ValueError, TypeError):
                row['servings'] = None
            
            try:
                row['prep_time_min'] = int(row['prep_time_min']) if row.get('prep_time_min') else None
            except (ValueError, TypeError):
                row['prep_time_min'] = None
            
            try:
                row['cook_time_min'] = int(row['cook_time_min']) if row.get('cook_time_min') else None
            except (ValueError, TypeError):
                row['cook_time_min'] = None
            
            # Build full image URL if base_url is provided
            if base_url and row.get('thumbnail_url'):
                row['thumbnail_url'] = base_url + row['thumbnail_url']
            
            recipes.append(row)
    
    return recipes


@app.route('/')
def root():
    """Landing page with API documentation."""
    return render_template_string(LANDING_PAGE_HTML)


@app.route('/recipes', methods=['GET'])
def get_recipes():
    """Get all recipes with optional filters."""
    base_url = request.host_url.rstrip('/')
    recipes = load_recipes(base_url)
    
    # Get query parameters
    region = request.args.get('region')
    cuisine = request.args.get('cuisine')
    diet_type = request.args.get('diet_type')
    max_oil = request.args.get('max_oil', type=int)
    difficulty = request.args.get('difficulty')
    
    # Apply filters
    filtered_recipes = recipes
    
    if region:
        filtered_recipes = [r for r in filtered_recipes if r.get('region', '').lower() == region.lower()]
    
    if cuisine:
        filtered_recipes = [r for r in filtered_recipes if r.get('cuisine', '').lower() == cuisine.lower()]
    
    if diet_type:
        filtered_recipes = [r for r in filtered_recipes if r.get('diet_type', '').lower() == diet_type.lower()]
    
    if difficulty:
        filtered_recipes = [r for r in filtered_recipes if r.get('difficulty', '').lower() == difficulty.lower()]
    
    if max_oil is not None:
        filtered_recipes = [r for r in filtered_recipes if r.get('estimated_oil_ml') is not None and r['estimated_oil_ml'] <= max_oil]
    
    return jsonify(filtered_recipes)


@app.route('/recipes/<string:recipe_id>', methods=['GET'])
def get_recipe(recipe_id):
    """Get a specific recipe by ID."""
    base_url = request.host_url.rstrip('/')
    recipes = load_recipes(base_url)
    
    for recipe in recipes:
        if recipe.get('id') == recipe_id:
            return jsonify(recipe)
    
    return jsonify({"error": "Recipe not found"}), 404


# For local development
if __name__ == '__main__':
    app.run(debug=True, port=5000)
