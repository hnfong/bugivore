$(function() {
  $("form.observe").dirty_form();
});

$(function() {
  window.onbeforeunload = function() {
    if (eval("$\(\".changed\"\).length > 0")) {
      return "You have unsaved edits.";
    }
  }
});
