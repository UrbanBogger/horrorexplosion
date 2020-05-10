var suggestion_url = "/reviews/film-rev-suggestions/";

window.addEventListener("scroll", function(e) {
    var percent_of_doc_body = Math.round((17 / 100) * document.body.offsetHeight);
    var scroll_trigger =  document.body.offsetHeight - percent_of_doc_body;

    if (Math.round(window.innerHeight + document.documentElement.scrollTop) >= scroll_trigger) {
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
            // send the POST request
            var xmlhttp = new XMLHttpRequest();
            xmlhttp.open("POST", suggestion_url, true);
            xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xmlhttp.setRequestHeader("X-CSRFToken", window.CSRF_TOKEN);

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
            xmlhttp.send("title=" + film_title + "&year=" + release_year);
        }
    }
}, false);