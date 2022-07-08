function movePage(html) {
    let currentUrl = window.location.href;
    let lastIndex = currentUrl.lastIndexOf('/');
    window.location.href = currentUrl.substring(0, lastIndex) + '/' + html;
}

function getParameterByName(name) {
    name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
    var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"), results = regex.exec(location.search);
    return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
}