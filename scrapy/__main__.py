from scrapy.download import *

if __name__ == '__main__':
    main_class = list(get_main_class('treeZhiBiao_1_ul'))
    for _class in main_class:
        _id, name = _class
        print(_id, name)
        make_dir(name)
        with Chrome() as c:
            driver = c.driver
            recursion_download(driver, _id)
