# Use the official Node.js image as the base image
FROM node:18-alpine

# Set the working directory inside the container
WORKDIR /usr/src/app

# Copy package.json and yarn.lock files
# COPY package.json yarn.lock ./

# Copy the entire project to the working directory
COPY . .

# Install dependencies using Yarn
RUN yarn install

# Set environment variables if needed
ENV PORT=3002

# Expose the port your app will run on
EXPOSE 3002

# Command to run the application
CMD ["yarn", "workspace", "orb", "dev"]
