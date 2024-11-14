#!/bin/sh
# Whyness Django Build

BUILD_CONFIG=""
BUILD_BRANCH=$(git branch --list |awk '/^[*]/ {print $2}')
BUILD_IMAGE=""
AWS_IMAGE_NAME="whyness_django"
AWS_REGION=eu-west-1
AWS_APPRUNNER="411955575430.dkr.ecr.eu-west-1.amazonaws.com"
if command -v docker
then
	echo "Starting build"
else
	echo "Docker is not installed"
	#exit 1
fi

if [ -z "$BUILD_BRANCH" ]
then
	echo "Unable to get build version"
	exit 1
else
	if [ "main" = "$BUILD_BRANCH" ]
	then
		echo "Building local development"
		BUILD_CONFIG="LOCAL"
		BUILD_IMAGE="_local"
	elif [ "prod" = "$BUILD_BRANCH" ]
	then
		echo "Building for PRODUCTION"
		BUILD_CONFIG="PROD"
		BUILD_IMAGE=""
	elif [ "stage" = "$BUILD_BRANCH" ]
	then
		echo "Building for DEVELOPMENT"
		BUILD_CONFIG="DEV"
		BUILD_IMAGE="_dev"
	else
		echo "Unknown build version"
		exit 1
	fi
fi
echo "Press Ctrl+c to abort"
sleep 3

if [ $BUILD_CONFIG = "PROD" ]
then
	echo "Building a Production release"
elif [ $BUILD_CONFIG = "DEV" ]
then
	echo "Building a development (staging) release"
else
	echo "Building locally"
fi

# Remove existing containers and images
# Stop all containers
sudo docker container list |awk '!/CONTAINER/ {print $1}' | xargs sudo docker container stop

sudo docker container rm $AWS_IMAGE_NAME$BUILD_IMAGE
sudo docker image rm $AWS_IMAGE_NAME$BUILD_IMAGE

# Build a new image
sudo docker build --tag $AWS_IMAGE_NAME$BUILD_IMAGE .
sudo docker container create -p 80:80 --name $AWS_IMAGE_NAME$BUILD_IMAGE --env-file whyness-env -v "$HOME/.aws/credentials:/root/.aws/credentials:ro" $AWS_IMAGE_NAME$BUILD_IMAGE

sudo docker container start $AWS_IMAGE_NAME$BUILD_IMAGE
sudo docker logs $AWS_IMAGE_NAME$BUILD_IMAGE

if [ $BUILD_CONFIG = "PROD" ] ||  [ $BUILD_CONFIG = "DEV" ]
then
	if ! aws ecr get-login-password --region "$AWS_REGION" | sudo docker login --username AWS --password-stdin "$AWS_APPRUNNER"
	then
		echo "Failed to log in to AWS"
		exit 1
	fi
	if ! sudo docker build -t $AWS_IMAGE_NAME$BUILD_IMAGE .
	then
		echo "Failed to build image"
		exit 1
	fi
	if ! sudo docker tag "$AWS_IMAGE_NAME$BUILD_IMAGE:latest" "$AWS_APPRUNNER/$AWS_IMAGE_NAME$BUILD_IMAGE:latest"
	then
		echo "Failed to tag build image"
		exit 1
	fi
	sudo docker push "$AWS_APPRUNNER/$AWS_IMAGE_NAME$BUILD_IMAGE:latest"
fi
