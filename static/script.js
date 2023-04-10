function printToConsole() {
    username = document.getElementById("username").value
    password = document.getElementById("password").value

    console.log(username + " " + password)
}

function getStudentClasses() {
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

function getTeacherClasses() {
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
          classname = data[i].name;
        table += "<tr><td onclick='seeGrades(classname)'>" + classname + "</td>";
        table += "<td>" + data[i].instructor + "</td>";
        table += "<td>" + data[i].time + "</td>";
        table += "<td>" + data[i].currentEnrollment + "/" + data[i].maxEnrollment + "</td></tr>";
      }

      document.getElementById("placeholder").innerHTML = table;
    };
    document.getElementById("header").innerHTML = "Your Courses"
    xhttp.send();
}

function allClasses() {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://localhost:5000/classes");
    xhttp.onload = function() {
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
        if (data[i].currentEnrollment == data[i].maxEnrollment){
            table += "<td>" + "Not available" + "</td></tr>";
        }
        else{
            table += "<td>" + "Add Class" + "</td></tr>"
        }
      }

      document.getElementById("placeholder").innerHTML = table;
    };
    xhttp.send();
}

function seeGrades(course) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "http://localhost:5000/classes/" + course);
    xhttp.onload = function() {
      var data = JSON.parse(this.responseText);
      var table = "<table border='1' id='classTable'>";
      table += "<tr><th>Student Name</th>" +
               "<th>Grade</th></tr>";

      for (var i = 0; i < data.length; i++) {
        table += "<tr><td>" + data[i].name + "</td>";
        table += "<td>" + data[i].grade + "</td></tr>";
      }

      document.getElementById("placeholder").innerHTML = table;
    };
    document.getElementById("header").innerHTML = course + "-------Click to return to course list";
    xhttp.send();
}

function editGrades(course, grade, student) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("PUT", "http://localhost:5000/classes/" + course);
    xhttp.setRequestHeader("Content-Type", "application/json");
    const body = {"name": student, "grade": grade};
    xhttp.send(JSON.stringify(body));
    xhttp.onload = function() {
        document.getElementById("placeholder").innerHTML = "The grade has been edited";
    };
}

function deleteGrades(course, student) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("DELETE", "http://localhost:5000/classes/" + course);
    xhttp.onload = function() {
      var data = JSON.parse(this.responseText);
      var table = "<table border='1' id='classTable'>";
      table += "<tr><th>Student Name</th>" +
               "<th>Grade</th></tr>";

      for (var i = 0; i < data.length; i++) {
        table += "<tr><td>" + data[i].name + "</td>";
        table += "<td>" + data[i].grade + "</td></tr>";
      }

      document.getElementById("placeholder").innerHTML = table;
    };
    xhttp.send();
}