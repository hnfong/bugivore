$(document).ready(function() {
  $("form:not(.allow_dirty)").dirty_form();

  $("form:not(.allow_dirty)").submit(function() {
    jQuery(this).find(".changed").removeClass("changed");
    return true;
  })

  window.onbeforeunload = function() {
    if (eval("$\(\".changed\"\).length > 0")) {
      return "You have unsaved edits.";
    }
  }
});
