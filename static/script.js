function getUserPosts(username) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/postsby/" + username);
  xhttp.onload = function () {
    var data = JSON.parse(this.responseText);
    table = "<table border='1' id='classTable'>";

    for (var i = 0; i < data.length; i++) {
      table += "<tr><th>" + data[i].title + " -- Post ID: " + data[i].id + "</th></tr>";
      table += "<tr><td>" + data[i].body + "</td></tr>";
      table += "<tr><td>" + "likes - " + data[i].likes + "  dislikes - " + data[i].dislikes + "  comments - " + data[i].comments + "</td></tr>";
      table += "<tr class='blank'><td class='blank'></td></tr>";
    }
    document.getElementById("posts-container").innerHTML = table;
  };
  xhttp.send();
}

function getFollowedPosts() {
  var x = 0;
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/followed");
  xhttp.onload = function () {
    var data = JSON.parse(this.responseText);
    table = "<table border='1' id='classTable'>";

    for (var i = 0; i < data.length; i++) {
      table += "<tr><th>" + data[i].title + " -- Poster: " + data[i].poster + " -- Post ID: " + data[i].id + "</th></tr>";
      table += "<tr><td>" + data[i].body + "</td></tr>";
      if (data[i].rating) {
        x = userPostRating(data[i].id);
        if (x == "1") {
          table += "<tr><td><button class=\"button button1active\" onclick='removeLike(\"" + data[i].id + "\")'>" + "Like " + data[i].likes + "</button>";
          table += "<button class=\"button button2\" onclick='changetoDislike(\"" + data[i].id + "\")'>" + "Dislike " + data[i].dislikes + "</button>";
        } else if (x == "2") {
          table += "<tr><td><button class=\"button button1\" onclick='changetoLike(\"" + data[i].id + "\")'>" + "Like " + data[i].likes + "</button>";
          table += "<button class=\"button button2active\" onclick='removeDislike(\"" + data[i].id + "\")'>" + "Dislike " + data[i].dislikes + "</button>";
        }
      } else {
        table += "<tr><td><button class=\"button button1\" onclick='addPostRating(" + data[i].id + ", 1)'>" + "Like " + data[i].likes + "</button>";
        table += "<button class=\"button button2\" onclick='addPostRating(" + data[i].id + ", 2)'>" + "Dislike " + data[i].dislikes + "</button>";
      }

      table += "<button onclick='seeComments(\"" + data[i].id + "\")'>" + "See Comments " + data[i].comments + "</button></td></tr>"
      table += "<tr class='blank'><td class='blank'></td></tr>";
    }
    document.getElementById("posts-container").innerHTML = table;
    document.getElementById("comments-container").innerHTML = "";
    document.getElementById("header1").classList.add("active");
    document.getElementById("header2").classList.remove("active");
  };
  xhttp.send();
}


function getAllPosts() {
  var x = 0;
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/allposts");
  xhttp.onload = function () {
    var data = JSON.parse(this.responseText);
    table = "<table border='1' id='classTable'>";

    for (var i = 0; i < data.length; i++) {
      table += "<tr><th>" + data[i].title + " -- Poster: " + data[i].poster + " -- Post ID: " + data[i].id + "</th></tr>";
      table += "<tr><td>" + data[i].body + "</td></tr>";
      if (data[i].rating) {
        x = userPostRating(data[i].id);
        if (x == "1") {
          table += "<tr><td><button class=\"button button1active\" onclick='removeLike(\"" + data[i].id + "\")'>" + "Like " + data[i].likes + "</button>";
          table += "<button class=\"button button2\" onclick='changetoDislike(\"" + data[i].id + "\")'>" + "Dislike " + data[i].dislikes + "</button>";
        } else if (x == "2") {
          table += "<tr><td><button class=\"button button1\" onclick='changetoLike(\"" + data[i].id + "\")'>" + "Like " + data[i].likes + "</button>";
          table += "<button class=\"button button2active\" onclick='removeDislike(\"" + data[i].id + "\")'>" + "Dislike " + data[i].dislikes + "</button>";
        }
      } else {
        table += "<tr><td><button class=\"button button1\" onclick='addPostRating(" + data[i].id + ", 1)'>" + "Like " + data[i].likes + "</button>";
        table += "<button class=\"button button2\" onclick='addPostRating(" + data[i].id + ", 2)'>" + "Dislike " + data[i].dislikes + "</button>";
      }
      table += "<a href='/page/" + data[i].id + "'>See Comments</a></td></tr>";
      // table += "<button onclick='seeComments(\"" + data[i].id + "\")'>" + "See Comments " + data[i].comments + "</button></td></tr>"
      table += "<tr class='blank'><td class='blank'></td></tr>";
    }
    document.getElementById("posts-container").innerHTML = table;
    document.getElementById("comments-container").innerHTML = "";
    document.getElementById("header1").classList.remove("active");
    document.getElementById("header2").classList.add("active");
  };
  xhttp.send();
}

function getPostbyID(postID) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/posts/" + postID);
  xhttp.onload = function () {
    var data = JSON.parse(this.responseText);
    table = "<table border='1' id='classTable'>";

    for (var i = 0; i < data.length; i++) {
      table += "<tr><th>" + data[i].title + " -- Post ID: " + data[i].id + "</th></tr>";
      table += "<tr><td>" + data[i].body + "</td></tr>";
      if (data[i].rating) {
        if (userPostRating(data[i].id) == 1) {
          table += "<tr><td><button class=\"button button1active\" onclick='removeLike(\"" + data[i].id + ", 1\")'>" + "Like " + data[i].likes + "</button>";
          table += "<button class=\"button button2\" onclick='changetoDislike(\"" + data[i].id + ", 2\")'>" + "Dislike " + data[i].dislikes + "</button>";
        } else {
          table += "<tr><td><button class=\"button button1\" onclick='changetoLike(\"" + data[i].id + "\")'>" + "Like " + data[i].likes + "</button>";
          table += "<button class=\"button button2active\" onclick='removeDislike(\"" + data[i].id + "\")'>" + "Dislike " + data[i].dislikes + "</button>";
        }
      } else {
        table += "<tr><td><button class=\"button button1\" onclick='addPostRating(" + data[i].id + ", 1)'>" + "Like " + data[i].likes + "</button>";
        table += "<button class=\"button button2\" onclick='addPostRating(" + data[i].id + ", 2)'>" + "Dislike " + data[i].dislikes + "</button>";
      }
      table += "<button onclick='addComment(\"" + data[i].id + "\")'>" + "Add Comment </button></td></tr>"
      table += "<tr class='blank'><td class='blank'></td></tr>";
    }
    if (i == 0) {
      //This aint workin for some reason
      document.getElementById("posts-container").innerHTML = "There are currently no comments, will you be the first?";
    } else {
      document.getElementById("posts-container").innerHTML = table;
    }
  };
  xhttp.send();
}

function seeComments(postID) {
  getPostbyID(postID)
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/posts/" + postID + "/comments");
  xhttp.onload = function () {
    var data = JSON.parse(this.responseText);
    table = "<table border='1' id='classTable'>";

    for (var i = 0; i < data.length; i++) {
      table += "<tr><td>" + data[i].body + "</td></tr>";
      table += "<tr><td><button class=\"button button1\" onclick='addCommentRating(" + postID + ", " + data[i].id + ", 1)'>" + "Like " + data[i].likes + "</button>";
      table += "<button class=\"button button2\" onclick='addCommentRating(" + postID + ", " + data[i].id + ", 2)'>" + "Dislike " + data[i].dislikes + "</button></td></tr>";
      table += "<tr class='blank'><td class='blank'></td></tr>";
    }
    document.getElementById("comments-container").innerHTML = table;
  };
  xhttp.send();
}

function userPostRating(postID) {
  var num = 0;
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/posts/" + postID + "/rating");
  xhttp.send();
  xhttp.onload = function () {
    var data = JSON.parse(this.responseText);
    num = data.rating;
    return num;
  };
}

function addPostRating(postID, rating) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/posts/" + postID + "/rating/" + rating);
  xhttp.send();
  xhttp.onload = function () {
    getAllPosts()
  };
}

function deletePostRating(postID) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("DELETE", "/posts/" + postID + "/rating");
  xhttp.onload = function () {
    var response = JSON.parse(this.responseText);
    if (response.success) {
      getAllPosts()
    } else {
      alert(response.message);
    }
  };
  xhttp.send();
}

function editPostRating(postID, rating) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("PUT", "/posts/" + postID + "/rating");
  xhttp.setRequestHeader("Content-Type", "application/json");
  const body = {
    "rating": rating
  };
  xhttp.send(JSON.stringify(body));
  xhttp.onload = function () {
    getAllPosts()
    alert("Rating changed successfully")
  };
}


function addCommentRating(postID, commentID, rating) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/posts/" + postID + "/" + commentID + "/rating/" + rating);
  xhttp.send();
  xhttp.onload = function () {
    getPostbyID(postID)
  };
}

function deleteCommentRating(postID, commentID) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("DELETE", "/posts/" + postID + "/" + commentID + "/rating");
  xhttp.onload = function () {
    var response = JSON.parse(this.responseText);
    if (response.success) {
      getPostbyID(postID)
    } else {
      alert(response.message);
    }
  };
  xhttp.send();
}

function editCommentRating(postID, commentID, rating) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("PUT", "/posts/" + postID + "/" + commentID + "/rating");
  xhttp.setRequestHeader("Content-Type", "application/json");
  const body = {
    "rating": rating
  };
  xhttp.send(JSON.stringify(body));
  xhttp.onload = function () {
    getPostbyID(postID)
    alert("Rating changed successfully")
  };
}



function getStudentClassesAdmin() {
  var table = "<table border='1' id='classTable'>";
  message = "Class dropped"
  table += "<tr><th>Name</th>" +
    "<th>Instructor</th>" +
    "<th>Time</th>" +
    "<th>Students Enrollment</th>" +
    "<th>Drop Class</th></tr>";

  table += "<tr> <td>CSE 1</td>" +
    "<td>Grace</td>" +
    "<td>TR 11:00-11:50 AM</td>" +
    "<td>5/10</td>" +
    "<td><button onclick='displayAlert(message)'>" + "Drop Class" + "</button></td></tr>" +
    "<tr><td>CSE 2</td>" +
    "<td>Bob</td>" +
    "<td>MWF 1:00-2:50 PM</td>" +
    "<td>2/10</td>" +
    "<td><button onclick='displayAlert(message)'>" + "Drop Class" + "</button></td></tr>" +
    "<tr><td>CSE 3</td>" +
    "<td>Joebery</td>" +
    "<td>TW 11:00-11:50 AM</td>" +
    "<td>7/10</td>" +
    "<td><button onclick='displayAlert(message)'>" + "Drop Class" + "</button></td></tr>";

  document.getElementById("placeholder").innerHTML = table;
  document.getElementById("addHeader").classList.remove("active");
  document.getElementById("enrolledHeader").classList.add("active");
}

function displayAlert(message) {
  alert(message);
}

function getTeacherClasses() {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/class");
  xhttp.onload = function () {
    var data = JSON.parse(this.responseText);
    var table = "<table border='1' id='classTable'>";
    table += "<tr><th>Name</th>" +
      "<th>Instructor</th>" +
      "<th>Time</th>" +
      "<th>Students Enrollment</th>" +
      "<th></th></tr>";
    for (var i = 0; i < data.length; i++) {
      table += "<tr><td>" + data[i].name + "</td>";
      table += "<td>" + data[i].instructor + "</td>";
      table += "<td>" + data[i].time + "</td>";
      table += "<td>" + data[i].currentEnrollment + "/" + data[i].maxEnrollment + "</td>";
      table += "<td>" + "<button onclick='seeGrades(\"" + data[i].name + "\")'>" + "View Grades</button></td></tr>";
    }
    document.getElementById("placeholder").innerHTML = table;
  };
  document.getElementById("header").innerHTML = "<a>Your Courses</a>"
  xhttp.send();
}

function getTeacherClassesAdmin() {
  var table = "<table border='1' id='classTable'>";
  message = "See Grades for students in class"
  table += "<tr><th>Name</th>" +
    "<th>Instructor</th>" +
    "<th>Time</th>" +
    "<th>Students Enrollment</th>" +
    "<th></th></tr>";
  table += "<tr> <td>CSE 1</td>" +
    "<td>admin</td>" +
    "<td>TR 11:00-11:50 AM</td>" +
    "<td>5/10</td>" +
    "<td>" + "<button onclick='displayAlert(message)'>" + "View Grades</button></td></tr>" +
    "<tr><td>CSE 2</td>" +
    "<td>admin</td>" +
    "<td>MWF 1:00-2:50 PM</td>" +
    "<td>2/10</td>" +
    "<td>" + "<button onclick='displayAlert(message)'>" + "View Grades</button></td></tr>";
  document.getElementById("placeholder").innerHTML = table;
  document.getElementById("addHeader").classList.add("active");
  document.getElementById("enrolledHeader").classList.remove("active");
}

function allClasses() {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/classes");
  xhttp.onload = function () {
    var data = JSON.parse(this.responseText);
    var table = "<table border='1' id='classTable'>";
    table += "<tr><th>Name</th>" +
      "<th>Instructor</th>" +
      "<th>Time</th>" +
      "<th>Students Enrollment</th>" +
      "<th>Add Class</th></tr>";

    for (var i = 0; i < data.length; i++) {
      table += "<tr><td>" + data[i].name + "</td>";
      table += "<td>" + data[i].instructor + "</td>";
      table += "<td>" + data[i].time + "</td>";
      table += "<td>" + data[i].currentEnrollment + "/" + data[i].maxEnrollment + "</td>";
      if (data[i].enrolled) {
        table += "<td><button onclick='dropCourse(\"" + data[i].name + "\")'>" + "Drop Class" + "</button></td></tr>"
      } else if (data[i].currentEnrollment >= data[i].maxEnrollment) {
        table += "<td>" + "Not available" + "</td></tr>";
      } else {
        table += "<td><button onclick='studentAddClass(\"" + data[i].name + "\")'>" + "Add Class" + "</button></td></tr>"
      }
    }
    document.getElementById("addHeader").classList.add("active");
    document.getElementById("enrolledHeader").classList.remove("active");
    document.getElementById("placeholder").innerHTML = table;
  };
  xhttp.send();
}

function checkEnrollment(course) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/class/" + course);
  xhttp.send();
  return this.responseText;
}

function seeGrades(course) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("GET", "/classes/" + course);
  xhttp.onload = function () {
    var data = JSON.parse(this.responseText);
    var table = "<table border='1' id='classTable'>";
    table += "<tr><th>Student Name</th>" +
      "<th>Grade (click to edit)</th>" +
      "<th></th></tr>";

    for (var i = 0; i < data.length; i++) {
      table += "<tr><td>" + data[i].student + "</td>";
      table += "<td contenteditable='true'>" + data[i].grade + "</td>";
      table += "<td><button id='grade-" + i + "'>Change Grade</button></td></tr>";
    }

    document.getElementById("placeholder").innerHTML = table;

    // Add event listeners to capture changes made by the user
    for (var i = 0; i < data.length; i++) {
      var gradeCell = document.getElementById("grade-" + i);
      gradeCell.addEventListener("click", function (event) {
        var studentName = this.parentNode.parentNode.firstChild.innerHTML;
        var newGrade = this.parentNode.parentNode.childNodes[1].innerHTML;
        editGrades(course, newGrade, studentName);
      });
    }
  };
  document.getElementById("header").innerHTML = "<button class='back-button' onclick=\"getTeacherClasses()\">Back to course list</button><a>" + course + "</a>";
  xhttp.send();
}

function editGrades(course, grade, student) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("PUT", "/classes/" + course);
  xhttp.setRequestHeader("Content-Type", "application/json");
  const body = {
    "name": student,
    "grade": grade
  };
  xhttp.send(JSON.stringify(body));
  xhttp.onload = function () {
    alert("Grade changed successfully")
  };
}

function studentAddClass(course) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("POST", "/classes/" + course);
  xhttp.send();
  xhttp.onload = function () {
    alert(this.responseText);
    allClasses();
  };
}

function dropCourse(course) {
  var xhttp = new XMLHttpRequest();
  xhttp.open("DELETE", "/classes/" + course);
  xhttp.onload = function () {
    var response = JSON.parse(this.responseText);
    if (response.success) {
      getStudentClasses();
      alert("Unenrolled from " + course);
    } else {
      alert(response.message);
    }
  };
  xhttp.send();
}

function follow_author(butt, reload=null) {
  var author = butt.dataset.author;
  var following = butt.dataset.following?.toLowerCase?.() === 'true';
  fetch("/follow/" + butt.dataset.author, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      "now_following": !following
    }),
  }).then((response) => response.json()).then((response) => {
    if(butt.dataset.reload?.toLowerCase?.() === 'true')
      document.location.reload();
    else {
      var follow_buttons = document.getElementsByClassName("follow_button");
      for (let i = 0; i < follow_buttons.length; i++) {
        if (follow_buttons[i].dataset.author == author) {
          let button = follow_buttons[i];
          if (response["now_following"]) {
            button.innerHTML = "Following";
            button.dataset.following = true;
          }
          else {
            button.innerHTML = "Follow";
            button.dataset.following = false;
          }
        }
      }
    }
  });
}