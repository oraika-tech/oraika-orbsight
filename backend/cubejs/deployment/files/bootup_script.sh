#!/bin/bash
# update system packages
yum update -y
systemctl enable docker
systemctl start docker

mkdir -p /cube/conf/schema

cat <<'EOF' > /cube/conf/cube.js
${cube_js}
EOF

cat <<'EOF' > /cube/conf/schema/${schema_file_name}
${schema_file}
EOF

cat <<'EOF' > /cube/.env
${env_file}
EOF

docker run -d -p 4000:4000 -p 3000:3000 \
  -v /cube/conf:/cube/conf \
  --env-file /cube/.env \
  --restart unless-stopped \
  cubejs/cube:${image_tag}