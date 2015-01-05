initialisePage();

function initialisePage() {
  loadRecentTransactions();
}

function loadRecentTransactions() {
  payments.getAll(function(success, paymentData) {
    console.log(paymentData);
    var synchronised = new Synchronise(paymentData.length,
        function(success, error)
        {
            if(success) initialiseDataTables(paymentData);
            else console.log(error);
        });

    for(var i = 0; i < paymentData.length; i++)
    {
        lookupField({friends: ["payer","readOnly.payee"]}, paymentData[i], function (success, data)
        {
            if(success) synchronised.complete();
            else synchronised.failed(data);
        } );
    }
  }, null, null, "-created");
}

function initialiseDataTables(paymentData) {
  $(document).ready(function() {
    // TODO add remaining debt
    var columnHeaders = ["payment by...", "payment to...", "created", "amount paid (£)", "status"];
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
        { "title" : columnHeaders[3] },
        { "title" : columnHeaders[4] }
      ]
    });
  });
}

// Transforms object data from server to array for DataTables
function serverDataToArray(data) {
  var finalArray = [];
  for (i=0; i < data.length; i++) {
    var color = getColor(data[i].disputed, data[i].approvedByCreditor);
    var glyph = getGlyph(data[i].disputed, data[i].approvedByCreditor);
    finalArray.push([data[i].payer.name + " " + data[i].payer.familyName, data[i].readOnly.payee.name + " " + data[i].readOnly.payee.familyName, data[i].created, penceToPound(data[i].amount), '<span style="color: ' + color + ';" class="glyphicon ' + glyph + '"></span>']);
  }
  return finalArray;
}

function getColor(disputed, approved)
{
    if(disputed) return 'red';
    else if(!approved) return 'orange';
    else return 'green';
}

function getGlyph(disputed, approved)
{
    if(disputed) return "glyphicon-exclamation-sign";
    else if(!approved) return "glyphicon-question-sign";
    else return "glyphicon-ok-sign";
}
