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
    markNotificationsSeen();
    return false;
  });

  $("#notificationContainer").hide();
/*
  $("#notificationContainer").click(function() {
    return false;
  });
*/
}

function setupNotifications() {
  notifications.getAll(function(success, data) {
    var template = '<div class="col-md-12 {{readOnly.notificationType}}" style="border-bottom:1px solid #616161;">{{content}} </div>';
    console.log(data);
    var maxLength = (data.length >= 11) ? 10 : data.length;
    for(i=0; i < maxLength; i++) {
      data[i].readOnly.notificationType = returnNotificationTypeCSS(data[i].type, data[i].seen)
      $("#notificationsBody").append( processTemplate(template, data[i]) );
    }
  });
  getUnreadNumber();
}

function returnNotificationTypeCSS(notificationType, seen) {
  var typeCSS = "";
  switch (notificationType) {
    case "FRIEND_REQUEST":
      typeCSS = "friendRequestNotification";
      break;
    case "INFO":
      typeCSS = "infoNotification";
      break;
    case "ERROR":
      typeCSS = "errorNotification";
      break;
    case "MISC":
      typeCSS = "miscNotification";
      break;
    case "SUCCESS":
      typeCSS = "successNotification";
      break;
  }
    return typeCSS + (seen ? " seenNotification" : "");
}

function markNotificationsSeen() {
  notifications.getAll(function(success, data) {
    for (var i = 0; i < data.length; i++) {
      data[i].seen = true;
      data[i].update();
    }
  });
  getUnreadNumber();
}

function getUnreadNumber() {
  notifications.getAll(function(success, data) {
    var read = 0;
    for (var i = 0; i < data.length; i++) {
      if (data[i].seen === false) {
        read++;
      }
      updateUnreadNumber(read);
    }
  })
}

function updateUnreadNumber(read) {
  $("#notificationLink>span.badge").html(read.toString());
}
