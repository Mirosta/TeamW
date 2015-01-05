initialisePage();

function initialisePage() {
  $(document).ready(function () {
    addGroupsToContainer();

    $('#delete-modal').on('show.bs.modal', function(e) {
        groupKey = $(e.relatedTarget).parent().parent().data('group-key');
        $('#remove-group-btn').click(function() {
            removeGroup(groupKey);
            $('[data-group-key=' + groupKey + ']').remove();
            $('#delete-modal').modal('hide');
        });
    });
  });
}

function addGroupsToContainer() {
   var template = '<div class="group-container" style="height:40px;" data-group-key="{{key}}">' +
                    '<div class="pull-left"><span style="font-size:16px;"> {{name}}</span> (<span style="color:{{readOnly.numberClass}};font-weight:bold;">{{readOnly.netAmount}}</span>)</div>' +
                    '<div class="btn-group pull-right" role="group"><button type="button" class="btn btn-default" data-toggle="modal" data-target="#add-debt-modal"><i class="glyphicon glyphicon-gbp"></i></button><button type="button" class="btn btn-default" data-toggle="modal" data-target="#edit-modal"><i class="glyphicon glyphicon-edit"></i></button><button type="button" class="btn btn-default" data-toggle="modal" data-target="#delete-modal"><i class="glyphicon glyphicon-trash"></i></button><button type="button" class="btn btn-default"><b>...</b></button> </div>' +
                  '</div><hr style="margin-bottom:5px;">';
  var groupsListDiv = $("#groups-list-div");
  groupsListDiv.html("");

  groups.getAll(function(success, data) {
    console.log(data);
    for (i=0; i<data.length; i++) {
      data[i].readOnly.numberClass = (data[i].readOnly.netAmount >= 0 ? "#26A65B" : "#CF000F");
      data[i].readOnly.netAmount = penceToPound(data[i].readOnly.netAmount);
      groupsListDiv.append( processTemplate(template, data[i]) );
    }
  });
}

function removeGroup(key) {
  groups.get(key, function(success, data) {
      if (success) {
          console.log("got group");
          console.log(data);
          data.remove(function(success, data) {
              if (!success) {
                  console.log("error");
                  console.log(data);
              }
          });
      } else {
          console.log(data);
      }
  });
}
