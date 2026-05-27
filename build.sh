echo "Starting static site generation"

echo "Clearing previous build"
rm -rf gen && mkdir gen

echo "Copying css"
cp -v -r src/*.css gen/

echo "Generating pages"
for page in src/*.html; do
    page_name=$(basename "$page")
    echo "Processing $page_name"
    page_content=$(cat "$page")

    # This goes over every component and tries to swap it into the page. Not
    # efficient since it doesn't check if they're present first but not a big
    # deal.
    for component in src/components/*.html; do
        component_name=$(basename "$component" .html)
        component_content=$(cat "$component")
        page_content="${page_content/<--$component_name-->/$component_content}"
    done

    echo "$page_content" > "gen/$page_name"

done

echo "Generation complete"
