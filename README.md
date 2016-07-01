# Sudoku
本项目包含数独的求解，地图数据集的爬取，以及计算生成唯一解的数独地图


环境：python 2.7.1


##1.数据集的爬取模块——spider

  - 网址：http://www.llang.net/sudoku/type0.html

  - 采集方法:Selnium + PhantomJS

  - 网站对爬虫基本没有限制，采集比较容易


##2.做题模块——parser

  - 测试了一千左右的不完全标准地图样本，
  - 阶数一上去，会触发bug，通过率非常低，
    ![](http://findmentor-findmentor.stor.sinaapp.com/my_img%2F20160701211810.png)
	
  - 关于阶数，难度，在更新的数据库中加了grade列，便于分级测试
      ![](http://findmentor-findmentor.stor.sinaapp.com/my_img%2FQQ%E6%88%AA%E5%9B%BE20160701220033.png)


##3.出题模块——map_generator

  - 由于做题模块的通过率不是极高，出题模块测试起来也没有意义，待2完善后再说
