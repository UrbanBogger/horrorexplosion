var search_choice = "all"
var url = "/reviews/search/";
// locate your element and add the Click Event Listener
document.getElementById("search-options").addEventListener("click",function(e) {
    e.preventDefault();

    if(e.target && e.target.nodeName == "A") {
       document.getElementById("search_concept").innerHTML = e.target.text;
       li_search_id = e.target.parentNode.id;
       document.getElementById("search_concept").className = li_search_id;
       search_choice = document.getElementById("search_concept").className;
       console.log('current search category: ' + search_choice)
       console.log('setting hidden field value')
       document.getElementById("search-category").setAttribute("value", search_choice);
       console.log('The value of the hidden value attribute:' + document.getElementById("search-category").getAttribute("value"));
        }
    });

var delayTimer;
function doSearch(search_txt, search_category) {
    clearTimeout(delayTimer);
    delayTimer = setTimeout(function() {
       // Do the ajax stuff
        console.log('Making the AJAX call!')
        var xmlhttp = new XMLHttpRequest();
        var url_request = url + "?q=" + user_input + "&sc=" + search_category
        console.log('url_request:' + url_request)
        xmlhttp.open("GET", url_request, true);
        xmlhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                var status = xmlhttp.status;
                if (status === 0 || (status >= 200 && status < 400)) {
                // The request has been completed successfully
                //console.log(xmlhttp.responseText);
                var json_resp = JSON.parse(xmlhttp.responseText);
                //console.log('HTML response: ' + json_resp['html_from_view']);
                displaySearchResults(json_resp['html_from_view']);

            } else {
              // Oh no! There has been an error with the request!
                 console.log('ERROR: AJAX request failed!')
            }
            }
        };
        xmlhttp.send();
    }, 1000); // Will do the ajax stuff after 1000 ms, or 1 s
}

document.getElementById("user-search").addEventListener("keyup",function(e) {
    user_input = document.getElementById("user-search").value;
    console.log('usr input: ' + user_input)
    if (/^\s*$/.test(user_input)) {
        console.log('REMOVING DIV');
        removeSearchResultDiv();
    }
    search_category = document.getElementById("search_concept").className;
    console.log('current search category: ' + search_choice)
    if (!/^\s*$/.test(user_input)) {
        doSearch(user_input, search_category);
    }
});

function displaySearchResults(search_results) {
    removeSearchResultDiv();
    // create the search result DIV
    var search_result_div = document.createElement("div");
    search_result_div.setAttribute("id", "container");
    search_result_div.setAttribute("class", "col-xs-10 col-xs-offset-1");
    search_result_div.setAttribute("style", "position: absolute; z-index: 99;");
    // add the search result DIV below the search input box
    var parent_div = document.getElementById("search-form-input-group").parentNode;
    var before_div = document.getElementById("search-form-input-group");
    parent_div.insertBefore(search_result_div, before_div.nextSibling);
    // add results in the form of a list to the search result DIV
    document.getElementById("container").innerHTML += search_results
}

function removeSearchResultDiv() {
   // remove the search result div if it exists
     if (document.getElementById("container")) {
         element = document.getElementById("container");
         element.parentNode.removeChild(element);

     }
}