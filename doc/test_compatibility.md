**注意本文档写得相当草略，需要更进一步的完善**

注意到大多数的兼容性测试的差异仅仅是WebDriver的不同，所以只需要把WebDriver构造的这部分逻辑抽离出来就行了。

显然，每个webdriver都应该有自己的有一套testcase类，因为webdriver是在testcase类被建立的时候被构造的，这是为了高效。故而我们需要考虑为每个webdriver生成一套testcase类。这里开始就用到了相当多的python的trick了。

# 思路
* 准备一套实际的测试逻辑的测试类，也就是现在的test/front/template下的那些类，他们都是实际的测试类，但他们一个都不能跑，因为我们在他们共通的基类FrontBasicTC中挖了一个空，initDriver。
* 准备不同浏览器所用的initDriver函数，也就是test/front/driver_tcfactor.py中的。我们称这类函数为TCFactor，因为他们会被插入到TC中，从而影响到Testcase(TC)的实际执行，相当于是TC的影响因子。
* 递归地访问FrontBasicTC的子类，对每个子类，构造一个继承自它的新类，然后将TCFactor添加为新类的属性。也就是让新类具有initDriver这个属性，然后这个属性的值为TCFactor。
* 用一个字典存放上一步生成的新类。覆写test_factory模块的__dir__和__getattr__方法，返回新类的名字和类对象，使得从unittest runner那边看来，上一步产生的新类就是test_factory本来就有的类。

# 注意
* 注意到我们需要访问FrontBasicTC的所有子类，我们使用的是__subclasses__方法，若一个py文件没有被执行过(也就是import过)的话，那么该方法就不会识别到该py文件中的子类。所以我们需要在test_factory.py的一开始就将template下的所有模块都import进来。为此我们将template作为一个包，然后在它的__init__.py文件中添加了__all__方法，用于`from template import *`。

# 简而言之
要添加浏览器的话就直接点开driver_tcfactor.py，然后在里面追加一个类方法，方法内部初始化了driver。之后test_factory就会自动识别到，然后为这个类方法按照template下的模块，生成一套它专属的Testcase.