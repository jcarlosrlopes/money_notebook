$(document).ready(function(){

    var loadForm = function() {
        var btn = $(this);

        $.get(btn.attr("href"), function() {
            $("#modal").modal("show");
        }).done(function(data) {
            $("#modal .modal-content").html(data);
        }).fail(function() {
            console.log("erro");
        });

        return false;
    };
  
    var saveForm = function() {
      var form = $(this);
      $.ajax({
        url: form.attr("action"),
        data: form.serialize(),
        type: form.attr("method"),
        dataType: 'json',
        done: function (data) {
          if (data.form_is_valid) {
            $("#table tbody").html(data.list);
            $("#modal").modal("hide");
          }
          else {
            $("#modal .modal-content").html(data.html_form);
          }
        }
      });
      return false;
    };
  
    $("body").on('click', '.js-load-form', loadForm);
    $("body").on('submit', '.js-save-form', saveForm);
  })
  