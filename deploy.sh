while getopts ":s:m:h:" opt; do
    case ${opt} in
        s )
            SCALE=$OPTARG
            ;;
        m )
            MASTER=$OPTARG
            ;;
        h )
            HOSTNAME=$OPTARG
            ;;
        \? )
            echo "Invalid option: $OPTARG" 1>&2
            ;;
    esac
done

# Generates docker-compose.yml
python generate_compose_file.py --scale $SCALE --master $MASTER --hostname $HOSTNAME || exit 1
docker-compose up --build -d

timeout=60
i=0
while true; do
    ACCEPTED=$(docker exec $MASTER salt-key --list=accepted | grep -v Accepted)
    if [[ ! -z "$ACCEPTED" ]]; then
        break
    fi

    i=$((i+1))
    if [ "$i" -ge "$timeout" ]; then
        echo "ERROR: Failed to accept keys before timeout ${timeout}!"
        exit 1
    fi
    docker exec $MASTER salt-key -A -y
    sleep 1
done