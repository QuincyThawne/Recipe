# Recipe API

A Flask-based REST API for serving Indian recipe data with filtering capabilities.

## Features

- Browse all recipes
- Filter by region, cuisine, diet type, difficulty, and maximum oil content
- Get individual recipe details by ID
- Serves recipe thumbnail images

## API Endpoints

### Health Check
```
GET /
```
Returns service status.

### Get All Recipes
```
GET /recipes
```

**Query Parameters:**
| Parameter | Type | Description |
|-----------|------|-------------|
| `region` | string | Filter by region |
| `cuisine` | string | Filter by cuisine type |
| `diet_type` | string | Filter by diet type (veg/non-veg) |
| `difficulty` | string | Filter by difficulty level |
| `max_oil` | integer | Maximum oil content in ml |

### Get Recipe by ID
```
GET /recipes/<recipe_id>
```
Returns a specific recipe by its ID.

## Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the development server:
   ```bash
   python app.py
   ```

3. Access the API at `http://localhost:5000`

## Deployment on Vercel

This project is configured for deployment on Vercel.

1. Install Vercel CLI:
   ```bash
   npm install -g vercel
   ```

2. Deploy:
   ```bash
   vercel
   ```

Or connect your GitHub repository to Vercel for automatic deployments.

## Project Structure

```
├── app.py              # Main Flask application
├── recipes_rows.csv    # Recipe data
├── recipe-images/      # Recipe thumbnail images
├── requirements.txt    # Python dependencies
├── vercel.json         # Vercel configuration
└── README.md           # This file
```

## License

MIT
