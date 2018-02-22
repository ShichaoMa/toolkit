[comment]: <> (![](https://dreamix.eu/blog/wp-content/uploads/2015/03/xpath_logo1-1508x706_c.jpg))
### 选择包含div的a标签

    
    
    '//div[@class="col"]/article[@class="product-col"]/a/div/parent::a'
    或
    '//div[@class="col"]/article[@class="product-col"]/a/div/../../a'
    或
    '//div[@class="col"]/article[@class="product-col"]/a[div]'
    

### 选择包含href属性的标签

    
    
    '//div[@class="col"]/article[@class="product-col"]/a[@href]'
    


[comment]: <tags> (xpath)
[comment]: <description> (比较难的xpath)
[comment]: <title> (xpath相关)
[comment]: <author> (夏洛之枫)