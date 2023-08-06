/**
 * Created by bee on 17/11/3.
 */
function QueryString() {
    var name, value, i;
    var str = location.search;
    var num = str.indexOf("?");
    str = str.substr(num + 1);
    var arrtmp = str.split("&");
    for (i = 0; i < arrtmp.length; i++) {
        num = arrtmp[i].indexOf("=");
        if (num > 0) {
            name = arrtmp[i].substring(0, num);
            value = arrtmp[i].substr(num + 1);
            this[name] = value;
        }
    }
}

//点击了分页列表页下面的页数按钮
function clickListPage(page) {
    var url = getRequestUrl(location.pathname, "page", page);
    window.location.href = url;
}

function getRequestUrl(path, key, value) {
    var url = "";
    var str = location.search;

    var Request = new QueryString();
    var num = str.indexOf("?");
    str = str.substr(num + 1);
    var arrtmp = [];
    if (str) {
        arrtmp = str.split("&");
    }
    var a = Request[key];

    if (a) {
        for (i = 0; i < arrtmp.length; i++) {
            num = arrtmp[i].indexOf(key);
            if (num > -1) {
                arrtmp.splice(i, 1);
                break;
            }
        }
    }
    arrtmp.push(key + "=" + value);
    url = arrtmp.join("&");
    url = path + "?" + url;
    return url
}