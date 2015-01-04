initialisePage();

function initialisePage() {
  $(document).ready(function() {
    setupNotificationContainer();
    setupNotifications();
  });
}

function setupNotificationContainer() {

  var width = $("#notificationContainer").width();
  $("#notificationLink").click(function() {
    $("#notificationContainer").fadeToggle(300);
    $("#notification_count").fadeOut("slow");
    return false;
  });

  $("#notificationContainer").hide();

  $("#notificationContainer").click(function() {
    return false;
  });
}

function setupNotifications() {
  notifications.getAll(function(success, data) {
    var template = '<div class="col-md-12" style="border-bottom:1px solid #616161;">{{content}} </div>';
    console.log(data);
    var maxLength = (data.length >= 11) ? 10 : data.length;
    for(i=0; i < maxLength; i++) {
      $("#notificationsBody").append( processTemplate(template, data[i]) );
    }
  });
}
