var suggestions_url = "/reviews/film-rev-suggestions/";

window.addEventListener("scroll", function(e) {
    var percent_of_doc_body = Math.round((25 / 100) * document.body.offsetHeight);
    var scroll_trigger =  document.body.offsetHeight - percent_of_doc_body;
    var bodyScrollTop = 0;

    if (document.scrollingElement.scrollTop) {
        bodyScrollTop = Math.max(document.scrollingElement.scrollTop, document.documentElement.scrollTop);
    } else {
        bodyScrollTop = document.documentElement.scrollTop;
    }

    var bodyScrollTop = Math.max(document.scrollingElement.scrollTop, document.documentElement.scrollTop);
    console.log('document.body.offsetHeight: ' + document.body.offsetHeight);
    console.log('window.innerHeight: ' + window.innerHeight);
    console.log('document scrollTop: ' + bodyScrollTop);
    if (Math.round(window.innerHeight + bodyScrollTop) >= scroll_trigger) {
    //if (Math.round(window.innerHeight + document.documentElement.scrollTop) >= scroll_trigger) {
        console.log('TRIGGERING THE REQUEST!!!');
        if (!document.getElementById("suggestions")) {
            // create the suggestions DIV
            var suggestions_div = document.createElement("div");
            suggestions_div.setAttribute("id", "suggestions");
            suggestions_div.setAttribute("class", "container");
            suggestions_div.setAttribute("style", "padding:0px;width:100%;");
            // add the search result DIV below the search input box
            var parent_div = document.getElementById("review-body");
            parent_div.appendChild(suggestions_div);
            film_title = document.getElementsByTagName("H1")[0].getElementsByTagName("A")[0].textContent.trim();
            release_year = document.getElementsByTagName("H2")[0].textContent.match(/(\d{4})/)[0].trim();
            // send the request
            var xmlhttp = new XMLHttpRequest();
            var url_request = suggestions_url + "?title=" + film_title + "&year=" + release_year;
            xmlhttp.open("GET", url_request, true);
            xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");

            xmlhttp.onreadystatechange = function() {
                if (xmlhttp.readyState === XMLHttpRequest.DONE) {
                    var status = xmlhttp.status;

                    if (status === 0 || (status >= 200 && status < 400)) {
                        // The request has been completed successfully
                        var json_resp = JSON.parse(xmlhttp.responseText);
                        var suggested_reviews = json_resp['html_from_view'];

                        if (document.getElementById("suggestions") && suggested_reviews) {
                            document.getElementById("suggestions").innerHTML += suggested_reviews;
                        }
                    } else {
                        // Oh no! There has been an error with the request!
                        console.log('ERROR: AJAX request failed!')
                    }
                }
            };
            xmlhttp.send();
        }
    }
}, false);