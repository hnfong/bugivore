$.WatchUnsaved = {
  /* all watched forms, set during document.onready */
  forms      : null,

  /* reset the flag indicating whether the form is submitting */
  resetSubmitting: function(formNode) {
    formNode._isSubmitting = false;
  },

  /* check if a form is submitting */
  isSubmitting: function(formNode) {
    return formNode._isSubmitting;
  },

  /* wrap form.onsubmit to indicate submission for dirty check */
  wrapOnsubmit: function(formNode) {
    var submitCallback = formNode.onsubmit;
    formNode.onsubmit = function() {
      if (formNode._isSubmitting) return false;
      formNode._isSubmitting = true;
      if (submitCallback)
        return submitCallback.apply(this, arguments);
    }
  },
};

$(document).ready(function() {
  $.WatchUnsaved.forms = $('form.watch_unsaved');
  $.WatchUnsaved.forms.each(function() {
    var form = $(this);
    $.WatchUnsaved.resetSubmitting(form[0]);
    $.WatchUnsaved.wrapOnsubmit(form[0]);

    /* save initial data for all textarea under this form */
    $('textarea', form).each(function() {
      $(this).data('_watchInitVal', $(this).val());
    });

    /* We assume that the form is submitted via a submit button (i.e. not
     * other images or plain buttons). In such case, we protect the form
     * against multiple submission by disabling the submit button. */
    $(':submit', form).each(function() {
      submit = $(this);
      submit[0].onclick = function () {
        submit[0].disabled = true;
        submit[0]._isSubmitting = true;
      };
    });
  });

  window.onbeforeunload = function() {
    var msg = 'You have unsaved changes.';
    var isDirty = false;

    $.WatchUnsaved.forms.each(function() {
      var form = $(this);
      if ($.WatchUnsaved.isSubmitting(form[0]) === false) {
        /* non-submitting form */
        $('textarea', form).each(function() {
          if ($(this).data('_watchInitVal') != $(this).val())
            isDirty = true;
        });
      }
    });

    if (isDirty === true) {
      /* It is important to reset the submitting form as non-submitting, to
       * allow the user to resubmit the same form in case some other form on
       * the same page is dirty. And this should be done only when the
       * submission is interrupted by dirty check. */
      $.WatchUnsaved.forms.each(function() {
        var form = $(this);
        $.WatchUnsaved.resetSubmitting(form[0]);

        $(':submit', form).each(function (){
          submit = $(this);
          if (submit[0]._isSubmitting === true) {
            submit[0].disabled = false;
            submit[0]._isSubmitting = null;
          }
        });
      });

      return msg;
    }
  }
});
