function printToConsole() {
    username = document.getElementById("username").value
    password = document.getElementById("password").value

    console.log(username + " " + password)
}

function getClasses() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://localhost:5000/class");
    xhttp.onload = function() {
      var data = JSON.parse(this.responseText);
      var table = "<table border='1' id='classTable'>";
      table += "<tr><th>Name</th>" +
               "<th>Instructor</th>" +
               "<th>Time</th>" +
               "<th>Students Enrollment</th></tr>";

      for (var i = 0; i < data.length; i++) {
        table += "<tr><td>" + data[i].name + "</td>";
        table += "<td>" + data[i].instructor + "</td>";
        table += "<td>" + data[i].time + "</td>";
        table += "<td>" + data[i].currentEnrollment + "/" + data[i].maxEnrollment + "</td></tr>";
      }

      document.getElementById("placeholder").innerHTML = table;
    };
    xhttp.send();
}

function allCourses() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://localhost:5000/classes");
    xhttp.onload = function() {
      var data = JSON.parse(this.responseText);
      var table = "<table border='1' id='classTable'>";
      table += "<tr><th>Name</th>" +
               "<th>Instructor</th>" +
               "<th>Time</th>" +
               "<th>Students Enrollment</th></tr>";

      for (var i = 0; i < data.length; i++) {
        table += "<tr><td>" + data[i].name + "</td>";
        table += "<td>" + data[i].instructor + "</td>";
        table += "<td>" + data[i].time + "</td>";
        table += "<td>" + data[i].currentEnrollment + "/" + data[i].maxEnrollment + "</td></tr>";
      }

      document.getElementById("placeholder").innerHTML = table;
    };
    xhttp.send();
}