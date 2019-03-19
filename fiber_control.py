import time
import cv2
import json
import threading


path = "../Fiber_test1/swap.txt"
media_dir = 'media/'
off_video = "black.wmv"
config = []


def get_config_from_file():
    try:
        f = open(path, "r")
        from_file = f.read()
        f.close()

        json_content = json.loads(from_file)
    except ValueError:
        print("Parse error")
        default_animation = '{\"animation\": 1,\"animation_name\": \"Widmo\",\"video_name\": \"'
        default_animation += off_video
        default_animation += '\",\"powered\": false}'
        json_content = json.loads(default_animation)

    return json_content


def write_config_to_file(config):
    f = open(path, "w")
    to_write = json.dumps(config, indent=4)
    print(to_write)
    f.write(to_write)
    f.close()


def check_changes_in_config_file():
    while True:
        global config

        try:
            config = get_config_from_file()
        except ValueError:
            print("Can't open swap file")

        time.sleep(0.5)


def choose_animation():
    cv2.namedWindow('window', cv2.WND_PROP_FULLSCREEN)
    cv2.setWindowProperty('window', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    while True:

        global config

        if config["powered"] == False:
            play_animation(media_dir + off_video, cv2)
        else:
            print('Animation name: ' + config["animation_name"])
            play_animation(media_dir + config["video_name"], cv2)


def play_animation(animation_name, cv2):
    try:
        vid = cv2.VideoCapture(animation_name)
        if not vid.isOpened():
            vid = cv2.VideoCapture(off_video)
    except cv2.error as e:
        print("cv2.error:", e)
    except Exception as e:
        print("Exception:", e)

    (major_ver, minor_ver, subminor_ver) = cv2.__version__.split('.')

    # if int(major_ver) < 3:
    #     fps = vid.get(cv2.cv.CV_CAP_PROP_FPS)
    #     print("Frames per second using video.get(cv2.cv.CV_CAP_PROP_FPS): {0}".format(fps))
    # else:
    fps = vid.get(cv2.CAP_PROP_FPS)
    delay = 1000 / fps
    print("Frames per second using video.get(cv2.CAP_PROP_FPS): {0}, Delay between frames: {0}".format(fps).format(delay))

    global config
    previous_config = config

    while True:
        if config != previous_config:
            break

        ret, frame = vid.read()

        if ret:
            cv2.imshow('window', frame)
        else:
            break

        if cv2.waitKey(int(delay)) & 0xFF == ord('q'):
            break

    # cv2.destroyAllWindows()


def start_manager():
    global config
    config = get_config_from_file()

    anim_thred = threading.Thread(target=choose_animation)
    data_swap_thred = threading.Thread(target=check_changes_in_config_file)

    anim_thred.start()
    data_swap_thred.start()

    return 0


start_manager()
