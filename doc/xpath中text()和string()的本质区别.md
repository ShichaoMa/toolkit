[comment]: <> (![](http://www.w3.org/Consortium/Offices/Presentations/XSLT_XPATH/images/xpath.png))
## 使用要点

XML例子：

    
    
    <book>
        <author>Tom <em>John</em> cat</author>
        <pricing>
            <price>20</price>
            <discount>0.8</discount>
        </pricing>
    </book>
    

### text()

经常在XPath表达式的最后看到text()，它仅仅返回所指元素的文本内容。

    
    
    text = $x('book/author/text()')
    

返回的结果是Tom cat，其中的John不属于author直接的节点内容。

### string()

string()函数会得到所指元素的所有节点文本内容，这些文本讲会被拼接成一个字符串。

    
    
    text = $x('book/author/string()')
    

返回的内容是”Tom John cat”

### data()

大多数时候，data()函数和string()函数通用，而且不建议经常使用data()函数，有数据表明，该函数会影响XPath的性能。

    
    
    text = $x('book/pricing/string()')
    

返回的是200.8

    
    
    text = $x('book/pricing/data()')
    

这样将返回分开的20和0.8。

## 总结

text()不是函数，XML结构的细微变化，可能会使得结果与预期不符，应该尽量少用，data()作为特殊用途的函数，可能会出现性能问题，如无特殊需要尽量不用，string()函数可以满足大部分的需求。

text()是一个node test，而string()是一个函数，data()是一个函数且可以保留数据类型。此外，还有点号（.）表示当前节点。


[comment]: <tags> (xpath)
[comment]: <description> (text和string的本质区别)
[comment]: <title> (xpath中text()和string()的本质区别)
[comment]: <author> (夏洛之枫)