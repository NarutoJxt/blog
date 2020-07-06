function loadMore(page_number, obj, loc, username) {
    obj1 = $(obj);
    obj1.loc = loc;
    obj1.username = username;
    let host = window.location.host;
    url = "http://" + host + "/" + obj1.loc;
    obj1.value = page_number;
    obj1.username = username;
    data = {
        "page": obj1.value,
        "loc": obj1.loc,
    };
    if (username) {
        data["username"] = obj1.username;
    }

    $.get(url, data, function (data, status) {

        if (status == "success") {
            objectList = data["object_list"];
            loc = obj1.loc;
            username = obj1.username;
            for (i = 0; i < objectList.length; i++) {
                temp = objectList[i];
                node = " <li>\n" +
                    "                                        <div class=\"article-left-person\">\n" +
                    "                                            <ul>\n" +
                    "                                                <li>\n" +
                    "                                                    <div class=\"article-header-person\">\n" +
                    "                                                        <a href=" + temp["article_url"] + ">" + temp['title'] + "</a>\n" +
                    "                                                    </div>\n" +
                    "                                                </li>\n" +
                    "                                                <li>\n" +
                    "                                                    <div class=\"article-body-person\">\n" +
                    "                                                        <p>\n" +
                    "                                                         " + temp['body'] + "\n" +
                    "                                                        </p>\n" +
                    "                                                    </div>\n" +
                    "                                                </li>\n" +
                    "                                                <li>\n" +
                    "                                                    <div class=\"article-footer-person\">\n" +
                    "                                                        <ul>\n" +
                    "                                                            <li>\n" +
                    "                                                                <img src=\"" + temp['collections_img'] + "\"\n" +
                    "                                                                     style=\"padding-left: 0\">\n" +
                    "                                                                <span>" + temp['collection_count'] + "</span>\n" +
                    "                                                            </li>\n" +
                    "                                                            <li>\n" +
                    "                                                                <img src=\"" + temp['thumb_up_img'] + "\">" + temp['thump_up_counts'] +
                    "                                                            </li>\n" +
                    "                                                            <li>\n" +
                    "                                                                <img src=\"" + temp['comment_img'] + "\">\n" +
                    "                                                                <span>" + temp['comment_counts'] + "</span>\n" +
                    "                                                            </li>\n" +
                    "                                                        </ul>\n" +
                    "                                                    </div>\n" +
                    "                                                </li>\n" +
                    "                                            </ul>\n" +
                    "                                        </div>\n";
                if (temp["img_url"]) {
                    node += "                                        <div class=\"article-right-person\">\n" +
                        "                                                <img src=\"" + temp["img_url"] + "\" style=\"max-width: 250px\"\n" +
                        "                                                     width=\"250px\"/>\n" +
                        "                                        </div>\n" +
                        "                                    </li>";
                } else {
                    node += "                                        <div class=\"article-right-person\">\n" +
                        "                                        </div>\n" +
                        "                                    </li>";
                }

                obj1.parent().before(node);
            }
            let page_has_next = data["page_has_next"];
            if (page_has_next) {
                obj1.value = obj1.value + 1;
                obj1.attr("onclick", "loadMore(obj1.value,obj1,obj1.loc,obj1.username)");
            } else {
                obj1.attr("disabled", "disabled");
                obj1.css("background-color", "lightgrey");
            }
        }
    })
}