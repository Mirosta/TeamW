initialisePage();

function initialisePage() {
  loadRecentTransactions();
}

function loadRecentTransactions() {
  payments.getAll(function(success, paymentData) {
    console.log(paymentData);
    initialiseDataTables(paymentData);
  }, null, null, "-created");
}

function initialiseDataTables(paymentData) {
  $(document).ready(function() {
    // TODO add remaining debt
    var columnHeaders = ["payment by...", "payment to...", "created", "amount paid (£)"];
    var data = serverDataToArray(paymentData);

    // Add table to DOM
    $('#history-tbl-div').html("");
    $('#history-tbl-div').append('<table id="past-transactions-tbl" class="table table-striped" cellspacing="0" width="100%"></table>');
    
    // Initialise datatable with options
    $('#past-transactions-tbl').dataTable({
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
    finalArray.push([data[i].payer, data[i].readOnly.payee, data[i].created, data[i].amount]);
  }
  return finalArray;
}
