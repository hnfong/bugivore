/* Add a class ``watch_unsaved'' to change forms in admin site, and let
 * watch_unsaved_edits to watch for unsaved changes. */

$(document).ready(function() {
  /* watch forms with non-empty id, thus excluding search forms  */
  $.WatchUnsaved.selector = 'form:not(id="")';
  /* recall watchForms, just in case */
  $.WatchUnsaved.watchForms();
});
