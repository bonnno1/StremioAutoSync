#!/bin/bash

# List of addon slugs and display names
declare -A addons=(
  ["netflix"]="Netflix AU"
  ["disney"]="Disney+ AU"
  ["stan"]="Stan AU"
  ["prime"]="Prime Video AU"
  ["apple"]="Apple TV+ AU"
  ["trending"]="Top Trending"
  ["cinema"]="Now in Cinemas"
  ["popular"]="Most Popular"
  ["new"]="New Releases"
  ["action"]="Action"
  ["comedy"]="Comedy"
  ["family"]="Family"
  ["horror"]="Horror"
  ["kids"]="Kids"
  ["thriller"]="Thriller"
  ["adventure"]="Adventure"
  ["romance"]="Romance"
)

for slug in "${!addons[@]}"; do
  name="${addons[$slug]}"
  echo "🚀 Creating folder for $slug"

  mkdir -p "$slug"

  echo "📝 Generating manifest.json"
  cat > "$slug/manifest.json" <<EOF
{
  "id": "org.stremio.$slug",
  "name": "$name",
  "description": "Auto-updating $name catalog from TMDb",
  "version": "1.0.0",
  "resources": ["catalog"],
  "types": ["series"],
  "catalogs": [{
    "type": "series",
    "id": "$slug",
    "name": "$name"
  }],
  "idPrefixes": ["tt"]
}
EOF

  echo "📁 Copying catalog.json"
  if [ -f "catalogs/$slug.json" ]; then
    cp "catalogs/$slug.json" "$slug/catalog.json"
  else
    echo "⚠️ WARNING: catalogs/$slug.json not found. Skipping."
  fi

done

echo "✅ All addon folders generated."
