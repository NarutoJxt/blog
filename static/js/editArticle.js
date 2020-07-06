
function edit(dom) {
    var article = dom.parentNode.parentNode.parentNode.parentNode;
    var prevAll = article.previousSibling.previousSibling.previousSibling.previousSibling;
    var title = prevAll.childNodes[1].textContent;
    title.replace(/(^\s*)|(\s*$)/g, "");
    window.location.href = "http://127.0.0.1:8000/updateArticle/?title="+title+"&type=update";

}