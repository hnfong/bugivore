$(document).ready(function() {
  $("form.dirty_check").dirty_form();

  $("form.dirty_check").submit(function() {
    jQuery(this).find(".changed").removeClass("changed");
    return true;
  })

  window.onbeforeunload = function() {
    if (eval("$\(\".changed\"\).length > 0")) {
      return "You have unsaved edits.";
    }
  }
});
