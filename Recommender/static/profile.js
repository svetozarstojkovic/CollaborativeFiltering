var username;
function init(locUsername) {

    localStorage.setItem("username", locUsername);
    username = locUsername;

    myMovies();
    loadAllMovies()
}

function filter() {
  // Declare variables
  var input, filter, table, tr, td, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("notRatedTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      if (td.innerHTML.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}

function rate(title, rate) {
    console.log(title);
     $.ajax({
        url: '/rate',
        data: { "username" : username,
                "title" : title,
                "rate" : rate },
        type: 'POST',
        success: function(response) {
            console.log(response);
            $('#snackbarDiv').html(response)
            var x = document.getElementById("snackbar")

            // Add the "show" class to DIV
            x.className = "show";

            // After 3 seconds, remove the show class from DIV
            setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);

            myMovies(username, 0)
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function doJaccard() {
    console.log("jaccardClick");
    username = localStorage.getItem("username")
    $("#recommended").html("<div class='loader'></div>")
     $.ajax({
            url: '/jaccard_method',
            data: { "username" : username },
            type: 'POST',
            success: function(response) {
                $("#recommended").html(response)
                $("#recommendedTable").DataTable({
                    "order": [[ 0, "desc" ]]
                } )
            },
            error: function(error) {
                console.log(error);
            }
        });
}

function doCosine() {
    console.log("cosineClick");
    $("#recommended").html("<div class='loader'></div>")
     $.ajax({
            url: '/cosine_method',
            data: { "username" : username },
            type: 'POST',
            success: function(response) {
                $("#recommended").html(response)
                $("#recommendedTable").DataTable({
                    "order": [[ 0, "desc" ]]
                } )
            },
            error: function(error) {
                console.log(error);
            }
        });
}

function doCenteredCosine() {
    console.log("cosineClick");
    $("#recommended").html("<div class='loader'></div>")
     $.ajax({
            url: '/centered_cosine_method',
            data: { "username" : username },
            type: 'POST',
            success: function(response) {
                $("#recommended").html(response)
                $("#recommendedTable").DataTable({
                    "order": [[ 0, "desc" ]]
                } )
            },
            error: function(error) {
                console.log(error);
            }
        });
}

function doPearson() {
    console.log("pearsonClick");
    $("#recommended").html("<div class='loader'></div>")
     $.ajax({
            url: '/pearson_method',
            data: { "username" : username },
            type: 'POST',
            success: function(response) {
                $("#recommended").html(response)
                $("#recommendedTable").DataTable({
                    "order": [[ 0, "desc" ]]
                } )
            },
            error: function(error) {
                console.log(error);
            }
        });
}


function movieDetails(title) {
    console.log("getDetails");
    $("#movie_details").html("<div class='loader'></div>")
     $.ajax({
            url: '/movie_details',
            data: { "title" : title,
                    "username" : username },
            type: 'POST',
            success: function(response) {
                $("#movie_details").html(response)
            },
            error: function(error) {
                console.log(error);
            }
        });
}

function myMovies() {
    console.log("myMovies");
    $("#rated").html("<div class='loader'></div>");
     $.ajax({
            url: '/my_movies',
            data: { "username" : username },
            type: 'POST',
            success: function(response) {
                $("#rated").html(response);
                $('#ratedMovieTable').DataTable();
            },
            error: function(error) {
                console.log(error);
            }
        });
}

function notRated() {
    console.log("myMovies");
    $("#not_rated").html("<div class='loader'></div>")
     $.ajax({
            url: '/not_rated',
            data: { "username" : username },
            type: 'POST',
            success: function(response) {
                $("#not_rated").html(response);
                $('#notRatedTable').DataTable();
            },
            error: function(error) {
                console.log(error);
            }
        });
}
function loadAllMovies() {
    console.log("loadMovies")
    $("#all_movies").load("../static/all_movies_table.html");
}
