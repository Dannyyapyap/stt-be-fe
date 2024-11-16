#!/bin/bash

# Install npm dependencies
npm install

# Install shadcn components only uncomment if there are errors showing missing packages from shadcn
# components=("accordion" "button" "input" "pagination")
# for component in "${components[@]}"; do
#     npx shadcn@latest add "$component" --yes
# done

# Create .env.local in current directory
cat > .env.local << EOL
NEXT_PUBLIC_API_ENDPOINT=http://localhost:8020
EOL

echo "Setup complete!"