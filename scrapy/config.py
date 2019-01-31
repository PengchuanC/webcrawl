import os


# 项目地址
ABS_PATH = os.path.abspath(os.path.dirname(__file__))


# chromedriver.exe文件路径
CHROME_DRIVER = os.path.join(ABS_PATH, 'src/chromedriver.exe')


# files save dir
FILES = os.path.join(ABS_PATH, 'files')

if not os.path.exists(FILES):
    os.mkdir(FILES)
