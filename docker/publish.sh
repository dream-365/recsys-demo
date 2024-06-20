REGION="cn-hangzhou"
USER_NAME=""
NAME_SPACE=""
IMG_ID=""
IMAGE_NAME="flask"
IMAGE_TAG="latest"

docker login --username=$USER_NAME registry.$REGION.aliyuncs.com
docker tag $IMG_ID registry.$REGION.aliyuncs.com/$NAME_SPACE/$IMAGE_NAME:$IMAGE_TAG
docker push registry.$REGION.aliyuncs.com/$NAME_SPACE/$IMAGE_NAME:$IMAGE_TAG