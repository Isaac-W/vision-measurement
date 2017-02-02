import cv2
import markerfinder as mk

"""
Given known distance between two markers, we can calculate the focal length f using the following:

F = px * D / S  -- where d is pixel size, D is known distance, and S is known size
F = dD * px1 * px2 / (S * abs(px1 - px2))  -- where px1 and px2 are pixel sizes, and dD is known difference in distance

then we compute distance given a pixel size and known size and focal length:

D = F * S / px
"""

def callback(value):
    pass


def setup_trackbars():
    cv2.namedWindow("Trackbars", 0)
    cv2.createTrackbar("Diff (mm)", "Trackbars", 0, 100, callback)
    cv2.createTrackbar("Size (mm)", "Trackbars", 0, 100, callback)


def ftoi_point(point):
    return int(point[0]), int(point[1])


def get_pixel_size(marker):
    return max(marker[1][1][0], marker[1][1][1])


def draw_marker(img, marker):
    e = marker[1]
    p = ftoi_point(e[0])

    cv2.ellipse(img, e, (0, 255, 0), 2)
    cv2.circle(img, p, 2, (255, 0, 0), 2)

    cv2.putText(img, str(p), p, cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 0, 0), 2)
    cv2.putText(img, 'd: ' + str(round(get_pixel_size(marker), 2)), (p[0], p[1] + 20), cv2.FONT_HERSHEY_PLAIN, 1, (255, 0, 0), 2)


def main():
    setup_trackbars()

    g_finder = mk.MarkerFinder(mk.GREEN_COLOR_MIN, mk.GREEN_COLOR_MAX)
    v_finder = mk.MarkerFinder(mk.VIOLET_COLOR_MIN, mk.VIOLET_COLOR_MAX)

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        return

    while True:
        ret, frame = cap.read()
        if ret is False or frame is None:
            break

        output = frame.copy()

        green_matches = g_finder.find_markers(frame, output)
        violet_matches = v_finder.find_markers(frame, output)

        g_marker = green_matches[0] if len(green_matches) else None
        v_marker = violet_matches[0] if len(violet_matches) else None

        # Draw centers and size
        if g_marker:
            draw_marker(output, g_marker)

        if v_marker:
            draw_marker(output, v_marker)

        # Find calculated focal length
        if g_marker and v_marker:
            px1 = get_pixel_size(g_marker)
            px2 = get_pixel_size(v_marker)

            # Get known distance/size
            dD = cv2.getTrackbarPos("Diff (mm)", "Trackbars")
            S = cv2.getTrackbarPos("Size (mm)", "Trackbars")

            if S != 0:
                # Compute focal length
                F = dD * px1 * px2 / (S * abs(px1 - px2))
                cv2.putText(output, 'F = %5.1d' % round(F, 1), (0, 30), cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 255), 2)

        cv2.imshow("Output", output)
        cv2.waitKey(1)

    cap.release()


if __name__ == '__main__':
    main()
