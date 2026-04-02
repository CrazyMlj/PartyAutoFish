import cv2
import os

template_folder_path = os.path.join('.', 'resources')


def convert_to_grayscale(filename):
    global template_folder_path
    if filename is not None:
        file_path = os.path.join(template_folder_path, filename)
        try:
            img_arr = cv2.imread(file_path)
            gray_img = cv2.cvtColor(img_arr, cv2.COLOR_RGBA2GRAY)
            cv2.imwrite(template_folder_path + "\\" + filename.split('.')[0] + "_grayscale.png", gray_img)
        except Exception as e:
            print('错误：转换失败 - ' + str(e))



if __name__ == '__main__':
    # convert_to_grayscale("bucket_full.png")
    # convert_to_grayscale("bucket_empty.png")
    # convert_to_grayscale("bucket_opened.png")
    # convert_to_grayscale("bucket_48.png")
    # convert_to_grayscale("no_bait.png")
    convert_to_grayscale("resources/templates/skip.png")

    # time.sleep(3)
    # # global_config.scr = mss.mss()
    # # print(bucket_48_matched())
    # # x_y_base = (1245, 675, 'c')
    # global_config.load_parameters()
    # global_config.set_scr(mss.mss())
    # # print(scale_point_anchored(*x_y_base))
    #
    # # print(is_color_similar_rgb((250, 198, 59), (250, 196, 58)))
    #
    # png_template.load_templates()
    # bait_match_val()

