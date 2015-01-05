// Load groups
initialisePage();

function initialisePage() {
  $(document).ready(function() {
    $div = $("#dshbrd-recent-div"); // temporary
    loadRecentTransactions($div);
    loadGroupsIntoDashboard();
    loadFriendsIntoDashboard();
  });
}

function loadRecentTransactions($div) {
  payments.getAll(function(success, paymentData) {
    console.log(paymentData);
    initialiseDataTables(paymentData, $div);
  }, 10, null, "-created");
}


function initialiseDataTables(paymentData, $div) {
  $(document).ready(function() {
    // (temp) Column headings for DataTables table
    var columnHeaders = ["payment by...", "payment to...", "created", "amount paid (£)", "remaining debt"];
    var data = serverDataToArray(paymentData);

    // Add table to DOM
    $($div).html("");
    $($div).append('<table id="recent-transactions-tbl" class="table table-striped" cellspacing="0" width="100%"></table>');
    
    // Initialise datatable with options
    $('#recent-transactions-tbl').dataTable({
      "bLengthChange" : false,
      "bFilter" : false, 
      "paging" : false,
      "info" : false,
      "data" : data,
      "columns" : [
        { "title" : columnHeaders[0] },
        { "title" : columnHeaders[1] },
        { "title" : columnHeaders[2] },
        { "title" : columnHeaders[3] }
      ]
    });
  });
}

// Transforms object data from server to array for DataTables
function serverDataToArray(data) {
  var finalArray = [];
  for (i=0; i < data.length; i++) {
    finalArray.push([data[i].payer, data[i].readOnly.payee, data[i].created, data[i].amount ]);
  }
  return finalArray;
}



function loadGroupsIntoDashboard() {
  var template = '<div>{{name}}<span class="pull-right bold" style="color:{{readOnly.numberClass}};">{{readOnly.netAmount}}</span><br></div>';

  groups.getAll(function(success, groupData) {
    $('#groups-content-div').html("");
    for (i=0; i < groupData.length; i++) {
      groupData[i].readOnly.numberClass = (groupData[i].readOnly.netAmount >= 0 ? "#26A65B" : "#CF000F");
      groupData[i].readOnly.netAmount = penceToPound(groupData[i].readOnly.netAmount);
      $('#groups-content-div').append( processTemplate(template, groupData[i]) );
    } 
  });
}

function loadFriendsIntoDashboard() {
  var template = '<div>{{name}}<span class="pull-right bold" style="color:{{readOnly.numberClass}};">{{readOnly.netAmount}}</span><br></div>';
  friends.getAll(function(success, friendData) {
    $('#friends-content-div').html(""); 
    for (i=0; i < friendData.length; i++) {
      friendData[i].readOnly.numberClass = (friendData[i].readOnly.netAmount >= 0 ? "#26A65B" : "#CF000F");
      friendData[i].readOnly.netAmount = penceToPound(friendData[i].readOnly.netAmount);
      $('#friends-content-div').append( processTemplate(template, friendData[i]) );
    }
  });
}
