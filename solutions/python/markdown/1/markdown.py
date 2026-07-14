# 导入 Python 的正则表达式模块。
# re 可以用来检查一段文字是否符合某种格式。
import re


# 定义 parse 函数。
# markdown 是传进来的 Markdown 字符串。
# 函数最终返回转换后的 HTML 字符串。
def parse(markdown):

    # 按照换行符 \n，把整个 Markdown 字符串拆成多行。
    #
    # 例如：
    # markdown = "# Title\nhello"
    #
    # 拆分后：
    # lines = ["# Title", "hello"]
    lines = markdown.split('\n')

    # res 用来保存最终生成的 HTML。
    # 开始时是空字符串。
    res = ''

    # in_list 用来记录：
    # 当前是否正在处理一个无序列表。
    #
    # False：当前不在列表中。
    # True：当前正在列表中。
    in_list = False

    # in_list_append 用来记录：
    # 是否需要在当前内容前面补一个 </ul>。
    #
    # 当上一行是列表项、当前行不是列表项时，
    # 需要先关闭列表。
    in_list_append = False

    # 遍历每一行 Markdown。
    #
    # i 每次代表当前正在处理的一行。
    for i in lines:

        # 检查当前行是否是六级标题。
        #
        # 正则：
        # ###### (.*)
        #
        # 表示：
        # 六个 #，后面跟一个空格，
        # 再跟任意内容。
        if re.match('###### (.*)', i) is not None:

            # i[7:] 表示从下标 7 开始截取。
            #
            # "###### " 一共有 7 个字符：
            # 六个 # 加一个空格。
            #
            # 例如：
            # i = "###### hello"
            # i[7:] = "hello"
            #
            # 转换为：
            # <h6>hello</h6>
            i = '<h6>' + i[7:] + '</h6>'

        # 如果不是六级标题，再检查是不是五级标题。
        elif re.match('##### (.*)', i) is not None:

            # 五个 # 加空格，一共 6 个字符。
            # 所以使用 i[6:] 取出标题内容。
            i = '<h5>' + i[6:] + '</h5>'

        # 检查四级标题。
        elif re.match('#### (.*)', i) is not None:

            # 四个 # 加空格，一共 5 个字符。
            i = '<h4>' + i[5:] + '</h4>'

        # 检查三级标题。
        elif re.match('### (.*)', i) is not None:

            # 三个 # 加空格，一共 4 个字符。
            i = '<h3>' + i[4:] + '</h3>'

        # 检查二级标题。
        elif re.match('## (.*)', i) is not None:

            # 两个 # 加空格，一共 3 个字符。
            i = '<h2>' + i[3:] + '</h2>'

        # 检查一级标题。
        elif re.match('# (.*)', i) is not None:

            # 一个 # 加空格，一共 2 个字符。
            i = '<h1>' + i[2:] + '</h1>'

        # 检查当前行是否是无序列表项。
        #
        # r'\* (.*)' 表示：
        # 开头是一个星号 *
        # 后面有一个空格
        # 再后面是任意内容
        #
        # 星号在正则里有特殊含义，
        # 所以需要写成 \*，表示普通星号。
        m = re.match(r'\* (.*)', i)

        # 如果匹配成功，说明当前行是列表项。
        if m:

            # 如果当前还没有进入列表，
            # 说明这是列表的第一项。
            if not in_list:

                # 把列表状态改成 True。
                in_list = True

                # 用来记录当前内容里是否存在粗体。
                is_bold = False

                # 用来记录当前内容里是否存在斜体。
                is_italic = False

                # m.group(1) 取得列表项星号后面的内容。
                #
                # 例如：
                # i = "* apple"
                #
                # m.group(1) = "apple"
                curr = m.group(1)

                # 检查列表内容里是否存在：
                #
                # 前面的内容 __粗体内容__ 后面的内容
                #
                # 三个 (.*) 分别表示：
                # group(1)：粗体前面的内容
                # group(2)：粗体里面的内容
                # group(3)：粗体后面的内容
                m1 = re.match('(.*)__(.*)__(.*)', curr)

                # 如果找到了粗体格式。
                if m1:

                    # 把：
                    # __文字__
                    #
                    # 转换为：
                    # <strong>文字</strong>
                    curr = (
                        m1.group(1)
                        + '<strong>'
                        + m1.group(2)
                        + '</strong>'
                        + m1.group(3)
                    )

                    # 记录发现了粗体。
                    is_bold = True

                # 检查当前内容是否包含斜体：
                #
                # 前面的内容 _斜体内容_ 后面的内容
                m1 = re.match('(.*)_(.*)_(.*)', curr)

                # 如果发现了斜体。
                if m1:

                    # 把：
                    # _文字_
                    #
                    # 转换为：
                    # <em>文字</em>
                    curr = (
                        m1.group(1)
                        + '<em>'
                        + m1.group(2)
                        + '</em>'
                        + m1.group(3)
                    )

                    # 记录发现了斜体。
                    is_italic = True

                # 这是列表的第一项，所以要同时生成：
                #
                # <ul>：打开无序列表
                # <li>：打开列表项
                #
                # 例如：
                # <ul><li>apple</li>
                #
                # 这里暂时没有关闭 </ul>，
                # 因为后面可能还有其他列表项。
                i = '<ul><li>' + curr + '</li>'

            # 如果 in_list 已经是 True，
            # 说明当前不是列表第一项，
            # 而是列表中的后续项目。
            else:

                # 重置粗体状态。
                is_bold = False

                # 重置斜体状态。
                is_italic = False

                # 取出当前列表项的正文。
                curr = m.group(1)

                # 检查是否包含粗体。
                m1 = re.match('(.*)__(.*)__(.*)', curr)

                # 如果包含粗体，只记录状态，
                # 这时还没有真正替换。
                if m1:
                    is_bold = True

                # 再检查是否包含斜体。
                #
                # 注意：这里把原来的 m1 覆盖掉了。
                m1 = re.match('(.*)_(.*)_(.*)', curr)

                # 如果包含斜体，记录状态。
                if m1:
                    is_italic = True

                # 如果之前发现粗体，
                # 尝试把粗体 Markdown 转换成 HTML。
                if is_bold:
                    curr = (
                        m1.group(1)
                        + '<strong>'
                        + m1.group(2)
                        + '</strong>'
                        + m1.group(3)
                    )

                # 如果发现斜体，
                # 把斜体 Markdown 转换成 HTML。
                if is_italic:
                    curr = (
                        m1.group(1)
                        + '<em>'
                        + m1.group(2)
                        + '</em>'
                        + m1.group(3)
                    )

                # 后续列表项不需要再次添加 <ul>，
                # 只需要生成一个新的 <li>。
                i = '<li>' + curr + '</li>'

        # 如果当前行不是列表项。
        else:

            # 如果上一行还在列表中，
            # 说明列表到这里结束了。
            if in_list:

                # 标记稍后需要添加 </ul>。
                in_list_append = True

                # 把列表状态改回 False。
                in_list = False

        # 检查当前的 i 是否已经转换成某种 HTML 块。
        #
        # 匹配以下开头：
        # <h   标题
        # <ul  列表开头
        # <p   段落
        # <li  列表项
        m = re.match('<h|<ul|<p|<li', i)

        # 如果当前内容不是标题、列表或段落，
        # 就把它当作普通段落。
        if not m:

            # 例如：
            # hello
            #
            # 转换为：
            # <p>hello</p>
            i = '<p>' + i + '</p>'

        # 检查当前整行内容是否包含粗体 Markdown。
        #
        # 这一步不仅处理普通段落，
        # 也可能处理标题中的粗体。
        m = re.match('(.*)__(.*)__(.*)', i)

        # 如果发现粗体。
        if m:

            # 转换成 <strong>。
            i = (
                m.group(1)
                + '<strong>'
                + m.group(2)
                + '</strong>'
                + m.group(3)
            )

        # 检查当前整行是否包含斜体 Markdown。
        m = re.match('(.*)_(.*)_(.*)', i)

        # 如果发现斜体。
        if m:

            # 转换成 <em>。
            i = (
                m.group(1)
                + '<em>'
                + m.group(2)
                + '</em>'
                + m.group(3)
            )

        # 如果之前发现列表已经结束。
        if in_list_append:

            # 在当前内容前面加上 </ul>，
            # 关闭上一段列表。
            #
            # 例如当前 i 是：
            # <p>hello</p>
            #
            # 会变成：
            # </ul><p>hello</p>
            i = '</ul>' + i

            # 已经关闭列表，所以重置标记。
            in_list_append = False

        # 把当前处理完成的 HTML，
        # 拼接到最终结果 res 后面。
        res += i

    # 所有行循环结束后，
    # 如果仍然处于列表状态，
    # 说明 Markdown 最后一行就是列表项。
    if in_list:

        # 因为后面已经没有普通行帮助关闭列表，
        # 所以需要手动补上 </ul>。
        res += '</ul>'

    # 返回最终生成的完整 HTML 字符串。
    return res