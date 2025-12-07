from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import csv
import json
import os

app = Flask(__name__, static_folder='recipe-images', static_url_path='/recipe-images')
CORS(app)


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
    """Health check endpoint."""
    return jsonify({"status": "Flask Recipe Service Running"})


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
