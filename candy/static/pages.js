$(document).ready(function () {
  $("#imgStar1").click(function () {
    StarOn("imgStar", 1);
  });

  $("#imgStar2").click(function () {
    StarOn("imgStar", 2);
  });

  $("#imgStar3").click(function () {
    StarOn("imgStar", 3);
  });
});

function StarOn(label, cnt) {
  $("#" + label + "Count").val(cnt);

  for (var i = 1; i < 6; i++) {
    if (i <= cnt) {
      $("#" + label + i).attr("src", "starOn.png");
    } else {
      $("#" + label + i).attr("src", "starOff.png");
    }
  }
}
