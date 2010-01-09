$(document).ready(function() {
  $("form.observe").dirty_form();

  $("form.observe").submit(function() {
    jQuery(this).find(".changed").removeClass("changed");
    return true;
  })

  window.onbeforeunload = function() {
    if (eval("$\(\".changed\"\).length > 0")) {
      return "You have unsaved edits.";
    }
  }
});
