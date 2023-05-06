function follow_author(butt, reload = null) {
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
    if (butt.dataset.reload?.toLowerCase?.() === 'true')
      document.location.reload();
    else {
      var follow_buttons = document.getElementsByClassName("follow_button");
      for (let i = 0; i < follow_buttons.length; i++) {
        if (follow_buttons[i].dataset.author == author) {
          let button = follow_buttons[i];
          if (response["now_following"]) {
            button.innerHTML = "Following";
            button.dataset.following = true;
          } else {
            button.innerHTML = "Follow";
            button.dataset.following = false;
          }
        }
      }
    }
  });
}

function ratePost(butt) {
  var selected = butt.dataset.selected?.toLowerCase?.() === 'true';
  var value = butt.dataset.value;
  var id = butt.dataset.id;
  var desire = selected ? 0 : value; // if voted, undo vote; if not voted, vote for the value

  fetch("/posts/" + id + "/rating/" + desire, {
    method: "POST"
  }).then((response) => response.json()).then((response) => {
    let newRating = response["rating"];
    let up = butt.parentNode.children[0];
    let down = butt.parentNode.children[1];
    let oldRating = 0;
    if (up.dataset.selected?.toLowerCase?.() === 'true') {
      oldRating = 1;
    }
    else if (down.dataset.selected?.toLowerCase?.() === 'true') {
      oldRating = 2;
    }
    up.classList.remove("highlight");
    down.classList.remove("highlight");
    up.dataset.selected = down.dataset.selected = false;

    if (newRating == 0) {
      if (oldRating == 1) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) - 1;
      } else if (oldRating == 2) {
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) - 1;
      }
    }
    if (newRating == 1) {
      up.classList.add("highlight");
      up.dataset.selected = true;
      if (oldRating == 0) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) + 1;
      } else if (oldRating == 2) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) + 1;
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) - 1;
      }
    } else if (newRating == 2) {
      down.classList.add("highlight");
      down.dataset.selected = true;
      if (oldRating == 0) {
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) + 1;
      } else if (oldRating == 1) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) - 1;
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) + 1;
      }
    }
  });
}


function rateComment(butt) {
  var selected = butt.dataset.selected?.toLowerCase?.() === 'true';
  var value = butt.dataset.value;
  var id = butt.dataset.id;
  var desire = selected ? 0 : value; // if voted, undo vote; if not voted, vote for the value

  fetch("/comments/" + id + "/rating/" + desire, {
    method: "POST"
  }).then((response) => response.json()).then((response) => {
    let newRating = response["rating"];
    let up = butt.parentNode.children[0];
    let down = butt.parentNode.children[1];
    let oldRating = 0;
    if (up.dataset.selected?.toLowerCase?.() === 'true') {
      oldRating = 1;
    }
    else if (down.dataset.selected?.toLowerCase?.() === 'true') {
      oldRating = 2;
    }

    up.classList.remove("highlight");
    down.classList.remove("highlight");
    up.dataset.selected = down.dataset.selected = false;

    if (newRating == 0) {
      if (oldRating == 1) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) - 1;
      } else if (oldRating == 2) {
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) - 1;
      }
    }
    if (newRating == 1) {
      up.classList.add("highlight");
      up.dataset.selected = true;
      if (oldRating == 0) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) + 1;
      } else if (oldRating == 2) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) + 1;
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) - 1;
      }
    } else if (newRating == 2) {
      down.classList.add("highlight");
      down.dataset.selected = true;
      if (oldRating == 0) {
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) + 1;
      } else if (oldRating == 1) {
        up.children[1].innerHTML = parseInt(up.children[1].innerHTML) - 1;
        down.children[0].innerHTML = parseInt(down.children[0].innerHTML) + 1;
      }
    }
  });
}