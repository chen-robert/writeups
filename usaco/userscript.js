$(".submission").submit(function(e) {
  e.preventDefault();
  var formData = new FormData(this);

  $.ajax({
    url: "current/tpcm/submit-solution.php",
    type: "POST",
    data: formData,
    success: function(data) {
      var start = data.indexOf('data-sid="') + 'data-sid="'.length;
      var end = data.indexOf('"', start);
      $("#last-status").data("sid", data.substring(start, end));
      postback();
    },
    cache: false,
    contentType: false,
    processData: false
  });
});

var retries = 100,
  timeout = 1000;

function postback() {
  var sid = $("#last-status").data("sid");
  if (sid == -1) return;
  $.post(
    "current/tpcm/status-update.php",
    { sid: sid },
    update_response,
    "json"
  );
}

function update_response(s) {
  console.log(s);
  if (s != null) {
    $("#last-status img").attr("src", "current/images/medal_none.png");
    if (parseInt(s.cd) <= -8 && s.sc == "status-working") {
      $("#last-status img").attr("src", "current/images/ajax.gif");
    }

    $("#last-status")
      .removeClass()
      .addClass(s.sc);
    $("#last-status p").text(s.sr);

    $("#last-status").data("response-code", parseInt(s.cd));
    $("#last-status .output-data").hide();

    if (s.output != null) {
      $("#last-status .output-data")
        .show()
        .text(s.output);
      if (parseInt($("#last-status").data("response-code")) <= -8) {
        setTimeout(postback, timeout);
      }

      return;
    }

    if (s.jd != null && s.jd.length != 0) {
      $("#trial-information").html(s.jd);
    }
  }

  if (parseInt($("#last-status").data("response-code")) <= -8) {
    setTimeout(postback, timeout);
  }
}

var elem = document.createElement("div");
elem.innerHTML = `
<style>
#injected-submit{
  position: fixed;
  height: 50px;
  width: 50px;
  bottom: 25px;
  right: 25px;
  background-color: #eee;
  border-radius: 50%;
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
</style>
<div id="injected-submit">
+
</div>
`;
document.body.appendChild(elem);
$(elem).click(() => $("form.submission").submit());
