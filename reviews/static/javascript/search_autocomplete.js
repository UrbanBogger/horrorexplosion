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
       document.getElementById("search-category").setAttribute("value", search_choice);
        }
    });

var delayTimer;
function doSearch(search_txt, search_category) {
    if (!search_txt || search_txt.length === 0) {
        return;
    }

    if (document.getElementById("searching-div")) {
        var element = document.getElementById("searching-div");
        element.parentNode.removeChild(element);
    }
    removeSearchResultDiv();
    // create the search result DIV
    var search_result_div = document.createElement("div");
    search_result_div.setAttribute("id", "container");
    search_result_div.setAttribute("class", "col-md-9 col-md-offset-1 col-xs-10 col-xs-offset-1");
    search_result_div.setAttribute("style", "position:absolute;z-index:1500;");
    // add the search result DIV below the search input box
    var parent_div = document.getElementById("search-form-input-group").parentNode;
    var before_div = document.getElementById("search-form-input-group");
    parent_div.insertBefore(search_result_div, before_div.nextSibling);
    var searching_div = document.createElement("div");
    searching_div.setAttribute("id", "searching-div");
    searching_div.setAttribute("class", "col-md-6 col-md-offset-1 col-xs-8 col-xs-offset-1");
    searching_div.setAttribute("style", "position:absolute;z-index:1500;background-color:white;border-style:solid;text-align:center;height:50px;vertical-align:middle;line-height:40px;");
    var parent_div = document.getElementById("container").parentNode;
    var before_div = document.getElementById("container");

    if (document.getElementById("searching-div")) {
        var element = document.getElementById("searching-div");
        element.parentNode.removeChild(element);
    }

    parent_div.insertBefore(searching_div, before_div.nextSibling);
    var s_div = document.getElementById("searching-div");
    var searching_txt = document.createElement("P");
    searching_txt.setAttribute("class", "searching");
    var dot_span_one = document.createElement("SPAN");
    var dot_one = document.createTextNode(".");
    dot_span_one.appendChild(dot_one);
    var dot_span_two = document.createElement("SPAN");
    var dot_two = document.createTextNode(".");
    dot_span_two.appendChild(dot_two);
    var dot_span_three = document.createElement("SPAN");
    var dot_three = document.createTextNode(".");
    dot_span_three.appendChild(dot_three);

    var search_msg = document.createTextNode("Searching");
    searching_txt.appendChild(search_msg);
    searching_txt.appendChild(dot_span_one);
    searching_txt.appendChild(dot_span_two);
    searching_txt.appendChild(dot_span_three);

    s_div.appendChild(searching_txt);

    clearTimeout(delayTimer);
    delayTimer = setTimeout(function() {
        var xmlhttp = new XMLHttpRequest();
        var url_request = url + "?q=" + search_txt + "&sc=" + search_category
        xmlhttp.open("GET", url_request, true);
        xmlhttp.setRequestHeader('X-Requested-With', 'XMLHttpRequest');

        xmlhttp.onreadystatechange = function() {
            if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                var status = xmlhttp.status;
                if (status === 0 || (status >= 200 && status < 400)) {
                // The request has been completed successfully
                var json_resp = JSON.parse(xmlhttp.responseText);
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
    if (e.which === 37|| e.which === 38 || e.which === 39 || e.which === 40 || e.which === 13) {
        return;
    }

    user_input = document.getElementById("user-search").value;
    if (/^\s*$/.test(user_input)) {
        removeSearchResultDiv();
    }
    else {
        search_category = document.getElementById("search_concept").className;
        doSearch(user_input, search_category);
    }
});

function displaySearchResults(search_results) {
    var element = document.getElementById("searching-div");
    element.parentNode.removeChild(element);

    if (document.getElementById("container")) {
        document.getElementById("container").innerHTML += search_results;
    }
}

function removeSearchResultDiv() {
   // remove the search result div if it exists
     if (document.getElementById("container")) {
         element = document.getElementById("container");
         element.parentNode.removeChild(element);
     }
}

const picked_li_color = "#C8C8C8";
const picked_li_substr = "rgb";
const default_li_color = "white";
document.addEventListener("keydown", function(e) {

        if (document.getElementById("search-list")) {
            var result_list = document.getElementById("search-list").getElementsByTagName("li");
            var nr_of_search_results = document.getElementById("search-list").getElementsByTagName("li").length;

            if (e.which === 40) {
                var current_index = 0;

                for (index = 0; index < nr_of_search_results; index++) {
                    if (result_list[index].style["background-color"].indexOf(picked_li_substr) !== -1) {
                        current_index = index+1;
                    }
                }

                if (current_index !== 0 && current_index <= nr_of_search_results-1) {
                    next_li = result_list[current_index];
                    next_li.style.setProperty("background-color", picked_li_color);
                    previous_li = result_list[current_index-1];
                    previous_li.style.setProperty("background-color", default_li_color);
                } else if (current_index === 0){
                    result_list[0].style.setProperty("background-color", picked_li_color);
                } else if (current_index > nr_of_search_results-1) {
                    result_list[nr_of_search_results-1].style.setProperty("background-color", default_li_color);
                }
            }

            if (e.which === 38) {
                var up_index = nr_of_search_results-1;

                for (index = 0; index < nr_of_search_results; index++) {
                    if (result_list[index].style["background-color"].indexOf(picked_li_substr) !== -1) {
                        up_index = index-1;
                    }
                }

                if (up_index !== nr_of_search_results-1 && up_index >= 0) {
                    previous_li = result_list[up_index];
                    previous_li.style.setProperty("background-color", picked_li_color);
                    previous_li = result_list[up_index+1];
                    previous_li.style.setProperty("background-color", default_li_color);
                } else if (up_index === nr_of_search_results-1){
                    result_list[up_index].style.setProperty("background-color", picked_li_color);
                } else if (up_index < 0) {
                    result_list[0].style.setProperty("background-color", default_li_color);
                }
            }

            if (e.which === 13){
                e.preventDefault();
                var chosen_li = null;
                for (index = 0; index < nr_of_search_results; index++) {
                    if (result_list[index].style["background-color"].indexOf(picked_li_substr) !== -1) {
                        chosen_li = result_list[index];
                    }
                }

                if (chosen_li){
                    elements = chosen_li.getElementsByTagName("A");
                    link = elements[0].href;
                    window.location.href = link;
                } else {
                    document.getElementById("search-submit").click();
                }
            }
        }
    }, false);