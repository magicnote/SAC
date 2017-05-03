#### Sublimetext 智能提示 研究

该项目的目的是:研究在Sublimetext上实现IDE的代码智能提示的可能性。  

##### 已解决问题:  
1. Sublimetext 特殊符号 如`$`,`-`,`>`的自动完成匹配问题  
参见Sublimetext的`word_separators`设置。  
2. 类的查找(类文件定位)  
使用composer实现(后续研究仅针对composer, 放弃非composer项目)。  
3. 类的解析(方法 常量 属性)  
参见PHP的`ReflectionClass`类。 [see](https://secure.php.net/manual/zh/class.reflectionclass.php)  
4. 针对单个项目定位`vendor`目录  
目前规则是:匹配当前与当前文件路径相符的第一个项目目录,从该目录下寻找`vendor/autoload.php`  

##### TODO
* 实现非new的方式取得的实例(方法返回的实例)，思路：解析 PHPDoc、PHPDocument等的`@return`注释
* 实现`$this`的匹配

#### License
[MIT license](http://opensource.org/licenses/MIT)