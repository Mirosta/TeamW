initialisePage();

var currentNotifications = [];

function initialisePage() {
  $(document).ready(function() {
    setupNotificationContainer();
    startNotificationPolling();
    setupFriendModal();
  });
}

function startNotificationPolling() {
    loadNotifications();
    setInterval(loadNotifications, 5000);
}

function setupNotificationContainer() {

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

function loadNotifications() {
  var $notifBody = $("#notificationsBody");
  notifications.getAll(function(success, data) {
      if(success)
      {
          currentNotifications = data;
          getUnreadNumber();
          $notifBody.html("");
          var template = '<div class="col-md-12 {{readOnly.notificationType}}" style="border-bottom:1px solid #616161;">{{content}} </div>';
          console.log(data);
          var maxLength = (data.length >= 11) ? 10 : data.length;
          for(i=0; i < maxLength; i++) {
              data[i].readOnly.notificationType = returnNotificationTypeCSS(data[i].type, data[i].seen)
              $notifBody.append( processTemplate(template, data[i]) );
          }
      }
  });
}

function setupFriendModal()
{
    $('#add-friend-btn').click(function() {
        var newFriend = friends.newInstance({'email': $('#email').val()});
        newFriend.create(function(success, data)
        {
            if(success)
            {
                $("#add-friend-modal").modal('hide');
                location.reload();
            }
            else
            {
                $("#add-friend-modal").find("div.addFriendError").html("Can't find that person").attr("style", "");
                console.log(data);
            }
        });
    });
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
      if(!data[i].seen) {
        data[i].seen = true;
        data[i].update();
      }
    }
  });
  getUnreadNumber();
}

function getUnreadNumber() {

    var read = 0;
    for (var i = 0; i < currentNotifications.length; i++) {
        if (currentNotifications[i].seen === false) {
            read++;
        }
        updateUnreadNumber(read);
    }
}

function updateUnreadNumber(read) {
  $("#notificationLink>span.badge").html(read.toString());
}
