# Sudoku
本项目包含数独的求解，地图数据集的爬取，以及计算生成唯一解的数独地图

(大晚上好像github被墙，明天传

1.数据集的爬取模块——spider

网址：http://www.llang.net/sudoku/type0.html

采集方法:selnium webdriver爬虫

网站对爬虫基本没有限制，采集比较容易

2.做题模块——parser

测试了一千左右的不完全标准地图样本，大概通过率70%左右

猜想哪里还有bug

3.出题模块——map_generator

由于做题模块的通过率不是极高，出题模块测试起来也没有意义，待2完善后再说
