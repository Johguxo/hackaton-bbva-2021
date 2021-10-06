
$(document).ready(function () {
  $('#submit').click(function () {
    var flag_login = true;
    var $inputs = $('#newForm :input');
    var values = {};
    $inputs.each(function () {
      values[this.name] = $(this).val();
      if (this.name == 'firstname') {
        flag_login = false;
      }
    });
    if (flag_login) {
      $.ajax({
        type: "POST",
        url: '/login-api/',
        headers: {
          "Authorization": token
        },
        contentType: "application/json",
        data: JSON.stringify(values),
        success: function (response) {
          alert(response);
        },
      });
    } else {
      $.ajax({
        type: "POST",
        url: '/register-api/',
        headers: {
          "Authorization": token
        },
        contentType: "application/json",
        data: JSON.stringify(values),
        success: function (response) {
          alert("Registrado");
        },
      });
    }
  })
  console.log("asdas", getCookie('csrftoken'));
});

function GetOptional() {
  data = {};
  forumQuestionsXhr = $.ajax({
    type: 'GET',
    url: '/question/question-report-list-api/',
    headers: {
      "Authorization": ''
    },
    data: data,
    success: function (response) {
      if (response.count == 0) {
        // Table is empty!
        setEmptyTableForumQuestionsResponse();
      } else {
        // Add lines to table!
        //$('#message_empty_table_registers').hide();
        drawTableForumQuestionsRows(response);
      }
    },
    error: function (error) {
      if (error.status == 401) {
        console.log('test');
        //unsubscribeUser();
        //localStorage.clear();
        //window.location.href = logoutUrl;
      }
    }
  });
}